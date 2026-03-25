
import subprocess
import os
from typing import List, Dict

# --- Git Operations ---

def git_init(path: str) -> str:
    return subprocess.run(["git", "init", path], capture_output=True, text=True).stdout

def git_clone(url: str, path: str) -> str:
    return subprocess.run(["git", "clone", url, path], capture_output=True, text=True).stdout

def git_status(path: str) -> str:
    return subprocess.run(["git", "-C", path, "status"], capture_output=True, text=True).stdout

def git_add(path: str, files: List[str] = ["."]) -> str:
    return subprocess.run(["git", "-C", path, "add"] + files, capture_output=True, text=True).stdout

def git_commit(path: str, message: str) -> str:
    return subprocess.run(["git", "-C", path, "commit", "-m", message], capture_output=True, text=True).stdout

def git_push(path: str, remote: str = "origin", branch: str = "main") -> str:
    return subprocess.run(["git", "-C", path, "push", remote, branch], capture_output=True, text=True).stdout

def git_pull(path: str, remote: str = "origin", branch: str = "main") -> str:
    return subprocess.run(["git", "-C", path, "pull", remote, branch], capture_output=True, text=True).stdout

def git_log(path: str, limit: int = 5) -> str:
    return subprocess.run(["git", "-C", path, "log", f"-n {limit}"], capture_output=True, text=True).stdout

def git_diff(path: str) -> str:
    return subprocess.run(["git", "-C", path, "diff"], capture_output=True, text=True).stdout

def git_branch(path: str) -> str:
    return subprocess.run(["git", "-C", path, "branch"], capture_output=True, text=True).stdout

def git_checkout(path: str, branch: str, create: bool = False) -> str:
    cmd = ["git", "-C", path, "checkout"]
    if create: cmd.append("-b")
    cmd.append(branch)
    return subprocess.run(cmd, capture_output=True, text=True).stdout

# --- Package Management ---

def pip_install(package: str) -> str:
    return subprocess.run(["pip", "install", package], capture_output=True, text=True).stdout

def pip_uninstall(package: str) -> str:
    return subprocess.run(["pip", "uninstall", "-y", package], capture_output=True, text=True).stdout

def pip_freeze() -> str:
    return subprocess.run(["pip", "freeze"], capture_output=True, text=True).stdout

def npm_install(package: str = "") -> str:
    cmd = ["npm", "install"]
    if package: cmd.append(package)
    return subprocess.run(cmd, capture_output=True, text=True, shell=True).stdout

def npm_run(script: str) -> str:
    return subprocess.run(["npm", "run", script], capture_output=True, text=True, shell=True).stdout

# --- Docker Operations (if available) ---

def docker_images() -> str:
    return subprocess.run(["docker", "images"], capture_output=True, text=True).stdout

def docker_ps(all: bool = False) -> str:
    cmd = ["docker", "ps"]
    if all: cmd.append("-a")
    return subprocess.run(cmd, capture_output=True, text=True).stdout

def docker_stop(container_id: str) -> str:
    return subprocess.run(["docker", "stop", container_id], capture_output=True, text=True).stdout

def docker_start(container_id: str) -> str:
    return subprocess.run(["docker", "start", container_id], capture_output=True, text=True).stdout

def docker_logs(container_id: str, tail: int = 20) -> str:
    return subprocess.run(["docker", "logs", "--tail", str(tail), container_id], capture_output=True, text=True).stdout
