
import subprocess
import shlex
import os

def run_command(command: str) -> str:
    """Runs a shell command and returns output."""
    try:
        # Security: In a real app we'd be very careful here.
        # For this prototype we allow execution as requested.
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        return f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    except Exception as e:
        return f"Execution Error: {e}"

def open_app(app_name: str) -> str:
    """Opens an application."""
    try:
        # Very basic windows implementation
        # start command is shell specific
        if os.name == 'nt':
            os.system(f"start {app_name}")
        else:
            # Linux/Mac fallback (xdg-open or open)
            subprocess.Popen([app_name]) 
        return f"Opened {app_name}"
    except Exception as e:
        return f"Error opening app: {e}"
