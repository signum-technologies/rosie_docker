# Running Rosie with Docker

This guide provides easy-to-follow instructions for running the `rosie_app` and `rosie_receiver` applications together using Docker. This setup allows the two components to communicate with each other, with `rosie_app` processing video streams and `rosie_receiver` displaying the output.

These instructions are designed for users who may not have much experience with Docker.

## Prerequisites

Before you begin, please make sure you have the following:

1.  **Docker Installed:** Docker must be installed and running on your computer. You can find installation instructions on the [official Docker website](https://docs.docker.com/get-docker/).
2.  **A Terminal:** You will need to use a command-line terminal. On Linux or macOS, you can use the built-in Terminal app. On Windows, you can use PowerShell or WSL.
3.  **Linux Desktop:** The `rosie_receiver` application has a graphical user interface (GUI). These instructions are intended for a Linux desktop environment (like Ubuntu) where the GUI can be displayed.
4.  **Camera:** A webcam connected to your computer, accessible as `/dev/video0`.

## Step 1: Build the Docker Images

First, we need to build the Docker images for both applications. An image is like a blueprint for our application.

1.  **Build `rosie_app`:**
    *   Open your terminal and, from this `rosie_docker` directory, navigate to the `rosie_app` folder:
        ```bash
        cd ../rosie_app
        ```
    *   Build the image. This might take a few minutes.
        ```bash
        docker build -t rosie-app .
        ```

2.  **Build `rosie_receiver`:**
    *   Now, navigate to the `rosie_receiver` folder:
        ```bash
        cd ../rosie_receiver
        ```
    *   Build the `rosie_receiver` image:
        ```bash
        docker build -t rosie-receiver .
        ```
    *   Finally, return to the `rosie_docker` directory to continue:
        ```bash
        cd ../rosie_docker
        ```

## Step 2: Create a Docker Network

For the two applications to talk to each other, they need to be on the same virtual network. Let's create one.

*   In your terminal, run this command:
    ```bash
    docker network create rosie-net
    ```

## Step 3: Run the `rosie_app` Container

Now we'll start the `rosie_app`, which is the backend that processes the camera feed.

*   This command will run the app in the background, connect it to your camera, and make it available on the network we just created.
    ```bash
    docker run -d --rm \
      --name rosie-app \
      --network rosie-net \
      --privileged \
      --device /dev/video0:/dev/video0 \
      -p 5001:5001 \
      rosie-app
    ```
You can check if it's running with `docker ps`. You should see `rosie-app` in the list.

## Step 4: Run the `rosie_receiver` Container

Next, we'll run `rosie_receiver`, the user interface that displays the results from `rosie_app`.

1.  **Allow Display Access:** First, you need to give Docker permission to display a window on your desktop.
    ```bash
    xhost +local:docker
    ```
    This command allows containers to connect to your screen.

2.  **Run the container:** Now, run the `rosie_receiver`. It will connect to the `rosie-app` we started in the previous step.
    ```bash
    docker run --rm -it \
      --network rosie-net \
      -e DISPLAY=$DISPLAY \
      -e rosie_publisher_url=http://rosie-app:5001 \
      -v /tmp/.X11-unix:/tmp/.X11-unix \
      rosie-receiver
    ```
A window for the `rosie_receiver` application should appear on your screen.

## Step 5: Stopping the Applications

When you are finished, you can stop the applications.

1.  **Stop `rosie_receiver`:** In the terminal where `rosie_receiver` is running, press `Ctrl+C`. The container will stop and be removed automatically.

2.  **Stop `rosie_app`:** The `rosie_app` is running in the background. Stop it using this command:
    ```bash
    docker stop rosie-app
    ```
    Because we used the `--rm` flag, the container will also be removed automatically after it stops.
