import os
import time

import requests
from flask import Flask

app = Flask(__name__)

SITES = os.environ.get(
    "PULSE_SITES", "https://github.com,https://www.google.com"
).split(",")
TIMEOUT_SECONDS = 5


def check_site(url):
    start = time.monotonic()
    try:
        response = requests.get(url, timeout=TIMEOUT_SECONDS)
        elapsed_ms = round((time.monotonic() - start) * 1000)
        return {
            "url": url,
            "up": response.status_code < 400,
            "status_code": response.status_code,
            "response_time_ms": elapsed_ms,
        }
    except requests.RequestException as error:
        return {"url": url, "up": False, "error": type(error).__name__}


@app.route("/health")
def health():
    return {"status": "ok"}


@app.route("/status")
def status():
    return {"sites": [check_site(url.strip()) for url in SITES]}