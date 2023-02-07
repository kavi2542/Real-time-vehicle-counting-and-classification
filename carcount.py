from PyQt5 import QtWidgets, uic, QtCore
import sys
import cv2
import torch
import firebase_admin
import time
import numpy as np
from tracker import *
from datetime import datetime
from PyQt5.QtCore import QTimer, QTime
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QFileDialog
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("path/to/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

timeis = time.localtime()
time_start = time.strftime("%H:%M:%S", timeis)
time_start_firebase = time.strftime("%H%M%S", timeis)
day = time.strftime("%Y/%m/%d", timeis)
day_firebase = time.strftime("%d%m%Y", timeis)
d = time.strftime("%d", timeis)
m = time.strftime("%m", timeis)
Y = time.strftime("%Y", timeis)

tracker = Tracker()
area1 =set()
area2 =set()
area3 =set()
area4 =set()
countM = 0;
countC = 0;
countT = 0;
countB = 0;
countTotal = 0;
class Car_Counting(QtWidgets.QMainWindow):
    def __init__(self):
        super(Car_Counting, self).__init__()
        uic.loadUi("hello.ui", self)
        self.ipBtn.clicked.connect(self.Add_IP)
        self.clearBtn.clicked.connect(self.clear_IP)
        self.Startbtn.clicked.connect(self.setVideo)
        self.submit.clicked.connect(self.setText)
        self.lineConbtn.clicked.connect(self.set_confiden)
        self.model = self.load_model();
        self.label.mouseMoveEvent = self.POINTS
        self.set_confiden(0.0);
        self.set_topleftX(0)
        self.set_topleftY(0)
        self.set_buttomleftX(0)
        self.set_buttomleftY(0)
        self.set_toprightX(0)
        self.set_toprightY(0)
        self.set_buttomrightX(0)
        self.set_buttomrightY(0)

        timer = QTimer(self)
        timer.timeout.connect(self.Time)
        timer.start(1000)
    
    def setText(self):
        topLeftX = self.xLinetop_left.text()
        topLeftY = self.yLinetop_left.text()
        buttomLeftX = self.xLinebuttom_left.text()
        buttomLeftY = self.yLinebuttom_left.text()
        topRightX = self.xLinetop_right.text()
        topRightY = self.yLinetop_right.text()
        buttomRightX = self.xLinebuttom_right.text()
        buttomRightY = self.yLinebuttom_right.text()
        
        # Setter
        if topLeftX == '' or topLeftY == '' or buttomLeftX == '' or buttomLeftY == '' or topRightX == '' or topRightY == '' or buttomRightX == '' or buttomRightY == '':
            QtWidgets.QMessageBox.information(
                QtWidgets.QMessageBox(), "Error", "กรุณาป้อนข้อมูลให้ครบ"
            )
        else:
            self.set_topleftX(topLeftX)
            self.set_topleftY(topLeftY)
            self.set_buttomleftX(buttomLeftX)
            self.set_buttomleftY(buttomLeftY)
            self.set_toprightX(topRightX)
            self.set_toprightY(topRightY)
            self.set_buttomrightX(buttomRightX)
            self.set_buttomrightY(buttomRightY)
        
        # Getter
        self.get_topleftX()
        self.get_topleftY()
        self.get_buttomleftX()
        self.get_buttomleftY()
        self.get_toprightX()
        self.get_toprightY()
        self.get_buttomrightX()
        self.get_buttomrightY()
        
    
    
    def POINTS(self, event):
        x = event.x()
        y = event.y()
        self.TextX.setText(str(x))
        self.TextY.setText(str(y))
    
    # confidest config
    def set_confiden(self, confident):
        confident = self.lineCon.text()
        if confident == '':
             QtWidgets.QMessageBox.information(
                QtWidgets.QMessageBox(), "Error", "กรุณาป้อนค่า Confident"
            )
        elif confident > str(1) and confident < str(0)  :
             QtWidgets.QMessageBox.information(
                QtWidgets.QMessageBox(), "Error", "กรุณาป้อนค่า Confident ให้อยู่ในช่วง 0.0 - 1"
            )
        else:
            self.con = confident
            print(self.con)

    def get_confiden(self):
        return self.con
    
    
    # topleftX
    def set_topleftX(self, topleftX):
        topleftX = self.xLinetop_left.text()
        self.topLeftX = topleftX
        print(self.topLeftX)

    def get_topleftX(self):
        return self.topLeftX
    
    
    # topleftY
    def set_topleftY(self, topleftY):
        topleftY = self.yLinetop_left.text()
        self.topLeftY = topleftY
        print(self.topLeftY)

    def get_topleftY(self):
        return self.topLeftY
    
    
    # buttomleftX
    def set_buttomleftX(self, buttomleftX):
        buttomleftX = self.xLinebuttom_left.text()
        self.buttomLeftX = buttomleftX
        print(self.buttomLeftX)

    def get_buttomleftX(self):
        return self.buttomLeftX
    
    # buttomleftY
    def set_buttomleftY(self, buttomleftY):
        buttomleftY = self.yLinebuttom_left.text()
        self.buttomLeftY = buttomleftY
        print(self.buttomLeftY)

    def get_buttomleftY(self):
        return self.buttomLeftY
    
    
    # toprightX
    def set_toprightX(self, toprightX):
        toprightX = self.xLinetop_right.text()
        self.topRightX = toprightX
        print(self.topRightX)

    def get_toprightX(self):
        return self.topRightX
    
    # toprightY
    def set_toprightY(self, toprightY):
        toprightY = self.yLinetop_right.text()
        self.topRightY = toprightY
        print(self.topRightY)

    def get_toprightY(self):
        return self.topRightY
    
    
    # buttomrightX
    def set_buttomrightX(self, buttomrightX):
        buttomrightX = self.xLinebuttom_right.text()
        self.buttomRightX = buttomrightX
        print(self.buttomRightX)

    def get_buttomrightX(self):
        return self.buttomRightX

    
    # buttomrightY
    def set_buttomrightY(self, buttomrightY):
        buttomrightY = self.yLinebuttom_right.text()
        self.buttomRightY = buttomrightY
        print(self.buttomRightY)

    def get_buttomrightY(self):
        return self.buttomRightY
    

    def Add_IP(self):
        ip = self.ipEdit.text()
        if ip == "":
            QtWidgets.QMessageBox.information(
                QtWidgets.QMessageBox(), "Error", "กรุณาป้อน IP URL"
            )
        else:
            print(ip)
            QtWidgets.QMessageBox.information(
                QtWidgets.QMessageBox(), "Welcome", "เชื่อมต่อ IP CAMERA สําเร็จ"
            )
            self.cap = cv2.VideoCapture(ip)
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.update_frame)
            framerate = 30
            rate = int(1000 / framerate)
            self.timer.start(rate)
            # timer01 = QTimer(self)
            # timer01.timeout.connect(self.UpdateFirebase)
            # timer01.start(5000)
            self.Startbtn.setEnabled(False)
            self.ipBtn.setEnabled(False)
            self.ipEdit.setEnabled(False)

    def clear_IP(self):
        self.ipEdit.clear()
        self.ipBtn.setEnabled(True)
        self.ipEdit.setEnabled(True)
        self.Startbtn.setEnabled(True)
        

    def setVideo(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Selecciona los mediose", ".", "Video Files (*.mp4 *.flv *.ts *.mts *.avi *.mov)",)
        print(filename)
        if filename != "":
            self.cap = cv2.VideoCapture(filename)
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.update_frame)
            framerate = 30
            rate = int(1000 / framerate)
            self.timer.start(rate)
            # timer01 = QTimer(self)
            # timer01.timeout.connect(self.UpdateFirebase)
            # timer01.start(5000)
            self.Startbtn.setEnabled(False)

    def load_model(self):
        model = torch.hub.load("yolov5",'custom', path="yolov5m.pt", source="local",device=0)
        return model

    def Time(self):
        current_time = QTime.currentTime()
        label_time = current_time.toString("hh:mm:ss")
        self.timeLabel.setText(label_time)
        self.end_time = label_time

    def get_endTime(self):
        return self.end_time

    def UpdateFirebase(self):
        endTime = self.get_endTime()
        db = firestore.client()
        db.collection("project").document(day_firebase + ":" + time_start_firebase).set(
            {
                "date": day,
                "time_start": time_start,
                "time_stop": endTime,
                "Car": str(countC),
                "Motorcycle": str(countM),
                "Bus": str(countB),
                "Truck": str(countT),
                "Total": str(countTotal),
            }
        )

    def update_frame(self):
        global countM
        global countC
        global countT
        global countB
        global countTotal
        topleftX = int(self.get_topleftX())
        topleftY = int(self.get_topleftY())
        buttomleftX = int(self.get_buttomleftX())
        buttomleftY = int(self.get_buttomleftY())
        toprightX = int(self.get_toprightX())
        toprightY = int(self.get_toprightY())
        buttomrightX = int(self.get_buttomrightX())
        buttomrightY = int(self.get_buttomrightY())
        confident = float(self.get_confiden())
        ret, img = self.cap.read()
        area_1 = [(buttomleftX,buttomleftY),(toprightX,toprightY),(buttomrightX,buttomrightY),(topleftX,topleftY)]
        if ret == True:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img,(640,360))
            height, width = img.shape[0], img.shape[1]
            cv2.polylines(img,[np.array(area_1,np.int32)],True,(0,255,0),2)
            results = self.model(img)
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
                if conff > confident:
                    if clas == 2 or clas == 3 or clas == 5 or clas == 7:
                        list.append([x1,y1,x2,y2,name,conff])
            boxes_ids=tracker.update(list)
            for box_id in boxes_ids:
                x,y,w,h,id,name,conff=box_id
                cv2.rectangle(img,(x,y),(w,h),(255, 0, 20),1)
                cv2.rectangle(img,(x,y-20),(w,y),(255, 144, 30),-1)
                cv2.putText(img,str(str(id)+':'+name+' '+str(conff)),(x,y-5),cv2.FONT_HERSHEY_DUPLEX,0.5,(255, 255, 255),1)
                cv2.circle(img, (w, h), 4, (0, 255, 0), -1)
                #เช็คตําแหน่งจุด w,h ถ้าเป็น False จะได้ค่า -1 เมื่ออยู่ด้านนอก และ 1 เมื่ออยู่ด้านใน
                result=cv2.pointPolygonTest(np.array(area_1,np.int32),(w,h),False)
                
                if result > 0:
                    if name == 'motorcycle':
                        area1.add(id)
                        cv2.polylines(img,[np.array(area_1,np.int32)],True,(0,0,255),3)
                    if name == 'car':
                        area2.add(id)
                        cv2.polylines(img,[np.array(area_1,np.int32)],True,(0,0,255),3)
                    if name == 'truck':
                        area3.add(id)
                        cv2.polylines(img,[np.array(area_1,np.int32)],True,(0,0,255),3)
                    if name == 'bus':
                        area4.add(id)
                        cv2.polylines(img,[np.array(area_1,np.int32)],True,(0,0,255),3)
            countM = len(area1)
            countC = len(area2)
            countT = len(area3)
            countB = len(area4)
            countTotal = str(countM+countC+countT+countB)
            self.carLabel.setText(str(countC))
            self.motorLabel.setText(str(countM))
            self.truckLabel.setText(str(countT))
            self.busLabel.setText(str(countB))
            self.totalLabel.setText(str(countTotal))
        img = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
        pix = QPixmap.fromImage(img)
        pix = pix.scaled(
                self.label.width(), self.label.height(), QtCore.Qt.KeepAspectRatio
            )
        self.label.setPixmap(pix)
        self.widthLabel.setText(str(width))
        self.heightLabel.setText(str(height))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Car_Counting()
    window.show()
    app.exec_()


