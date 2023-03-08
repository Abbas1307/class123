import cv2
import mediapipe as mp
from pynput.keyboard import Key,Controller
import math
from pynput.mouse import Button,Controller
import pyautogui


mouse=Controller()
pinch=False
cap = cv2.VideoCapture(0)
hand = mp.solutions.hands
drawing = mp.solutions.drawing_utils

hands_object = hand.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5,max_num_hands=1)
width=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
hieght=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(width,hieght)

screen_width,screen_hieght=pyautogui.size()
print(screen_width,screen_hieght)

def count_fingers(lst,image):
    count=0
    global pinch

    threshholdData=(lst.landmark[0].y*100-lst.landmark[9].y*100)/2
    #print(threshholdData)
    
    if (lst.landmark[5].y*100-lst.landmark[8].y*100)>threshholdData:
        count+=1
    if (lst.landmark[9].y*100-lst.landmark[12].y*100)>threshholdData:
        count+=1
    if (lst.landmark[13].y*100-lst.landmark[16].y*100)>threshholdData:
        count+=1
    if (lst.landmark[17].y*100-lst.landmark[20].y*100)>threshholdData:
        count+=1
    if (lst.landmark[5].x*100-lst.landmark[4].x*100)>6:
        count+=1

    finger_tip_x=int(lst.landmark[8].x*width)
    finger_tip_y=int(lst.landmark[8].y*hieght)

    thumb_tip_x=int(lst.landmark[4].x*width)
    thumb_tip_y=int(lst.landmark[4].y*hieght)

    cv2.line(image,(finger_tip_x,finger_tip_y),(thumb_tip_x,thumb_tip_y),(0,0,255),2,1)

    center_x=int((finger_tip_x+thumb_tip_x)/2)
    center_y=int((finger_tip_y+thumb_tip_y)/2)

    cv2.circle(image,(center_x,center_y),2,(0,0,0),2,2)

    #return count
#distance=math.squrt((x2-x1)**2+(y2-y1)**2)

    distance=math.sqrt(((thumb_tip_x-finger_tip_x)**2)+((thumb_tip_y-finger_tip_y)**2))
    #print(distance)

    print("mouse position: ",mouse.position,"tips center position: ",center_x,center_y)

    relative_mouse_x=(center_x/width)*screen_width
    relative_mouse_y=(center_y/hieght)*screen_hieght
    mouse.position=(relative_mouse_x,relative_mouse_y)

    if distance>40:
        if pinch==True:
            pinch=False
            mouse.release(Button.left)
    if distance<=40:
        if pinch==False:
            pinch=True
            mouse.press(Button.left)

while True:
    success, image = cap.read()
    image=cv2.flip(image,1)

    
    # Detect the Hands Landmarks 
    results = hands_object.process(cv2.cvtColor(image,cv2.COLOR_BGR2RGB))
    #print(results)

    if results.multi_hand_landmarks:
         hand_keyPoints=results.multi_hand_landmarks[0]
         #print(hand_keyPoints) 
         c=count_fingers(hand_keyPoints,image)
         cv2.putText(image,"Pinch: "+str(pinch),(200,100),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,0,255),2)
         drawing.draw_landmarks(image,hand_keyPoints,hand.HAND_CONNECTIONS)

    cv2.imshow("Media Controller", image)

    # Quit the window on pressing Sapcebar key
    key = cv2.waitKey(1)
    if key == 27:
        break

cv2.destroyAllWindows()