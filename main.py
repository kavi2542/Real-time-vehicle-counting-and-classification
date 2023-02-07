import cv2
import torch
from tracker import *
import numpy as np
model = torch.hub.load('ultralytics/yolov5', 'yolov5l', pretrained=True)

cap=cv2.VideoCapture('Traffic.mp4')


def POINTS(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE :  
        colorsBGR = [x, y]
        print(colorsBGR)
        

cv2.namedWindow('FRAME')
cv2.setMouseCallback('FRAME', POINTS)

tracker = Tracker()
#         มุมซ้ายล่าง   มุมขวาบน  มุมขวาล่าง   มุมซ้ายบน
area_1 = [(607,139),(819,183),(809,197),(578,156)]
# area_1 = [(607,139),(819,183),(809,197),(578,156)]

area1 =set()
area2 =set()
area3 =set()
area4 =set()
while True:
    ret,frame=cap.read()
    frame=cv2.resize(frame,(1020,500))
    cv2.polylines(frame,[np.array(area_1,np.int32)],True,(0,255,0),3)
    results=model(frame)
    # frame=np.squeeze(result.render())
    list = []
    for index,row in results.pandas().xyxy[0].iterrows():
        name=row['name']
        conf = row['confidence']
        x1=int(row['xmin'])
        y1=int(row['ymin'])
        x2=int(row['xmax'])
        y2=int(row['ymax'])
        conff = round(conf, 2)
        clas = int(row['class'])
        if clas == 3 or clas == 2 or clas == 5 or clas == 7:
            list.append([x1,y1,x2,y2,name,conff])
    boxes_ids=tracker.update(list)
    for box_id in boxes_ids:
        x,y,w,h,id,name,conff=box_id
        cv2.rectangle(frame,(x,y),(w,h),(255, 0, 20),1)
        cv2.rectangle(frame,(x,y-20),(w,y),(255, 144, 30),-1)
        cv2.putText(frame,str(str(id)+':'+name+' '+str(conff)),(x,y-5),cv2.FONT_HERSHEY_DUPLEX,0.5,(255, 255, 255),1)
        cv2.circle(frame, (w, h), 4, (0, 255, 0), -1)
        #เช็คตําแหน่งจุด w,h ถ้าเป็น False จะได้ค่า -1 เมื่ออยู่ด้านนอก และ 1 เมื่ออยู่ด้านใน
        result=cv2.pointPolygonTest(np.array(area_1,np.int32),(int(w),int(h)),False)
        if result > 0:
            if name == 'motorcycle':
                area1.add(id)
                cv2.polylines(frame,[np.array(area_1,np.int32)],True,(0,0,255),3)
            elif name == 'car':
                area2.add(id)
                cv2.polylines(frame,[np.array(area_1,np.int32)],True,(0,0,255),3)
            elif name == 'truck':
                area3.add(id)
                cv2.polylines(frame,[np.array(area_1,np.int32)],True,(0,0,255),3)
            elif name == 'bus':
                area4.add(id)
                cv2.polylines(frame,[np.array(area_1,np.int32)],True,(0,0,255),3)
    countM = len(area1)
    countC = len(area2)
    countT = len(area3)
    countB = len(area4)
    countTotal = str(countM+countC+countT+countB)
    cv2.putText(frame,str('Bike : ' + str(countM)),(20,50),cv2.FONT_HERSHEY_PLAIN,1.5,(0,0,255),2)
    cv2.putText(frame,str('Car : ' + str(countC)),(20,80),cv2.FONT_HERSHEY_PLAIN,1.5,(0,0,255),2)
    cv2.putText(frame,str('Truck : ' +str(countT)),(20,110),cv2.FONT_HERSHEY_PLAIN,1.5,(0,0,255),2)
    cv2.putText(frame,str('Bus : ' + str(countB)),(20,140),cv2.FONT_HERSHEY_PLAIN,1.5,(0,0,255),2)
    cv2.putText(frame,str('Total : ' +str(countTotal)),(20,170),cv2.FONT_HERSHEY_PLAIN,1.5,(0,0,255),2)
    cv2.imshow('FRAME',frame)
    if cv2.waitKey(1)&0xFF==27:
        break
cap.release()
cv2.destroyAllWindows()
    
    
