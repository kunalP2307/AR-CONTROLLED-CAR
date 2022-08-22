from module import HandDetector
import cv2
import math
import time



class Timer:
    def __init__(self, time_between=5):
        self.start_time = time.time()
        self.time_between = time_between

    def can_send(self):
        if time.time() > (self.start_time + self.time_between):
            self.start_time = time.time()
            return True
        return False


cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=2, minTrackCon=0.6, detectionCon=0.6)

width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

REVERSE = False
timer  = Timer(time_between=5)

while True:
    success, img = cap.read()
    hands = detector.findHands(img, draw=False)


    if len(hands) == 1:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        print(fingers)
        if fingers == [1, 1, 1, 1, 1]:
            if timer.can_send():
                REVERSE = not REVERSE

    if len(hands) == 2:
        hand1 = hands[0]
        hand2 = hands[1]
        centerPoint1 = hand1['center']
        centerPoint2 = hand2['center']

        x1, y1 = centerPoint1
        x2, y2 = centerPoint2

        cv2.circle(img, centerPoint1, 20, (255, 0, 255), thickness=-1)
        cv2.circle(img, centerPoint2, 20, (255, 0, 255), thickness=-1)
    
        cv2.line(img, centerPoint1, centerPoint2, (255, 0, 0), 5)
        stearing_center = (int((x1 + x2)/2), int((y2 + y1)/2)) 
        distance = int(math.hypot(x2 - x1, y2 - y1)/2)
        cv2.circle(img, stearing_center, distance, color=(255, 0, 0), thickness=10)

        try:
            slope = (y2 - y1) / (x2 - x1)
            if slope > 1:
                print(f"{REVERSE} GO LEFT")
            elif slope < -1:
                print(f"{REVERSE} GO RIGHT")
            else:
                print(f"{REVERSE} GO STRAIGT")
        except:
            pass
        
        if cv2.waitKey(5) & 0xFF == 27:
            break

    img = cv2.flip(img, 1)
    cv2.putText(img=img, text=str(REVERSE), org=(10, 20), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(0, 255, 0),thickness=3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)


cap.release()
cv2.destroyAllWindows()
