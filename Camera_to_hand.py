import cv2  # used to access camera vision
import serial
import time
import mediapipe as mp

Mp_hands = mp.solutions.hands
Mp_drawing = mp.solutions.drawing_utils



webcam = cv2.VideoCapture(0)  # the number refers to whcib camera, 0 is built in 
if not webcam.isOpened():
    print(" Error: Could not open webcam.")
    exit()



while True:
    success, img = webcam.read()
    #convert OpenCV BGR (blue,red,green) into RBG for mediapipe to properly access
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

    #use the hand tracking on the frame: variable = function.function(minimum hands, min detection confidence)
    result = Mp_hands.Hands(max_num_hands=2 , min_detection_confidence = 0.5).process(img)

    #convert back to BGR to allow OpenCV to "draw" over image
    img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
    # connect the "landmarks" (these are teh joints) to form a skeleton hand
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            Mp_drawing.draw_landmarks(img, hand_landmarks, connections = Mp_hands.HAND_CONNECTIONS)


    cv2.imshow('Original Frame', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break  # pressing q breaks the loop anf allows for the next commands to run shutting it all down 
webcam.release()
cv2.destroyAllWindows()