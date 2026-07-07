import subprocess

def echo_message(message):
    """Echo a message back to the caller using the system shell."""
    result = subprocess.run(f"echo {message}", shell=True, capture_output=True, text=True)
    return result.stdout.strip()
