import os
import requests

port = os.environ.get("PORT", "7860")

r = requests.get(
    f"http://localhost:{port}/sdapi/v1/system-info/status?full=true&refresh=true"
)

if r.status_code != 200:
    exit(-1)

response = r.json()

freeVram = response["memory"]["gpu"]["free"]
freeRam = response["memory"]["ram"]["free"]
oom = response["memory"]["events"]["oom"]
retries = response["memory"]["events"]["retries"]

vramLimit = 0.25
ramLimit = 0.5

if (freeVram < vramLimit) or (freeRam < ramLimit) or (oom >= 1) or (retries >= 1):
    print(
        f"Bad. FreeVRAM: {freeVram}<{vramLimit}, FreeRAM: {freeRam}<{ramLimit}, OOM: {oom}, Retries: {retries} "
    )
    exit(-1)

print("Ok")
exit(0)
