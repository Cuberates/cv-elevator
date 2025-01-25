all: 
	pip3 install opencv-python mediapipe pyserial keyboard
	@echo "BUILD SUCCESSFUL!"
run: 
	python3 control-module.py
