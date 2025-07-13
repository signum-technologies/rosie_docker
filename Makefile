LATEST_PYTHON3 := $(shell (ls /usr/bin/python3.* 2>/dev/null | grep -E -o 'python3\\.[0-9]+' | uniq | sort -V | tail -n 1 | grep .) || echo python3)

.PHONY: setup terminal_monitor_setup run_terminal_monitor run_rosie_app_docker run_rosie_receiver_docker

# target to setup the terminal monitor
terminal_monitor_setup:
	@echo "Using python: $(LATEST_PYTHON3)"
	$(LATEST_PYTHON3) -m venv .venv
	./.venv/bin/pip install -r requirements.txt


# target to run the terminal monitor
run_terminal_monitor:
	./.venv/bin/python terminal_monitor.py --ip 127.0.0.1 --port 27182


# target to run the rosie app docker container
run_rosie_app_docker:
	docker pull signumtech/rosie-app
	docker run -it --privileged --device /dev/video0 signumtech/rosie-app


# target to run the rosie receiver docker container
run_rosie_receiver_docker:
	@echo "Pulling latest Rosie Receiver image..."
	docker pull signumtech/rosie_receiver:latest
	@echo "Configuring X server access for Docker (required for GUI)..."
	xhost +local:root
	@echo "Running Rosie Receiver container..."
	docker run --rm -it --privileged \
		-e DISPLAY=$(DISPLAY) \
		-v /tmp/.X11-unix:/tmp/.X11-unix \
		signumtech/rosie_receiver:latest