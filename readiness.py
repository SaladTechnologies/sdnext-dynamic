import requests
import sys
import os

load_refiner = os.environ.get("LOAD_REFINER", "0") == "1"
host = "localhost"
port = os.environ.get("PORT", "7860")

image_gen_url = f"http://{host}:{port}"
ready_file = "/tmp/ready"


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
        url = f"{image_gen_url}/sdapi/v1/log?lines=30&clear=true"
        response = requests.get(url)
        if response.status_code == 200:
            logs = response.json()
            return any("Startup time:" in line for line in logs)
    except Exception:
        pass
    return False


def load_refiner_model():
    """
    Loads the refiner model.
    Returns:
        True if the model is loaded, False otherwise.
    """
    try:
        url = f"{image_gen_url}/sdapi/v1/options"
        response = requests.post(
            url, json={"sd_model_refiner": "sd_xl_refiner_1.0.safetensors"}
        )
        if response.status_code == 200:
            return True
    except Exception:
        pass
    return False


def check_readiness():
    """
    Checks the readiness of the SDNext server and exits with 0 if ready, 1 otherwise.
    """
    # Check if the readiness file already exists
    try:
        with open(ready_file, "r") as f:
            # If the file exists, the server is ready
            if f.read() == "ready":
                print("Server is ready.")
                sys.exit(0)
    except Exception:
        pass

    server_ready = get_sdnext_server_status()
    if not server_ready:
        sys.exit(1)
    print("Server is ready, waiting for model to load...")
    model_loaded = get_sdnext_logs()
    if not model_loaded:
        sys.exit(1)
    print("Model loaded.")
    if load_refiner:
        print("Loading refiner model...")
        refiner_loaded = load_refiner_model()
        if not refiner_loaded:
            sys.exit(1)
        print("Refiner model loaded.")
    try:
        # Create the readiness file
        with open(ready_file, "w") as f:
            f.write("ready")
        print("Server is ready.")
        sys.exit(0)
    except Exception as e:
        print(e)
        sys.exit(1)


# Run the readiness check
check_readiness()
