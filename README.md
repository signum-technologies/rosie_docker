# rosie_docker

This repository provides instructions and tools for running the Rosie ecosystem using Docker. The Rosie ecosystem consists of two main components:

1.  `rosie_app`: An application that connects to a camera to take real-time physiological measurements.
2.  `rosie_receiver`: An application that displays the measurements from `rosie_app`.

## Running the Rosie Measurement App (`rosie_app`)

The `rosie_app` runs in a Docker container and is responsible for capturing and processing video from a camera to generate health measurements.

For detailed instructions on how to pull the Docker image and run the application, please see the dedicated readme file:
[**`rosie_app` Docker Instructions](./rosie_app_docker_readme.md)**

## Viewing the Measurements

Once the `rosie_app` is running and generating measurements, you have two options for viewing them:

### 1. Using the Rosie Receiver GUI

The `rosie_receiver` is a graphical application that displays the measurements in a user-friendly interface. It also runs in a Docker container.

For detailed instructions on how to run the `rosie_receiver` GUI, please see its readme file:
[**`rosie_receiver` Docker Instructions](./rosie_receiver_docker_readme.md)**

### 2. Using the Terminal Monitor

This repository includes a terminal-based monitor that connects to the `rosie_app` and prints the measurements directly to your terminal. This is a lightweight alternative to the GUI.

#### Setup

Before running the monitor for the first time, you need to set up the Python environment. This command creates a virtual environment and installs the necessary dependencies from `requirements.txt`.

```bash
make terminal_monitor_setup
```

#### Running

After the one-time setup is complete, you can run the monitor with the following command:

```bash
make run_terminal_monitor
```

The monitor will connect to the `rosie_app` and begin displaying measurements. To stop the monitor, press `Ctrl+C`.

For more advanced usage, such as connecting to a `rosie_app` on a different IP address, see the [terminal monitor documentation](./terminal_monitor.md).
