import cv2  # used to access camera vision
import mediapipe as mp
import numpy as np
import os
import uuid
import math


Mp_hands = mp.solutions.hands
Mp_drawing = mp.solutions.drawing_utils




def distance(a, b):
    return math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2 + (a.z - b.z)**2)

def finger_closed(hand_landmarks, tip_id, pip_id, wrist_id = 0):
    tip = hand_landmarks.landmark[tip_id]
    pip = hand_landmarks.landmark[pip_id]
    wrist = hand_landmarks.landmark[wrist_id]

    tip_dist = distance(tip, wrist)
    pip_dist = distance(pip, wrist)


    return tip_dist < pip_dist

def hand_closed(hand_landmarks):

    finger_tips = [4, 8, 12, 16, 20]   # thumb, index, middle, ring, pinky
    finger_pips = [3, 6, 10, 14, 18]   # corrected pip indices

    closed_count = 0
    for tip, pip in zip(finger_tips, finger_pips):
        if finger_closed(hand_landmarks, tip, pip):
            closed_count += 1  

    return closed_count == 5



webcam = cv2.VideoCapture(0)  # the number refers to whcib camera, 0 is built in 
if not webcam.isOpened():
    print(" Error: Could not open webcam.")
    exit()


with Mp_hands.Hands(max_num_hands=2 , min_detection_confidence = 0.8, min_tracking_confidence=0.5) as hands: 
    while webcam.isOpened():
        ret, frame = webcam.read()
        #convert OpenCV BGR (blue,red,green) into RBG for mediapipe to properly access
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

        frame.flags.writeable = False
        result = hands.process(frame)
        frame.flags.writeable = True
        

        #convert back to BGR to allow OpenCV to "draw" over image
        frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
 
        # connect the "landmarks" (these are teh joints) to form a skeleton hand
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
 
              
                Mp_drawing.draw_landmarks(frame, hand_landmarks, connections = Mp_hands.HAND_CONNECTIONS)
                for id, lm in enumerate(hand_landmarks.landmark):
                    h, w, c, = frame.shape
                    cx, cy = int(lm.x*w), int(lm.y*h)
                    
                    if hand_closed(hand_landmarks):
                        print("Hand is CLOSED")
                    else:
                        print("Hand is OPEN")

                   # print(f"ID: {id}, X: {cx}, y:{cy}")


        cv2.imshow('Original Frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break  # pressing q breaks the loop anf allows for the next commands to run shutting it all down 
webcam.release()
cv2.destroyAllWindows()