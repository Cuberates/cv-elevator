# CV-Elevator
Elevator powered by Computer Vision (CV) Technology (Prototype)

## About 
CV-Elevator is a model of a potentially useful application of OpenCV into developing smart elevator systems to ensure safety during the COVID19 pandemic. It works by scanning the user's hand via computer vision technology, and operating based on their selection. This minimises the need to touch the button themselves in selecting a floor, which was crucial in subsiding SARS-COV-2 infections. We have done a presentation on this in the RMIT TechGenius 2021 and the Ho Chi Minh City Science and Engineering Fair 2021. 

## Usage
The model was implemented in Python 3 using the help of MediaPipe and Pyserial, and it was ran on an Arduino UNO R3. 
Download the Arduino IDE from the main website and install the required frameworks for `control-module.py` via the following command: `pip3 install opencv-python mediapipe pyserial keyboard time os`
Connect your Arduino UNO R3 and configure the PORT and the BAUD RATE on the Arduino IDE. 
To run the project, do the following command: `python3 control-module.py`

Feel free to fork the project. 
MIT License applies. 
