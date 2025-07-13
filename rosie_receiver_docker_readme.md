# Rosie Receiver Docker Image

This document provides instructions on how to run the Rosie Receiver application using the pre-built Docker image from Docker Hub.

## Prerequisites

- Docker is installed on your system.
- You are on a Linux system with an X server (e.g., a standard desktop environment).

## Easy Run with Make

For convenience, a `Makefile` is provided which simplifies running the application. To pull the latest image, configure display access, and run the container, you can just run:

```bash
make run_rosie_receiver_docker
```

This single command will execute all the necessary steps for you.

For more granular control, or if you prefer to run the commands manually, follow the steps below.

## Running the Application

1.  **Pull the Docker Image**

    Open a terminal and pull the latest image from Docker Hub:
    ```bash
    docker pull signumtech/rosie_receiver:latest
    ```

2.  **Allow Docker to Access Your X Server**

    The Rosie Receiver has a graphical user interface (GUI). For the GUI to display on your host machine from within the Docker container, you need to grant the container access to your X server.

    Run the following command in your terminal:
    ```bash
    xhost +local:root
    ```
    This command allows local connections from the root user (which is the user inside the container) to the X server.

3.  **Run the Rosie Receiver Container**

    Now, run the application using the following command:

    ```bash
    docker run --rm -it --privileged \
        -e DISPLAY=$DISPLAY \
        -v /tmp/.X11-unix:/tmp/.X11-unix \
        signumtech/rosie_receiver:latest
    ```

    Let's break down this command:
    - `--rm`: Automatically removes the container when it exits.
    - `-it`: Runs the container in interactive mode and allocates a pseudo-TTY.
    - `--privileged`: This is required for the application to access necessary hardware devices.
    - `-e DISPLAY=$DISPLAY`: Passes your host's display environment variable to the container, so it knows where to open the GUI.
    - `-v /tmp/.X11-unix:/tmp/.X11-unix`: Mounts the X11 socket from your host into the container, allowing GUI applications to run.

    The Rosie Receiver GUI should now appear on your screen.

## Troubleshooting

- If the GUI does not appear, make sure you have executed the `xhost +local:root` command successfully.
- Ensure that the `DISPLAY` environment variable is set correctly on your host system. You can check it by running `echo $DISPLAY`.
