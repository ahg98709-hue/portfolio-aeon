
import os
import sys
import platform
import subprocess
import psutil
import socket
import datetime
import webbrowser
import shutil
from typing import List, Dict, Optional, Union

# --- Application Management ---

def open_application(app_name_or_path: str) -> str:
    """
    Opens an application. 
    Tries to launch by name (using system path) or absolute path.
    """
    try:
        # Check if it's a simple name and exists in PATH
        if os.path.sep not in app_name_or_path:
            full_path = shutil.which(app_name_or_path)
            if full_path:
                app_name_or_path = full_path
        
        if platform.system() == "Windows":
            # os.startfile is best for files/apps associated with the OS
            try:
                os.startfile(app_name_or_path)
                return f"Launched {app_name_or_path}"
            except OSError:
                # Fallback to subprocess with shell=True for commands like 'notepad'
                subprocess.Popen(f'start "" "{app_name_or_path}"', shell=True)
                return f"Launched {app_name_or_path} via shell"

        elif platform.system() == "Darwin": # macOS
            subprocess.Popen(["open", app_name_or_path])
        else: # Linux
            subprocess.Popen(["xdg-open", app_name_or_path])
        return f"Launched {app_name_or_path}"
    except Exception as e:
        # Final fallback
        try:
            subprocess.Popen(app_name_or_path, shell=True)
            return f"Launched {app_name_or_path} via subprocess fallback"
        except Exception as e2:
            return f"Failed to launch {app_name_or_path}: {e}, {e2}"

def close_application(process_name: str) -> str:
    """Terminates a process by name."""
    count = 0
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] and process_name.lower() in proc.info['name'].lower():
            try:
                proc.kill()
                count += 1
            except:
                pass
    return f"Terminated {count} instances of {process_name}"

def is_process_running(process_name: str) -> bool:
    """Checks if a process is running."""
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and process_name.lower() in proc.info['name'].lower():
            return True
    return False

def get_process_id(process_name: str) -> List[int]:
    """Returns PIDs for a process name."""
    pids = []
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] and process_name.lower() in proc.info['name'].lower():
            pids.append(proc.info['pid'])
    return pids

def run_command(command: str) -> str:
    """Runs a shell command and returns output."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        return str(e)

# --- System Information ---

def get_os_info() -> str:
    """Returns OS information."""
    return f"{platform.system()} {platform.release()} ({platform.version()})"

def get_cpu_usage() -> float:
    """Returns CPU usage percentage."""
    return psutil.cpu_percent(interval=1)

def get_ram_usage() -> Dict[str, Union[float, int]]:
    """Returns RAM usage statistics."""
    mem = psutil.virtual_memory()
    return {
        "total": mem.total,
        "available": mem.available,
        "percent": mem.percent,
        "used": mem.used,
        "free": mem.free
    }

def get_disk_usage(path: str = "/") -> Dict[str, Union[float, int]]:
    """Returns disk usage statistics."""
    try:
        usage = shutil.disk_usage(path)
        return {
            "total": usage.total,
            "used": usage.used,
            "free": usage.free,
            "percent": (usage.used / usage.total) * 100
        }
    except:
        return {}

def get_boot_time() -> str:
    """Returns system boot time."""
    return datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")

def get_active_user() -> str:
    """Returns current user name."""
    return os.getlogin()

# --- Network Info ---

def get_hostname() -> str:
    return socket.gethostname()

def get_local_ip() -> str:
    try:
        return socket.gethostbyname(socket.gethostname())
    except:
        return "127.0.0.1"

# --- Power Management (Windows/Linux) ---

def shutdown_system(delay: int = 0) -> str:
    """Shuts down the system."""
    try:
        if platform.system() == "Windows":
            os.system(f"shutdown /s /t {delay}")
        else:
            os.system(f"shutdown -h +{delay}")
        return "Shutting down..."
    except Exception as e:
        return str(e)

def restart_system(delay: int = 0) -> str:
    """Restarts the system."""
    try:
        if platform.system() == "Windows":
            os.system(f"shutdown /r /t {delay}")
        else:
            os.system(f"shutdown -r +{delay}")
        return "Restarting..."
    except Exception as e:
        return str(e)

def lock_screen() -> str:
    """Locks the workstation."""
    try:
        if platform.system() == "Windows":
            os.system("rundll32.exe user32.dll,LockWorkStation")
            return "Locked"
        return "Not supported on this OS"
    except Exception as e:
        return str(e)

# --- Python Environment ---

def get_python_version() -> str:
    return sys.version

def get_installed_packages() -> List[str]:
    """Returns list of installed pip packages."""
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "list"], capture_output=True, text=True)
        return result.stdout.splitlines()
    except:
        return []

# --- Messaging Helpers (User Request) ---

def open_whatsapp(phone_number: str, message: str = "") -> str:
    """Opens WhatsApp Web with pre-filled message."""
    url = f"https://wa.me/{phone_number}?text={message}"
    webbrowser.open(url)
    return f"Opened WhatsApp for {phone_number}"

def open_telegram(username: str) -> str:
    """Opens Telegram chat."""
    url = f"https://t.me/{username}"
    webbrowser.open(url)
    return f"Opened Telegram for {username}"

def open_youtube_search(query: str) -> str:
    """Searches YouTube."""
    url = f"https://www.youtube.com/results?search_query={query}"
    webbrowser.open(url)
    return f"Searching YouTube for {query}"

def open_google_search(query: str) -> str:
    """Searches Google."""
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    return f"Searching Google for {query}"

def open_url(url: str) -> str:
    """Opens any URL in default browser."""
    webbrowser.open(url)
    return f"Opened {url}"
