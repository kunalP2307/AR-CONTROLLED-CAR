from module import HandDetector
import cv2
import math
import time
import pygame
import serial

Arduino = serial.Serial(port='COM3  ', baudrate=9600)

class Timer:
    def _init_(self, time_between=5):
        self.start_time = time.time()
        self.time_between = time_between

    def can_send(self):
        if time.time() > (self.start_time + self.time_between):
            self.start_time = time.time()
            return True
        return False

def cvimage_to_pygame(image):
    return pygame.image.frombuffer(image.tostring(), image.shape[1::-1], "RGB")

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=2, minTrackCon=0.6, detectionCon=0.6)

width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

SCREEN = pygame.display.set_mode((int(width), int(height)))

wheel = pygame.image.load('wheel.png')

REVERSE = False
orientation = "Forward"

timer  = Timer(time_between=5)

Running = True
while Running:
    flag = False
    success, img = cap.read()
    hands = detector.findHands(img, draw=False)

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Running = False


    if len(hands) == 1:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        print(fingers)
        if fingers == [1, 1, 1, 1, 1]:
            if timer.can_send():
                REVERSE = not REVERSE

    elif len(hands) == 2:
        flag = True
        hand1 = hands[0]
        hand2 = hands[1]
        centerPoint1 = hand1['center']
        centerPoint2 = hand2['center']

        x1, y1 = centerPoint1
        x2, y2 = centerPoint2

        stearing_center = (int((x1 + x2)/2), int((y2 + y1)/2)) 
        distance = int(math.hypot(x2 - x1, y2 - y1)/2)

        if REVERSE == True:
            orientation = "REVERSE"
        else:
            orientation = "FORWARD"
        command = orientation
        try:
            slope = (y2 - y1) / (x2 - x1)
            if slope > 1:

                # print("Go LEFT")
                command += " GO LEFT\n"
                # Arduino.write(b"Left\n")
    
            elif slope < -1:
                # print("GO RIGHT")
                command += " GO RIGHT\n"
                # Arduino.write(b"Right\n")
            else:
                # print("Forward")
                command += " GO STRAIGHT\n"
                # Arduino.write(b"Forward\n")
        except:
            pass
    else:
        # print("Stop")
        command = "STOP\n"
        # Arduino.write(b"Stop\n")

    Arduino.write(bytes(command, 'utf-8'))
    print(command.strip())
    
    img = cv2.flip(img, 1)
    cv2.putText(img=img, text=str(orientation), org=(10, 20), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(0, 255, 0),thickness=3)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cvimage_to_pygame(img)
    SCREEN.blit(img, (0, 0))
    if flag:
        wheel1 =  pygame.transform.scale(wheel, (distance*2, distance*2))
        x, y = stearing_center
        x -= distance
        y -= distance
        x = width - x - (distance*2)
        wheel1 = pygame.transform.rotate(wheel1, math.degrees(math.atan(slope)))
        SCREEN.blit(wheel1, (x, y))
    pygame.display.update()

pygame.quit()
cap.release()