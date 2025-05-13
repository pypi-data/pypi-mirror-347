# ================================================
# FILE: mcpo_control_panel/services/mcpo_service.py
# (Corrected function signatures for health check loop)
# ================================================
import asyncio
import logging
import os
import signal
import sys
import subprocess
import json
from typing import Optional, Tuple, List, Dict, Any, Callable # Added Callable
import httpx  # For health check and openapi requests
from sqlmodel import Session as SQLModelSession # To avoid conflict with FastAPI Session
import errno # For checking OS errors
from pathlib import Path
import contextlib

from ..models.mcpo_settings import McpoSettings
from .config_service import load_mcpo_settings, generate_mcpo_config_file, get_server_definitions
from ..db.database import engine # Import engine directly for background tasks

logger = logging.getLogger(__name__)

# --- Constants and Paths ---
DEFAULT_DATA_DIR_NAME_FOR_SERVICE = ".mcpo_manager_data"
PID_FILENAME = "mcpo_process.pid"

def _get_data_dir_path() -> Path:
    """Determines the path to the manager's data directory."""
    effective_data_dir_str = os.getenv("MCPO_MANAGER_DATA_DIR_EFFECTIVE")
    if effective_data_dir_str:
        data_dir = Path(effective_data_dir_str)
    else:
        data_dir = Path.home() / DEFAULT_DATA_DIR_NAME_FOR_SERVICE
    data_dir.mkdir(parents=True, exist_ok=True) # Ensure the directory exists
    return data_dir

def _get_pid_file_path() -> str:
    """Determines the full path to the PID file."""
    return str(_get_data_dir_path() / PID_FILENAME)

PID_FILE = _get_pid_file_path() # Dynamically set path

# --- Health Check State Variables ---
_health_check_failure_counter = 0
_mcpo_manual_operation_in_progress = False # Flag to prevent health checker interference

# --- Process State Management (PID file) ---

def _save_pid(pid: int):
    """Saves the MCPO process PID to the PID file."""
    pid_file_path_str = _get_pid_file_path()
    try:
        Path(pid_file_path_str).parent.mkdir(parents=True, exist_ok=True)
        with open(pid_file_path_str, "w") as f:
            f.write(str(pid))
        logger.info(f"MCPO process PID {pid} saved to {pid_file_path_str}")
    except IOError as e:
        logger.error(f"Error saving PID {pid} to {pid_file_path_str}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error saving PID {pid}: {e}", exc_info=True)

def _load_pid() -> Optional[int]:
    """Loads the MCPO process PID from the PID file."""
    pid_file_path_str = _get_pid_file_path()
    if not os.path.exists(pid_file_path_str):
        return None
    try:
        with open(pid_file_path_str, "r") as f:
            pid_str = f.read().strip()
            if pid_str:
                pid = int(pid_str)
                return pid
            logger.warning(f"PID file {pid_file_path_str} is empty.")
            return None
    except (IOError, ValueError) as e:
        logger.error(f"Error loading PID from {pid_file_path_str}: {e}. Removing invalid file.")
        _clear_pid() # Clear the invalid file
        return None
    except Exception as e:
        logger.error(f"Unexpected error loading PID from {pid_file_path_str}: {e}", exc_info=True)
        return None

def _clear_pid():
    """Deletes the PID file."""
    pid_file_path_str = _get_pid_file_path()
    if os.path.exists(pid_file_path_str):
        try:
            os.remove(pid_file_path_str)
            logger.info(f"PID file {pid_file_path_str} deleted.")
        except OSError as e:
            logger.error(f"Error deleting PID file {pid_file_path_str}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error deleting PID file {pid_file_path_str}: {e}", exc_info=True)

def _is_process_running(pid: Optional[int]) -> bool:
    """Checks if a process with the given PID is running."""
    if pid is None:
        return False

    if sys.platform == "win32":
        try:
            # Use shell=True cautiously, needed here for tasklist filter
            result = subprocess.run(
                f'tasklist /nh /fi "PID eq {pid}"',
                shell=True, capture_output=True, text=True, check=False, timeout=5
            )
            output = result.stdout.strip()
            # Process found if output is not empty and contains the PID
            return bool(output and str(pid) in output)
        except subprocess.TimeoutExpired:
            logger.error(f"Timeout checking process {pid} status on Windows.")
            return False # Assume not running if check timed out
        except Exception as e:
            logger.error(f"Error checking process {pid} status on Windows: {e}")
            return False # Assume not running on error

    else: # Unix-like systems
        try:
            os.kill(pid, 0) # Signal 0 checks existence and permissions
            return True
        except OSError as e:
            if e.errno == errno.ESRCH:
                # ESRCH: No such process
                return False
            elif e.errno == errno.EPERM:
                # EPERM: Operation not permitted - process exists, but we lack permissions
                # For status check, this means it IS running.
                logger.warning(f"Permission error checking PID {pid} (EPERM), but process likely exists.")
                return True
            else:
                logger.error(f"Unexpected OSError checking PID {pid}: {e}")
                return False
        except Exception as e:
            logger.error(f"Unexpected error checking PID {pid}: {e}", exc_info=True)
            return False

# --- Start/Stop/Restart MCPO ---

def _start_mcpo_subprocess_sync(settings: McpoSettings) -> Tuple[Optional[int], str]:
    """
    Synchronous function to start the mcpo process.
    Called via asyncio.to_thread.
    """
    command = ["mcpo", "--port", str(settings.port), "--config", settings.config_file_path]
    if settings.use_api_key and settings.api_key:
        command.extend(["--api-key", settings.api_key])

    logger.info(f"[Subprocess] Attempting to start mcpo: {' '.join(command)}")

    log_file_handle = None
    stdout_redir = subprocess.DEVNULL
    stderr_redir = subprocess.DEVNULL
    process_cwd = str(_get_data_dir_path()) # Use data dir as CWD by default

    try:
        # Configure log file redirection if specified
        if settings.log_file_path:
            log_dir = os.path.dirname(settings.log_file_path)
            if log_dir: # Only create if path includes a directory
                 Path(log_dir).mkdir(parents=True, exist_ok=True)
                 logger.info(f"[Subprocess] MCPO log directory created (or already exists): {log_dir}")

            try:
                # 'a' - append, buffering=1 - line buffering
                log_file_handle = open(settings.log_file_path, 'a', buffering=1, encoding='utf-8', errors='ignore')
                stdout_redir = log_file_handle
                stderr_redir = log_file_handle
                logger.info(f"[Subprocess] mcpo process stdout/stderr will be redirected to {settings.log_file_path}")
            except IOError as e:
                logger.error(f"[Subprocess] Failed to open log file '{settings.log_file_path}': {e}. Output will be redirected to DEVNULL.")
            except Exception as e:
                 logger.error(f"[Subprocess] Unexpected error opening log file '{settings.log_file_path}': {e}. Output will be redirected to DEVNULL.", exc_info=True)

        # Platform-specific Popen arguments
        process_kwargs = {
            "stdout": stdout_redir,
            "stderr": stderr_redir,
            "stdin": subprocess.DEVNULL,
            "cwd": process_cwd,
        }

        if sys.platform == "win32":
            # CREATE_NEW_PROCESS_GROUP allows killing the process tree via taskkill /T
            process_kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
        else: # Linux/Unix
            # Start in a new session to become process group leader
            # Required for reliable group kill via killpg
            process_kwargs["start_new_session"] = True

        # Start the process
        logger.info(f"[Subprocess] Launching Popen with command: {command} | CWD: {process_cwd} | Params: {process_kwargs}")
        process = subprocess.Popen(command, **process_kwargs)

        msg = f"MCPO process successfully started. PID: {process.pid}."
        logger.info(f"[Subprocess] {msg}")
        return process.pid, msg

    except FileNotFoundError:
        msg = f"Error starting mcpo: 'mcpo' command not found. Ensure mcpo is installed and in the system PATH for the user running the manager."
        logger.error(f"[Subprocess] {msg}")
        return None, msg
    except PermissionError as e:
        msg = f"Error starting mcpo: Permission denied executing command or accessing CWD ({process_cwd}). Error: {e}"
        logger.error(f"[Subprocess] {msg}")
        return None, msg
    except Exception as e:
        msg = f"Unexpected error starting mcpo process: {e}"
        logger.error(f"[Subprocess] {msg}", exc_info=True)
        return None, msg
    finally:
        # Close the log file handle if opened here
        if log_file_handle:
            try:
                log_file_handle.close()
            except Exception as e:
                logger.warning(f"[Subprocess] Failed to close log file handle: {e}")

async def start_mcpo(settings: McpoSettings) -> Tuple[bool, str]:
    """Asynchronously starts the MCPO process if it's not already running."""
    global _mcpo_manual_operation_in_progress, _health_check_failure_counter
    if _mcpo_manual_operation_in_progress:
        logger.warning("Attempted to start MCPO during another management operation. Aborted.")
        return False, "MCPO management operation already in progress."

    _mcpo_manual_operation_in_progress = True
    try:
        current_pid = _load_pid()
        if _is_process_running(current_pid):
            msg = f"MCPO process is already running with PID {current_pid}."
            logger.warning(msg)
            return False, msg # Not an error, just already running

        # Check config file existence before starting
        config_path = Path(settings.config_file_path)
        if not config_path.is_file():
            # Try creating the parent directory if it doesn't exist
            config_path.parent.mkdir(parents=True, exist_ok=True)
            if not config_path.is_file(): # Check again
                 msg = f"MCPO configuration file not found: {settings.config_file_path}. Cannot start. Please generate it (e.g., via 'Apply and Restart')."
                 logger.error(msg)
                 return False, msg

        logger.info(f"Attempting to start mcpo with settings: port={settings.port}, config='{settings.config_file_path}'...")

        # Run the synchronous start function in a separate thread
        pid, message = await asyncio.to_thread(_start_mcpo_subprocess_sync, settings)

        if pid:
            _save_pid(pid)
            _health_check_failure_counter = 0 # Reset health check failures after successful manual start
            logger.info(f"MCPO started. {message}")
            return True, message
        else:
            _clear_pid() # Clear PID file if start failed
            logger.error(f"Failed to start MCPO. {message}")
            return False, message
    except Exception as e:
        logger.error(f"Unexpected error during MCPO start: {e}", exc_info=True)
        return False, f"Internal error during start: {e}"
    finally:
        await asyncio.sleep(0.2) # Small delay before releasing flag
        _mcpo_manual_operation_in_progress = False

async def stop_mcpo() -> Tuple[bool, str]:
    """
    Asynchronously stops the MCPO process (and its group on Linux).
    Handles the case where the process check might lag slightly after SIGKILL.
    """
    global _mcpo_manual_operation_in_progress
    if _mcpo_manual_operation_in_progress:
        logger.warning("Attempted to stop MCPO during another management operation. Aborted.")
        return False, "MCPO management operation already in progress."

    _mcpo_manual_operation_in_progress = True
    pid_to_stop = _load_pid()

    try:
        if not pid_to_stop:
            msg = "MCPO process PID not found in file. Stop operation cannot proceed (might be already stopped or not started by manager)."
            logger.warning(msg)
            # Considered success as there's nothing to stop based on PID file
            return True, msg

        # Check if process exists *before* attempting stop
        if not _is_process_running(pid_to_stop):
            msg = f"MCPO process with PID {pid_to_stop} (from file) not found in the system. Clearing stale PID file."
            logger.warning(msg)
            _clear_pid()
            return True, msg # Success, process is already gone

        logger.info(f"Attempting to stop mcpo process with PID {pid_to_stop}...")
        stop_successful = False
        final_message = f"Failed to stop MCPO process (PID: {pid_to_stop})." # Default failure message

        try:
            if sys.platform == "win32":
                logger.info(f"Windows: Attempting to kill process tree with PID {pid_to_stop} using taskkill /F /T...")
                result = await asyncio.to_thread(
                    subprocess.run,
                    f'taskkill /F /T /PID {pid_to_stop}',
                    shell=True, capture_output=True, text=True, check=False, timeout=10
                )
                logger.info(f"Taskkill Result (PID: {pid_to_stop}): RC={result.returncode}, stdout='{result.stdout.strip()}', stderr='{result.stderr.strip()}'")
                await asyncio.sleep(1.0) # Give time for termination

                if not _is_process_running(pid_to_stop):
                    final_message = f"MCPO process (PID: {pid_to_stop}) stopped successfully via taskkill."
                    logger.info(final_message)
                    stop_successful = True
                else:
                    final_message = f"Failed to stop MCPO process (PID: {pid_to_stop}) using taskkill (RC={result.returncode}). Check permissions or process state."
                    logger.error(final_message + f" Stderr: {result.stderr.strip()}")
                    stop_successful = False

            else: # Linux/Unix - Use Process Group Killing
                pgid = -1
                try:
                    # Get Process Group ID (PGID)
                    pgid = os.getpgid(pid_to_stop)
                    logger.info(f"Linux: Found PGID {pgid} for PID {pid_to_stop}.")

                    # 1. Send SIGTERM to the group
                    logger.info(f"Linux: Sending SIGTERM to process group {pgid}...")
                    os.killpg(pgid, signal.SIGTERM)
                    await asyncio.sleep(1.5) # Wait for graceful termination

                    if not _is_process_running(pid_to_stop):
                        final_message = f"MCPO process group {pgid} (PID: {pid_to_stop}) stopped successfully via SIGTERM."
                        logger.info(final_message)
                        stop_successful = True
                    else:
                        # 2. Send SIGKILL to the group if SIGTERM failed
                        logger.warning(f"Linux: Process group {pgid} (PID: {pid_to_stop}) did not terminate after SIGTERM. Sending SIGKILL...")
                        os.killpg(pgid, signal.SIGKILL)
                        # Wait slightly longer after SIGKILL to allow system state update
                        await asyncio.sleep(2.0)

                        # *** Final Check after SIGKILL ***
                        if not _is_process_running(pid_to_stop):
                            final_message = f"MCPO process group {pgid} (PID: {pid_to_stop}) stopped successfully via SIGKILL."
                            logger.info(final_message)
                            stop_successful = True
                        else:
                            # Process still appears running *after* SIGKILL
                            final_message = (f"WARNING: Process check still reports PID {pid_to_stop} (PGID: {pgid}) as running after SIGKILL! "
                                             f"This is unexpected. Assuming kernel terminated the process. Check system state (e.g., 'ps', 'top').")
                            logger.warning(final_message)
                            # Consider stop successful from manager's perspective as SIGKILL was sent.
                            stop_successful = True

                except ProcessLookupError:
                    final_message = f"Process with PID {pid_to_stop} not found during stop attempt (possibly terminated concurrently)."
                    logger.warning(final_message)
                    stop_successful = True # Consider success as it's gone
                except PermissionError:
                     final_message = f"Permission denied sending signal to process group {pgid} (PID: {pid_to_stop}). Ensure manager has sufficient privileges."
                     logger.error(final_message)
                     stop_successful = False
                except Exception as e_inner:
                     final_message = f"Unexpected error stopping process/group (PID: {pid_to_stop}, PGID: {pgid}): {e_inner}"
                     logger.error(final_message, exc_info=True)
                     stop_successful = False

        except Exception as e_outer:
            final_message = f"Outer error during stop attempt for mcpo (PID: {pid_to_stop}): {e_outer}"
            logger.error(final_message, exc_info=True)
            stop_successful = False

        # Clear PID file ONLY if stop was considered successful
        if stop_successful:
            _clear_pid()

        return stop_successful, final_message

    except Exception as e_main:
         logger.error(f"Critical error in stop_mcpo function (PID: {pid_to_stop}): {e_main}", exc_info=True)
         return False, f"Internal error in stop_mcpo function: {e_main}"
    finally:
        await asyncio.sleep(0.2)
        _mcpo_manual_operation_in_progress = False

async def restart_mcpo_process_with_new_config(db_session: SQLModelSession, settings: McpoSettings) -> Tuple[bool, str]:
    """
    Stops mcpo, generates a new config, and starts mcpo.
    Used by 'Apply and Restart' and the Health Checker.
    """
    global _mcpo_manual_operation_in_progress
    # Prevent concurrent restarts
    if _mcpo_manual_operation_in_progress and not settings.health_check_enabled :
        logger.warning("Restart process already initiated, new restart request ignored.")
        return False, "Restart process already in progress."

    _mcpo_manual_operation_in_progress = True
    logger.info("Starting MCPO restart process...")
    final_messages = []
    restart_success = False

    try:
        # 1. Stop the current process (if running)
        current_pid = _load_pid()
        stop_needed = _is_process_running(current_pid)

        if stop_needed:
            logger.info(f"Restart: Detected running MCPO process (PID: {current_pid}). Attempting stop...")
            # stop_mcpo manages the _mcpo_manual_operation_in_progress flag and clears PID on success
            # It will release the flag in its finally block
            stop_success, stop_msg = await stop_mcpo()
            final_messages.append(f"Stop: {stop_msg}")
            if not stop_success:
                message = " | ".join(final_messages) + " CRITICAL ERROR: Failed to stop current MCPO process. Restart cancelled."
                logger.error(message)
                # Flag _mcpo_manual_operation_in_progress should be released in stop_mcpo's finally block
                return False, message
        else:
            logger.info("Restart: Running MCPO process not detected (or PID not found). Skipping stop.")
            _clear_pid() # Clear PID just in case it was stale

        # 2. Generate new configuration file
        logger.info("Restart: Generating new MCPO configuration file...")
        config_generated = generate_mcpo_config_file(db_session, settings)
        if not config_generated:
            message = " | ".join(final_messages) + " ERROR: Failed to generate configuration file. MCPO start cancelled."
            logger.error(message)
            # Release flag if stop wasn't called or if config generation failed
            _mcpo_manual_operation_in_progress = False
            return False, message
        final_messages.append("Configuration file successfully generated.")

        # 3. Start MCPO with the new configuration
        logger.info("Restart: Attempting to start MCPO with the new configuration...")
        # start_mcpo manages its own _mcpo_manual_operation_in_progress flag and resets health check counter
        start_success, start_msg = await start_mcpo(settings)
        final_messages.append(f"Start: {start_msg}")
        restart_success = start_success

    except Exception as e:
        logger.error(f"Unexpected error during MCPO restart process: {e}", exc_info=True)
        final_messages.append(f"Critical restart error: {e}")
        restart_success = False
        # Ensure flag is released if error happened outside start/stop
        _mcpo_manual_operation_in_progress = False

    return restart_success, " | ".join(final_messages)

# --- Get Status and Logs ---

def get_mcpo_status() -> str:
    """Returns the string status of the MCPO process: RUNNING, STOPPED, ERROR."""
    pid = _load_pid()
    if pid is None:
        return "STOPPED" # PID file not found

    if _is_process_running(pid):
        return "RUNNING" # Process with PID from file found and running
    else:
        # PID file exists, but process not found - this indicates an issue or stale file
        logger.warning(f"MCPO Status: PID {pid} found in file, but the corresponding process is NOT running -> ERROR")
        return "ERROR"

async def get_mcpo_logs(lines: int = 100, log_file_path: Optional[str] = None) -> List[str]:
    """Asynchronously reads the last N lines from the MCPO log file."""
    settings = load_mcpo_settings()
    actual_log_path = log_file_path or settings.log_file_path

    if not actual_log_path:
        logger.warning("Attempted to read MCPO logs, but log file path is not configured.")
        return ["Error: Log file path is not configured."]
    if not os.path.exists(actual_log_path):
        logger.warning(f"Attempted to read MCPO logs, but file not found: {actual_log_path}")
        return [f"Error: Log file not found at path: {actual_log_path}"]

    try:
        from collections import deque
        last_lines = deque(maxlen=lines)

        # Read file line by line in binary mode and decode ignoring errors
        def read_lines_sync():
            try:
                with open(actual_log_path, 'rb') as f:
                    # Simple read from beginning for reliability with deque
                    for line_bytes in f:
                        last_lines.append(line_bytes.decode('utf-8', errors='ignore').rstrip())
                return list(last_lines)
            except Exception as read_e:
                logger.error(f"Error during log file read {actual_log_path} in thread: {read_e}", exc_info=True)
                return [f"Error reading logs: {read_e}"]

        return await asyncio.to_thread(read_lines_sync)

    except Exception as e:
        logger.error(f"Error preparing to read log file {actual_log_path}: {e}", exc_info=True)
        return [f"Error preparing log read: {e}"]

# --- Tool Aggregation ---
# (get_aggregated_tools_from_mcpo remains unchanged)
async def get_aggregated_tools_from_mcpo(db_session: SQLModelSession) -> Dict[str, Any]:
    """
    Aggregates tools from the running MCPO instance.
    Returns a dictionary with status, a list of servers with their tools,
    and the public base URL for generating links.
    """
    logger.info("Aggregating tools from running MCPO instance...")
    mcpo_status = get_mcpo_status()
    settings = load_mcpo_settings() # Load current settings

    # Determine base URL for links in the UI
    base_url_for_links = ""
    if settings.public_base_url:
        base_url_for_links = settings.public_base_url.rstrip('/')
        logger.debug(f"Using public base URL for links: {base_url_for_links}")
    elif mcpo_status == "RUNNING": # Use local URL only if MCPO is running
        base_url_for_links = f"http://127.0.0.1:{settings.port}"
        logger.debug(f"Public base URL not set, using local for links: {base_url_for_links}")
    else:
         logger.debug("Public base URL not set, MCPO not running, links will not be generated.")

    # Initialize result
    result: Dict[str, Any] = {
        "status": mcpo_status,
        "servers": {},
        "base_url_for_links": base_url_for_links
    }

    if mcpo_status != "RUNNING":
        logger.warning(f"Cannot aggregate tools, MCPO status: {mcpo_status}")
        return result

    # Determine internal URL for API requests to MCPO (always localhost)
    mcpo_internal_api_url = f"http://127.0.0.1:{settings.port}"
    headers = {}
    if settings.use_api_key and settings.api_key:
        headers["Authorization"] = f"Bearer {settings.api_key}"

    # Get enabled server definitions from DB
    enabled_definitions = get_server_definitions(db_session, only_enabled=True, limit=10000)
    if not enabled_definitions:
        logger.info("No enabled server definitions found in the database.")
        return result

    # --- Nested async function to fetch OpenAPI spec for one server ---
    async def fetch_openapi(definition):
        server_name = definition.name
        # Skip request for internal Health Check echo server
        if server_name == settings.INTERNAL_ECHO_SERVER_NAME and settings.health_check_enabled:
            return server_name, {"status": "SKIPPED", "error_message": "Internal echo server (skipped).", "tools": []}

        # Format URL for openapi.json request to MCPO
        url = f"{mcpo_internal_api_url}/{server_name}/openapi.json"
        server_result_data = {"status": "ERROR", "error_message": None, "tools": []}
        try:
            async with httpx.AsyncClient(headers=headers, timeout=10.0, follow_redirects=True) as client:
                logger.debug(f"Requesting OpenAPI for server '{server_name}' at URL: {url}")
                resp = await client.get(url)

                if resp.status_code == 200:
                    try:
                        openapi_data = resp.json()
                        paths = openapi_data.get("paths", {})
                        found_tools = []
                        for path, methods in paths.items():
                            if post_method_details := methods.get("post"):
                                tool_info = {
                                    "path": path,
                                    "summary": post_method_details.get("summary", ""),
                                    "description": post_method_details.get("description", "")
                                }
                                found_tools.append(tool_info)
                        server_result_data["tools"] = found_tools
                        server_result_data["status"] = "OK"
                        logger.debug(f"Server '{server_name}': Found {len(found_tools)} tools.")
                    except json.JSONDecodeError as json_e:
                         server_result_data["error_message"] = f"Error parsing JSON response from MCPO: {json_e}"
                         logger.warning(f"Error parsing OpenAPI JSON for '{server_name}' (HTTP {resp.status_code}): {resp.text[:200]}...")

                else:
                    error_text = resp.text[:200]
                    server_result_data["error_message"] = f"MCPO Error (HTTP {resp.status_code}): {error_text}"
                    logger.warning(f"Error requesting OpenAPI for '{server_name}' (HTTP {resp.status_code}): {error_text}")

        except httpx.RequestError as e:
            server_result_data["error_message"] = f"Network error: {e.__class__.__name__}"
            logger.warning(f"Network error requesting OpenAPI for '{server_name}': {e}")
        except Exception as e:
            server_result_data["error_message"] = f"Internal error: {e.__class__.__name__}"
            logger.warning(f"Error processing OpenAPI for '{server_name}': {e}", exc_info=True)

        return server_name, server_result_data
    # --- End of nested fetch_openapi function ---

    # Start requests to all servers concurrently
    tasks = [fetch_openapi(d) for d in enabled_definitions]
    fetch_results = await asyncio.gather(*tasks, return_exceptions=True) # Gather results and exceptions

    # Collect results into the final dictionary
    for i, definition in enumerate(enabled_definitions):
         server_name = definition.name
         result_item = fetch_results[i]
         if isinstance(result_item, Exception):
             logger.error(f"Exception fetching OpenAPI for '{server_name}': {result_item}", exc_info=result_item)
             result["servers"][server_name] = {"status": "ERROR", "error_message": f"Exception: {result_item.__class__.__name__}", "tools": []}
         elif isinstance(result_item, tuple) and len(result_item) == 2:
             # Expected result: tuple (server_name, server_result)
             _, server_result = result_item
             result["servers"][server_name] = server_result
         else:
              logger.error(f"Unexpected result from asyncio.gather for '{server_name}': {result_item}")
              result["servers"][server_name] = {"status": "ERROR", "error_message": "Unexpected internal result", "tools": []}

    logger.info(f"Tool aggregation finished. Processed {len(enabled_definitions)} definitions.")
    return result


# --- Health Check Logic ---

@contextlib.asynccontextmanager
async def get_async_db_session(engine_to_use=engine):
    """Async context manager for getting a DB session in background tasks."""
    session = None
    try:
        # Create a new session directly from the engine
        session = SQLModelSession(engine_to_use)
        yield session
    except Exception as e:
        logger.error(f"Error creating DB session in background task: {e}", exc_info=True)
        raise # Re-raise exception for caller to handle
    finally:
        if session:
            try:
                session.close()
            except Exception as e:
                logger.error(f"Error closing DB session in background task: {e}", exc_info=True)

# <<< CORRECTED SIGNATURE >>>
async def run_health_check_loop_async(get_db_session_func: Callable):
    """Asynchronous loop for periodic MCPO health checks."""
    global _health_check_failure_counter, _mcpo_manual_operation_in_progress
    logger.info("Starting background MCPO health check loop...")

    await asyncio.sleep(10) # Initial delay before first check

    while True:
        try:
             settings = load_mcpo_settings()
        except Exception as e:
             logger.error(f"Health Check: CRITICAL ERROR loading settings. Loop paused. Error: {e}", exc_info=True)
             await asyncio.sleep(60) # Wait a minute before retrying settings load
             continue

        if not settings.health_check_enabled:
            if _health_check_failure_counter > 0:
                logger.info("Health Check: Check disabled, resetting failure counter.")
                _health_check_failure_counter = 0
            await asyncio.sleep(settings.health_check_interval_seconds)
            continue

        if _mcpo_manual_operation_in_progress:
            logger.info("Health Check: Manual MCPO management detected, skipping check.")
            await asyncio.sleep(max(1, settings.health_check_failure_retry_delay_seconds // 2))
            continue

        # Check process status before HTTP check
        mcpo_status = get_mcpo_status()
        if mcpo_status != "RUNNING":
            logger.warning(f"Health Check: MCPO process not running (status: {mcpo_status}). Skipping HTTP check.")
            # Reset counter if stopped, increment if ERROR
            if mcpo_status == "STOPPED" and _health_check_failure_counter > 0:
                 logger.info(f"Health Check: MCPO stopped, resetting failure counter.")
                 _health_check_failure_counter = 0
            elif mcpo_status == "ERROR":
                 logger.warning(f"Health Check: MCPO status is ERROR. Incrementing failure counter.")
                 _health_check_failure_counter += 1
                 # Pass the get_db_session_func down
                 await handle_health_check_failure(settings, get_db_session_func) # <<< PASS ARGUMENT HERE

            await asyncio.sleep(settings.health_check_interval_seconds)
            continue

        # Validate essential settings for the check
        if not settings.INTERNAL_ECHO_SERVER_NAME or not settings.INTERNAL_ECHO_TOOL_PATH:
             logger.error("Health Check: INTERNAL_ECHO_SERVER_NAME or INTERNAL_ECHO_TOOL_PATH not configured. Check cannot proceed.")
             await asyncio.sleep(settings.health_check_interval_seconds * 2) # Wait longer
             continue

        # Format URL and payload for the request
        health_check_url = f"http://127.0.0.1:{settings.port}/{settings.INTERNAL_ECHO_SERVER_NAME.strip('/')}{settings.INTERNAL_ECHO_TOOL_PATH.strip('/')}"
        payload = settings.INTERNAL_ECHO_PAYLOAD
        headers = {}
        if settings.use_api_key and settings.api_key:
            headers["Authorization"] = f"Bearer {settings.api_key}"

        # --- Perform HTTP Health Check ---
        try:
            async with httpx.AsyncClient(headers=headers, timeout=settings.health_check_timeout_seconds, follow_redirects=True) as client:
                logger.debug(f"Health Check: Sending POST to {health_check_url} (timeout: {settings.health_check_timeout_seconds}s)")
                response = await client.post(health_check_url, json=payload)

            if 200 <= response.status_code < 300:
                if _health_check_failure_counter > 0:
                    logger.info(f"Health Check: SUCCESS (Status: {response.status_code}). Failure counter reset.")
                else:
                     logger.debug(f"Health Check: Success (Status: {response.status_code}).")
                _health_check_failure_counter = 0
                await asyncio.sleep(settings.health_check_interval_seconds) # Wait normal interval
            else:
                logger.warning(f"Health Check: FAILURE (Status: {response.status_code}). URL: {health_check_url}. Response: {response.text[:200]}")
                _health_check_failure_counter += 1
                # Pass the get_db_session_func down
                await handle_health_check_failure(settings, get_db_session_func) # <<< PASS ARGUMENT HERE

        except httpx.ConnectError as e:
            logger.error(f"Health Check: Connection error requesting MCPO ({health_check_url}). Error: {e}")
            _health_check_failure_counter += 1
            # Pass the get_db_session_func down
            await handle_health_check_failure(settings, get_db_session_func) # <<< PASS ARGUMENT HERE
        except httpx.TimeoutException:
            logger.error(f"Health Check: Timeout ({settings.health_check_timeout_seconds}s) requesting MCPO ({health_check_url}).")
            _health_check_failure_counter += 1
            # Pass the get_db_session_func down
            await handle_health_check_failure(settings, get_db_session_func) # <<< PASS ARGUMENT HERE
        except httpx.RequestError as e:
            logger.error(f"Health Check: Network error requesting MCPO ({health_check_url}). Error: {e.__class__.__name__}: {e}")
            _health_check_failure_counter += 1
            # Pass the get_db_session_func down
            await handle_health_check_failure(settings, get_db_session_func) # <<< PASS ARGUMENT HERE
        except Exception as e:
            logger.error(f"Health Check: Unexpected error ({health_check_url}). Error: {e.__class__.__name__}: {e}", exc_info=True)
            _health_check_failure_counter += 1
            # Pass the get_db_session_func down
            await handle_health_check_failure(settings, get_db_session_func) # <<< PASS ARGUMENT HERE

# <<< CORRECTED SIGNATURE >>>
async def handle_health_check_failure(settings: McpoSettings, get_db_session_func: Callable):
    """Handles a failed health check, deciding if a restart is needed."""
    global _health_check_failure_counter, _mcpo_manual_operation_in_progress

    logger.info(f"Health Check: Failure attempt {_health_check_failure_counter} of {settings.health_check_failure_attempts}.")

    if _health_check_failure_counter >= settings.health_check_failure_attempts:
        logger.warning(f"Health Check: Reached maximum ({settings.health_check_failure_attempts}) failed check attempts.")

        if settings.auto_restart_on_failure:
            logger.info("Health Check: Auto-restart enabled. Attempting MCPO restart...")

            restart_success = False
            restart_message = "Failed to get DB session for restart."
            try:
                # Use the context manager which internally uses the global engine
                # The 'get_db_session_func' argument is now accepted but not explicitly used here,
                # which resolves the TypeError from main.py.
                async with get_async_db_session() as db_session:
                    if db_session:
                        # Call restart function, it manages _mcpo_manual_operation_in_progress flag
                        restart_success, restart_message = await restart_mcpo_process_with_new_config(db_session, settings)
                    else:
                         logger.error("Health Check: Failed to get DB session for restart (context manager returned None). Auto-restart cancelled.")
            except Exception as e_db:
                 logger.error(f"Health Check: Error getting DB session for restart: {e_db}", exc_info=True)
                 restart_message = f"DB Session Error: {e_db}"

            if restart_success:
                logger.info(f"Health Check: MCPO successfully restarted after failures. Message: {restart_message}")
                _health_check_failure_counter = 0 # Reset counter after successful restart
                await asyncio.sleep(settings.health_check_interval_seconds) # Wait normal interval
            else:
                logger.error(f"Health Check: Automatic MCPO restart FAILED after failures. Message: {restart_message}")
                # Increase pause significantly if auto-restart failed, especially if stop failed
                failed_restart_pause = settings.health_check_interval_seconds * 5
                logger.warning(f"Health Check: Increased pause to {failed_restart_pause}s due to failed auto-restart.")
                _health_check_failure_counter = 0 # Reset counter to avoid immediate retry loop, but problem persists
                await asyncio.sleep(failed_restart_pause)

        else: # auto_restart_on_failure is False
            logger.info("Health Check: Auto-restart disabled. Manual intervention required to restore MCPO.")
            _health_check_failure_counter = 0 # Reset counter to prevent log spam
            await asyncio.sleep(settings.health_check_interval_seconds) # Wait normal interval
    else:
        # Max attempts not yet reached
        logger.info(f"Health Check: Waiting {settings.health_check_failure_retry_delay_seconds}s before next check attempt...")
        await asyncio.sleep(settings.health_check_failure_retry_delay_seconds)