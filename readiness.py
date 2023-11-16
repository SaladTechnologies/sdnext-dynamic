import requests
import sys

image_gen_url = "http://127.0.0.1:7860"


def get_sdnext_server_status():
    """
    Checks the status of the SDNext server.
    Returns:
        True if the server status can be retrieved, False otherwise.
    """
    try:
        url = f"{image_gen_url}/sdapi/v1/system-info/status?state=true&memory=true&full=true&refresh=true"
        response = requests.get(url)
        if response.status_code == 200:
            return True
    except Exception:
        pass
    return False


def get_sdnext_logs():
    """
    Checks the last 5 lines of the SDNext server logs.
    Returns:
        True if the logs indicate that the model has loaded, False otherwise.
    """
    try:
        url = f"{image_gen_url}/sdapi/v1/log?lines=5&clear=true"
        response = requests.get(url)
        if response.status_code == 200:
            logs = response.json()
            return any("Startup time:" in line for line in logs)
    except Exception:
        pass
    return False


def check_readiness():
    """
    Checks the readiness of the SDNext server and exits with 0 if ready, 1 otherwise.
    """
    server_ready = get_sdnext_server_status()
    if not server_ready:
        sys.exit(1)
    model_loaded = get_sdnext_logs()
    if not model_loaded:
        sys.exit(1)
    sys.exit(0)


# Run the readiness check
check_readiness()
