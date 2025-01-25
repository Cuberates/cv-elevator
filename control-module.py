import cv2 as cv
import mediapipe as mp
import time
import serial
import os
import keyboard

mp_hands = mp.solutions.hands
mp_draw  = mp.solutions.drawing_utils
hands    = mp_hands.Hands(False, 1, 1, 0.5, 0.5)

ser = serial.Serial('COM3', 2000000) # Change the PORT NUMBER and BAUD RATE if something goes wrong, but we doubt it will resolve your issues :D

def detectFloor(currentCoordinate, width, numFloor): # Works by dividing the screen into different sections and traversing through them, could've been faster but we are a lazy team.
    part = int(width/numFloor)
    for region in range(1, numFloor+1):
        if currentCoordinate <= part * region:
            return region
def rotateMotor(currentFloor, nextFloor): # This function converts the difference of any two floors into the motor's rotary directions. 
    delta_floor = nextFloor - currentFloor
    if delta_floor < 0:
        for x in range(-delta_floor):  
            ser.write(b'0')
            time.sleep(4.5)
    else:
        for x in range(delta_floor) : 
            ser.write(b'1')
            time.sleep(4.5)

def calibrate(): # Absolutely useless function, but at least it helped us debug the model.
    while True:
        try:
            if keyboard.is_pressed('w'):
                ser.write(b'2')
                print('Calibration success')
                time.sleep(0.001)
            elif keyboard.is_pressed('s'):
                ser.write(b'3')
                print('Calibration success')
                time.sleep(0.002)
        except: break

def main(webcam, width, height, _id, floorCount): # The magic begins here

    currentFloor, nextFloor, numFloor = 1, 1, floorCount
    capture = cv.VideoCapture(webcam)

    while True:
        success, img = capture.read()
        img = cv.resize(img, (width, height))
        
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        # Displaying the contours (for visual purposes)
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x*w), int(lm.y*h)
                    if id == _id:
                        cv.circle(img, (cx, cy), 30, (255, 0, 255), cv.FILLED)  
                mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)
        cv.imshow("Preview", img)

        # Scanning the hand digits
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x*w), int(lm.y*h)
                    
                    if id == _id:
                        print("ID=", _id, "Detected at", detectFloor(cx, w, numFloor))
                        # Computing the floor after locating the correct hand digit
                        for floor in range(1, numFloor+1):
                            if floor == detectFloor(cx, w, numFloor):
                                nextFloor = floor
                                print('Current Floor:', currentFloor)
                                print('Next Floor   :', nextFloor)
                                print('Rotation     :', nextFloor-currentFloor, '(cycles)')                           
                                print('')
                                rotateMotor(currentFloor, nextFloor)
                                currentFloor = nextFloor
                                break
        cv.waitKey(1)

main(0, 1280, 720, 8, 4)