# Running rosie_app with Docker

This guide explains how to run the `rosie_app` using Docker. This is useful for running the application in a sandboxed environment without having to worry about dependencies.


## Prerequisites

*   You must have [Docker](https://docs.docker.com/get-docker/) installed on your system.
*   You must be on a Linux system with an X11 display server. This has not been tested thorougly on a mac on windows system.
*   You need a rgb camera (a standard webcam will likely work) connected to your computer.

## Running the Application

Follow these steps to run the application.

### 1. Pull the Docker Image

First, pull the latest `rosie-app` image from Docker Hub:

```bash
docker pull signumtech/rosie-app
```
By default, this will pull the `latest` tag.


### 2. Run the Docker Container

Now you can run the application using the following command. This command gives the container access to your display and your camera.

```bash
docker run -it --privileged --device /dev/video0 signumtech/rosie-app
```

The application window should now appear on your screen.

### Command Breakdown

Here is a brief explanation of the `docker run` command flags used:

*   `-it`: Runs the container in interactive mode and allocates a pseudo-TTY.
*   `--privileged`: Gives the container full access to host devices. This is used to grant access to the camera and display without configuring each one individually.
*   `--device /dev/video0`: This gives the container access to your primary webcam. If you have multiple cameras, it might be located at `/dev/video1` or higher. You can check available video devices with `ls /dev/video*`.
*   `signumtech/rosie-app`: The name of the image to run.

## Security Note

The `--privileged` flag gives the container the same access to the system as the user running the command. Only use it with images you trust.
