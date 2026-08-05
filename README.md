# Distributed Selenium Automation Framework

A scalable, multi-instance automation framework built with Python and Selenium. This project is designed to run numerous isolated browser instances concurrently, each functioning as a separate "worker node" with its own proxy, session data, and digital footprint.

## Architecture

This system was engineered for **horizontal scaling and fingerprint isolation**. 
By compiling the core `worker.py` into an executable and deploying it across numbered sub-directories (e.g., Nodes 1 through 40), the system ensures strict isolation:
- **Session Isolation:** Each worker maintains its own local `profile` directory, ensuring cookies, cache, and local storage do not leak between instances.
- **Network Isolation:** Each node reads from its localized `config.json` to route traffic through independent proxies.
- **Executable Agnostic:** The code dynamically detects if it is running as a frozen executable (`sys.frozen`) or a Python script, dynamically adjusting its base path for configuration loading.

## Use Cases
- Distributed Web Scraping
- Load Testing
- Multi-Account Session Management
- Geo-Restricted Data Fetching via Proxy Rotation

## Setup & Deployment

1. **Configure the Node:**
   Rename `config.example.json` to `config.json` and input the proxy/credential details for the specific node.

2. **Isolate:**
   Place the script and the `config.json` in an isolated directory (e.g., `worker_01/`).

3. **Run:**
   Execute `python worker.py` (or the compiled `.exe`). The script will automatically generate a `profile` directory and log all activities to `logs.txt` within that node's folder.