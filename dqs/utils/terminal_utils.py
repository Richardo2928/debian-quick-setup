import subprocess

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def log(message: str) -> None:
    """Logs a message to the terminal."""
    print(f"\n{YELLOW}{message}{RESET}")
    
def ok(message: str) -> None:
    """Logs a success message to the terminal."""
    print(f"{GREEN}{message}{RESET}")

def error(message: str) -> None:
    """Logs an error message to the terminal."""
    print(f"{RED}{message}{RESET}")
    
def run_command(command: str) -> bool:
    """Runs a shell command and returns True if it succeeds, False otherwise."""
    try:
        log(f"Running: {command}")
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        error(f"Command failed: {e.stderr.decode().strip()}")
        return False