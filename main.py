import mediapipe as mp
import cv2
import tkinter as tk
import numpy as np
import time
import math
from fruitNinja import *

class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y

def processImg(frame, width, height, pose):
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = cv2.flip(image, 1)
    image = cv2.resize(image, (width, height), interpolation=cv2.INTER_LINEAR)
    results = pose.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    return image,results

def getDeltaTime(prevTime):
    currentTime = time.time()
    deltaTime = currentTime-prevTime
    return deltaTime,currentTime

def getDistance(prevPos, currPos):
    deltaX = (prevPos.x-currPos.x)**2
    deltaY = (prevPos.y-currPos.y)**2
    return math.sqrt(deltaX+deltaY), currPos

def main():
    root = tk.Tk() 
    scrWidth = root.winfo_screenwidth()
    scrHeight = root.winfo_screenheight()
    root.destroy()

    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)
    mp_drawing = mp.solutions.drawing_utils

    cv2.namedWindow("image", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty("image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    canvas = np.zeros((scrHeight, scrWidth, 3), dtype=np.uint8)

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, 20)

    if not cap.isOpened():
        exit()
    _, iniFrame = cap.read()

    imgHeight, imgWidth , _ = iniFrame.shape
    width = min(scrWidth, (int)(imgWidth/imgHeight*scrHeight))
    height = min(scrHeight, (int)(imgHeight/imgWidth*scrWidth))

    xOffset = (scrWidth-width)//2
    yOffset = (scrHeight-height)//2


    prevTime = 0
    
    prevPosLeft = lambda: None
    prevPosLeft.x = prevPosLeft.y = 0
    posLeft = lambda: None
    posLeft.x = posLeft.y = 0
    velocityLeft = 0

    prevPosRight = lambda: None
    prevPosRight.x = prevPosRight.y = 0
    posRight = lambda: None
    posRight.x = posRight.y = 0
    velocityRight = 0

    elements = []
    score = 0
    lives = 5

    while cap.isOpened():
        cv2.setWindowProperty("image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        ret, frame = cap.read()
        if not ret:
            break

        image,results = processImg(frame,width,height,pose)

        deltaTime, prevTime = getDeltaTime(prevTime)


        if results.pose_landmarks:
            resultLeft = results.pose_landmarks.landmark[20]
            posLeft = Point((int)(resultLeft.x*width), (int)(resultLeft.y*height))
            cv2.circle(image, (posLeft.x, posLeft.y), 15, (255,0,0), cv2.FILLED)
            distanceLeft,prevPosLeft = getDistance(prevPosLeft, posLeft)
            velocityLeft = (distanceLeft/deltaTime)

            resultRight = results.pose_landmarks.landmark[19]
            posRight = Point((int)(resultRight.x*width), (int)(resultRight.y*height))
            cv2.circle(image, (posRight.x, posRight.y), 15, (0,255,0), cv2.FILLED)
            distanceRight,prevPosRight = getDistance(prevPosRight, posRight)
            velocityRight = (distanceRight/deltaTime)

            cv2.putText(image, "score: "+str(score), (10, 50), cv2.FONT_HERSHEY_PLAIN, 5, (0,0,0), 3)
            cv2.putText(image, "lives: "+str(lives), (10, 150), cv2.FONT_HERSHEY_PLAIN, 5, (0,0,0), 3)


        elements, score, lives = fruitNinja(image, width, height, 
                                            elements, score, lives,
                                            posLeft, velocityLeft, 
                                            posRight, velocityRight)



        canvas[yOffset:yOffset + height, xOffset:xOffset + width] = image
        cv2.imshow("image", canvas)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()