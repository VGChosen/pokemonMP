import mediapipe as mp
import cv2
import time
import pydirectinput as pyc
cam = cv2.VideoCapture(1)
mpInitialise = mp.solutions.hands
mpHands = mpInitialise.Hands()
mpDraw = mp.solutions.drawing_utils
cTime = 0
pTime = 0
tip_ids = [4, 8, 12, 16, 20]
while True:
    success, frame = cam.read()
    fingers = []
    lm_list = []
    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = mpHands.process(frameRGB)
    if results.multi_hand_landmarks:
        for hand in results.multi_hand_landmarks:
            for id, lm in enumerate(hand.landmark):
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                mpDraw.draw_landmarks(frame, hand, mpInitialise.HAND_CONNECTIONS)
                lm_list.append([id, cx, cy])

    if results.multi_hand_landmarks:
        if lm_list[tip_ids[0]][1] > lm_list[tip_ids[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        for id in range(1, 5):
            if lm_list[tip_ids[id]][2] < lm_list[tip_ids[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        # Commmands
        match fingers:
            case [0, 1, 0, 0, 0]:
                print('up')
                pyc.press('up')

            case [0, 1, 1, 0, 0]:
                print('down')
                pyc.press('down')

            case [0, 1, 1, 1, 0]:
                print('left')
                pyc.press('left')

            case [0, 1, 1, 1, 1]:
                print('right')
                pyc.press('right')

            case [1, 0, 0, 0, 0]:
                print('x')
                pyc.press('x')

            case [1, 1, 0, 0, 0]:
                print('y')
                pyc.press('y')

            case [1, 0, 0, 0, 1]:
                print('Shift')
                pyc.press('shift')

            case [1, 1, 1, 1, 1]:
                print('Enter')
                pyc.press('enter')

    cTime = time.time()
    fps = (1/(cTime - pTime))
    pTime = cTime
    cv2.putText(frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 255), 3)
    cv2.imshow('Window', frame)


    if cv2.waitKey(750) & 0xFF == ord('q'):
        break
