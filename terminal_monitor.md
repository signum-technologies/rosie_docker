# Health Pod Terminal Monitor

This document provides instructions on how to set up and run the terminal-based health monitor for the Health Pod. This monitor connects to the backend service and prints real-time health measurements (Heart Rate, Respiratory Rate) to the terminal.

## Setup

The setup process involves creating a Python virtual environment and installing the necessary dependencies. A virtual environment is a self-contained directory that holds a specific Python interpreter and its own set of libraries, preventing conflicts with other projects or the system's global packages.

### Prerequisites

- You must have Python 3 installed on your system.

### Instructions

You can set up the environment using a single `make` command or by running the steps manually.

#### Using `make`

To set up the terminal monitor, run the following command in your terminal:

```bash
make terminal_monitor_setup
```

This command will:
1.  Create a Python virtual environment in a folder named `.venv`.
2.  Activate the environment.
3.  Install the required Python packages from `requirements.txt`.

#### Manual Setup

If you prefer to set up the environment manually, follow these steps:

1.  **Create the virtual environment:**
    ```bash
    python3 -m venv .venv
    ```

2.  **Activate the virtual environment:**
    - On macOS and Linux:
      ```bash
      source .venv/bin/activate
      ```
    - On Windows:
      ```bash
      .\.venv\Scripts\activate
      ```
    Your terminal prompt should change to indicate that you are now in the `.venv` environment.

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Running the Monitor

Once the setup is complete, you can run the terminal monitor.

### Using `make`

To run the monitor with the default configuration (connecting to `127.0.0.1:27182`), use:

```bash
make run_terminal_monitor
```

### Manual Execution

If you set up the environment manually, make sure the virtual environment is still active. If not, reactivate it using the command from the setup step.

Then, run the script with:

```bash
python terminal_monitor.py
```

#### Custom IP and Port

The monitor connects to a backend server. By default, it attempts to connect to `127.0.0.1` on port `27182`. You can specify a different IP address and port using the `--ip` and `--port` flags:

```bash
python terminal_monitor.py --ip <backend_ip_address> --port <backend_port>
```
For example:
```bash
python terminal_monitor.py --ip 192.168.1.100 --port 8080
```

## Stopping the Monitor

To stop the monitor, press `Ctrl+C` in the terminal where it is running. The application will perform a graceful shutdown.
