import cv2  # used to access camera vision
import mediapipe as mp
import numpy as np
import os
import uuid


Mp_hands = mp.solutions.hands
Mp_drawing = mp.solutions.drawing_utils


def is_finger_closed(tip, pip):
    return tip.y > pip.y

def hand_closed(hand_landmarks):
    finger_tips = [4, 8, 12, 16, 20]   # thumb, index, middle, ring, pinky
    finger_pips = [3, 6, 10, 14, 18]
    closed_count = 0
    for tip, pip in zip(finger_tips, finger_pips):
        if hand_landmarks.landmark[tip].y > hand_landmarks.landmark[pip].y:
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