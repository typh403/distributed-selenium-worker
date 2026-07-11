# Isolated Selenium Worker Node (Template)

A Python/Selenium worker template designed to run as many **independent, isolated browser instances**, each with its own proxy, Chrome profile and config. Every node is a self-contained folder (or compiled `.exe`), so isolation is achieved at the **process/directory level** rather than inside a single codebase.

> **Status:** working skeleton / template. The isolation and configuration layer is implemented. The actual task logic is intentionally left as a placeholder (see [Limitations](#known-limitations)).

- Developed: `[07/11/26]`
- Published on GitHub: `[09/28/26]`

## Design Idea

Instead of one program juggling many sessions, the same small worker is copied into numbered folders (`worker_01/`, `worker_02/`, ... up to any number of nodes). Each copy is fully independent:

| Concern | How it is isolated |
|---|---|
| Session data | Each node creates its own local `profile/` directory (cookies, cache, local storage never mix) |
| Network | Each node reads its own `config.json` and routes traffic through its own proxy |
| Logging | Each node writes to its own `logs.txt` |
| Deployment | `worker.py` detects if it is a frozen executable (`sys.frozen`) or a plain script and resolves its base path accordingly, so the same code works as `.py` or compiled `.exe` |

This is a "process-per-worker" pattern: no shared state, so nodes cannot interfere with each other and the number of workers scales by adding folders.

## What It Does Today

1. Loads `config.json` from the node's own directory.
2. Logs the node's task name, proxy and username to console and `logs.txt`.
3. Launches Chrome with the node's proxy and a dedicated `--user-data-dir`.
4. Opens an IP-check page so you can verify the proxy is applied.
5. **Waits for manual input** (`input()`), keeping the browser open for you to interact with it.

Because of step 5 the project is **semi-automated**: the framework brings up isolated, correctly configured browser sessions; what you do inside them is up to you (or your own automation code).

## Configuration

Copy `config.example.json` to `config.json` in the node's folder:

| Field | Used? | Description |
|---|---|---|
| `channel_name` | Logged | Label for the node/task |
| `proxy` | Yes | `host:port` proxy for this node |
| `username` | Logged only | Not yet wired to any authentication logic |

## Setup

```bash
pip install selenium
```

1. Create a folder for the node, e.g. `worker_01/`.
2. Put `worker.py` and `config.json` inside it.
3. Run `python worker.py` (or the compiled `.exe`).

A `profile/` folder and `logs.txt` are created automatically next to the script. Repeat with a new folder for each additional node.

## Known Limitations

- **No task logic:** the automation step is a placeholder; the script only opens an IP-check page and waits.
- **Blocking `input()`:** each node waits for a keypress, so nodes cannot yet run unattended or be terminated programmatically.
- **Proxy authentication:** only `host:port` proxies are supported. Chrome does not accept credentials through `--proxy-server`, and the `username` field is currently not used.
- **Minimal anti-detection:** a single Chrome flag (`--disable-blink-features=AutomationControlled`) is set. This is not a complete fingerprint-isolation solution.
- **No orchestration layer:** nodes are started individually; there is no launcher that spawns or monitors many nodes.
- **Procedural code:** a single `main()` function, no class structure yet.

## Roadmap

- [ ] Refactor into classes (`NodeConfig`, `BrowserSession`, `Worker`)
- [ ] Pluggable task modules so each node can run a different job
- [ ] Headless mode and clean programmatic shutdown (remove `input()`)
- [ ] Authenticated proxy support
- [ ] Simple launcher to start/monitor multiple nodes

## Responsible Use

Use this only on systems and accounts you own or are authorized to test, and follow the terms of service of any site you access.

## Development Notes

Architecture and design decisions are mine. `[Adjust to the truth: describe exactly how much of worker.py and this README was AI-assisted.]`