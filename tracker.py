import math


class Tracker:
    def __init__(self):
        # จัดเก็บตำแหน่งกึ่งกลางของวัตถุ
        self.center_points = {}
        #เก็บจำนวนไอดี
        # ทุกครั้งที่ตรวจพบรหัสวัตถุใหม่ จำนวนจะเพิ่มขึ้นทีละหนึ่ง
        self.id_count = 0


    def update(self, objects_rect):
        # กล่องวัตถุและรหัส
        objects_bbs_ids = []

        # รับจุดศูนย์กลางของวัตถุใหม่
        # คือ การวนลูปทุกวัตถุที่ส่งเข้ามาในตัวแปร objects_rect และกำหนดตัวแปร x, y, w, h, name, conff โดยให้ค่าแต่ละตัวแปร คือ พิกัด x และ y ของกล่องวัตถุ, ความกว้างของกล่องวัตถุ, ความสูงของกล่องวัตถุ, ชื่อของวัตถุ, และค่าความแม่นยำของการตรวจจับวัตถุ แล้วคำนวณตำแหน่งกึ่งกลางของวัตถุด้วยการ (x + x + w) // 2 และ (y + y + h) // 2 เพื่อไว้ใช้ในการเปรียบเทียบกับตำแหน่งกึ่งกลางของวัตถุที่ตรวจพบไปแล้ว.
        for rect in objects_rect:
            x, y, w, h ,name,conff = rect
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2

            # ค้นหาว่าตรวจพบวัตถุนั้นแล้วหรือไม่
            same_object_detected = False
            for id, pt in self.center_points.items():
                dist = math.hypot(cx - pt[0], cy - pt[1])
            # นี่คือส่วนของโปรแกรมที่ใช้ในการตรวจสอบว่าตรวจพบวัตถุที่เหมือนกันหรือไม่ โดยจะคำนวณระยะห่างระหว่างจุดกึ่งกลางของวัตถุใหม่ (cx, cy) และจุดกึ่งกลางของวัตถุเก่าในอาร์เรย์ self.center_points ว่าต่ำกว่า 35 หรือไม่ ถ้าใช่ โปรแกรมจะนำ ID ของวัตถุเก่านั้นไปใช้ในการปรับปรุงข้อมูลใน self.center_points และเพิ่มข้อมูลลงใน objects_bbs_ids และตั้งค่า same_object_detected เป็น True และให้ออกจากลูป for เพื่อไม่ต้องคำนวณระยะห่างอีก
                if dist < 40:
                    self.center_points[id] = (cx, cy)
#                    print(self.center_points)
                    objects_bbs_ids.append([x, y, w, h, id ,name,conff])
                    same_object_detected = True
                    break
           

            # ถ้าตรวจพบวัตถุใหม่ เราจะกำหนด ID ให้กับวัตถุนั้น
            # if same_object_detected is False: แปลว่า ถ้าไม่ได้ตรวจพบวัตถุนั้นแล้ว ให้ทำการเก็บข้อมูลตำแหน่งของวัตถุใหม่ใน self.center_points โดยใช้ค่า id ของวัตถุนั้น เป็น key และเก็บค่าตำแหน่ง (cx, cy) เป็น value และเพิ่มเลข id ใน self.id_count โดย 1 และเพิ่มข้อมูล [x, y, w, h, self.id_count ,name,conff] ใน objects_bbs_ids เพื่อใช้ในการแสดงผล
            if same_object_detected is False:
                self.center_points[self.id_count] = (cx, cy)
                objects_bbs_ids.append([x, y, w, h, self.id_count ,name,conff])
                self.id_count += 1

        # Clean the dictionary by center points to remove IDS not used anymore
        # ส่วนนี้คือการสร้าง dictionary ใหม่ที่เก็บข้อมูลของจุดศูนย์กลางของวัตถุที่ตรวจพบ โดยรับค่า objects_bbs_ids ที่เป็นรายการที่เก็บข้อมูลของวัตถุที่ตรวจพบ และในลูป for จะเอาค่า object_id จาก obj_bb_id และดึงค่า center จาก self.center_points ที่เก็บไว้ แล้วเก็บค่าใน new_center_points โดยใช้ object_id เป็น key เพื่อให้สามารถเรียกใช้ค่าได้ในภายหลัง.
        new_center_points = {}
        for obj_bb_id in objects_bbs_ids:
            _, _, _, _, object_id , _ ,_ = obj_bb_id
            center = self.center_points[object_id]
            new_center_points[object_id] = center

        # Update dictionary with IDs not used removed
        # คำสั่งนี้จะคัดลอกค่าจาก new_center_points ไปเก็บไว้ใน self.center_points และส่งค่า objects_bbs_ids กลับไปในฟังก์ชันนั้น. โดย self.center_points เป็น dictionary ที่เก็บตำแหน่งของวัตถุที่ตรวจพบในปัจจุบัน, และ objects_bbs_ids เป็น list ที่เก็บข้อมูลต่างๆ ของวัตถุที่ตรวจพบ (เช่น ตำแหน่ง, ขนาด, รหัส id และชื่อวัตถุ)
        self.center_points = new_center_points.copy()
        return objects_bbs_ids