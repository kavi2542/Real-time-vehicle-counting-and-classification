import torch
import cv2
# import firebase_admin
import time
from datetime import datetime
# from firebase_admin import credentials
# from firebase_admin import firestore

# cred = credentials.Certificate("path/to/serviceAccountKey.json")
# firebase_admin.initialize_app(cred)

model = torch.hub.load('yolov5', 'yolov5l', source='local')

motorCount = 0
busCount = 0
carCount = 0
truckCount = 0
total = 0
cy1 = 350
offset = 12
count = 0

cap = cv2.VideoCapture('car44.mp4')

timeis = time.localtime()
time_start = time.strftime('%H:%M:%S', timeis)
time_start_firebase = time.strftime('%H%M%S', timeis)
day = time.strftime('%Y/%m/%d', timeis)
day_firebase = time.strftime('%d%m%Y', timeis)
d = time.strftime('%d', timeis)
m = time.strftime('%m', timeis)
Y = time.strftime('%Y', timeis)

while True:
    ret, img = cap.read()
    count += 1
    if count % 2 != 0:
        continue
    height, width = img.shape[0], img.shape[1]
    # print(height,width)
    # img = cv2.resize(img, (950, 540))
    # img = cv2.resize(img, (640, 360))
    curtime = datetime.now().time()
    ftime = curtime.strftime('%H:%M:%S')
    H = curtime.strftime('%H')
    M = curtime.strftime('%M')
    S = curtime.strftime('%S')

    cv2.putText(img, 'Car Count: ', (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(img, 'Motor Count: ', (10, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(img, 'Bus Count: ', (10, 110),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(img, 'Truck Count: ', (10, 140),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(img, 'Count Total: ', (10, 170),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(img, "TIME : "+str(ftime), (550, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.line(img, (100, cy1), (800, cy1), (0, 255, 255), 3)
    blur = cv2.blur(img,(3,3))
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    
#     img=cv2.resize(img,(600,500))
    detection = model(gray)
    results = detection.pandas().xyxy[0].to_dict(orient="records")
    for result in results:
        conf = result['confidence']
        name = result['name']
        clas = result['class']
        conff = "{}%".format(round(conf * 100 , 2))
        text = name + ' ' + str(conff)
        
        if clas == 2 or clas == 3 or clas == 5 or clas == 7:
                        x1 = int(result['xmin'])  # มุมบนซ้าย
                        y1 = int(result['ymin'])  # มุมบนซ้าย
                        x2 = int(result['xmax'])  # มุมล่างขวา
                        y2 = int(result['ymax'])  # มุมล่างขวา
                        cx = int((x1+x2)/2)
                        cy = int((y1+y2)/2)


                        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 191, 255), 1)
                        cv2.circle(img, (cx, cy), 3, (0, 0, 255), 7, -1)
                        cv2.putText(img, text, (x1+3, y1-10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (60, 255, 255), 2)
                
                        if cy < (cy1+offset) and cy > (cy1-offset):
                           if clas == 2:
                                carCount +=1
                                cv2.line(img, (0, cy1),
                                        (width, cy1), (0, 0, 255), 3)
                                # time.sleep(0.1)
                        if cy < (cy1+offset) and cy >= (cy1-offset):
                             if clas == 3:
                                motorCount +=1
                                cv2.line(img, (0, cy1),
                                        (width, cy1), (0, 0, 255), 3)
                                # time.sleep(0.1)
                        if cy < (cy1+offset) and cy > (cy1-offset):
                              if clas == 5:
                                busCount +=1
                                cv2.line(img, (0, cy1),
                                        (width, cy1), (0, 0, 255), 3)
                                # time.sleep(0.1)
                        if cy < (cy1+offset) and cy > (cy1-offset):
                             if clas == 7:
                                truckCount +=1
                                cv2.line(img, (0, cy1),
                                        (width, cy1), (0, 0, 255), 3)

                        total = carCount+motorCount+busCount+truckCount
                        cv2.putText(img, str(carCount), (250, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                        cv2.putText(img, str(motorCount), (250, 80),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                        cv2.putText(img, str(busCount), (250, 110),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                        cv2.putText(img, str(truckCount), (250, 140),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                        cv2.putText(img, str(total), (250, 170),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv2.imshow('Video', img)
#     cv2.imshow('Test', blur)
    # cv2.imshow('Test2', gray)

    if cv2.waitKey(1) == 27:
        ftime
        break

# db = firestore.client()
# db.collection('project').document(day_firebase+':'+time_start_firebase).set({
#     'date':day,
#     'time_start':time_start,
#     'time_stop': ftime,
#     'Car':str(carCount),
#     'Motorcycle':str(motorCount),
#     'Bus':str(busCount),
#     'Truck':str(truckCount),
#     'Total':str(total)
#     })
print('Car : ', carCount)
print('Motorcycle : ', motorCount)
print('Bus : ', busCount)
print('Truck : ', truckCount)
print('ToTal : ', total)
# print(height, width);
cv2.destroyAllWindows()
cap.release()
