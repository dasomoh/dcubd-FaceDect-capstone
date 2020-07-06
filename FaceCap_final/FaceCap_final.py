from tkinter import *
from tkinter import messagebox
import datetime
import random
import time
import cv2
import os
from PIL import Image
import numpy as np
import mysql.connector
from mtcnn.mtcnn import MTCNN
import sys
import pymysql

date = datetime.datetime.now().date()
date = str(date)

class Application(object):
    def __init__(self, master):
        self.master = master

        self.UserId = StringVar()
        self.Userpasswd = StringVar()
        self.name = StringVar()
        self.identi = StringVar()
        self.major = StringVar()
        
        # frame
        self.top = Frame(master, height=200, bg="white")
        self.top.pack(fill=X)
        
        #  bottom
        self.bottom = Frame(master, height=600, bg="#326fa8")
        self.bottom.pack(fill=X)
    
        self.heading = Label(self.top, text="얼굴 인식 출석 시스템 - 회원가입", 
                             font='arial 30 bold',
                             bg='white', fg='black')
        self.heading.place(x=180, y=75)
            
        # datetime 
        self.date_lbl = Label(self.top, text=date,
                             font='arial 15 bold', bg='white', fg='black')
        self.date_lbl.place(x=650, y=0)
        
        #=======================1:회원 가입 페이지 등 텍스트=======================
        self.bottom_title = Label(self.bottom, text='1 : 회원 가입 페이지',
                                 font='arial 30 bold', bg='#326fa8'
                                 ,fg='black')
        self.bottom_title.place(x=200, y=5) 
        
        self.bottom_title = Label(self.bottom, text='5가지 항목을 모두 입력해주세요.',
                                 font='arial 25 bold', bg='#326fa8'
                                 ,fg='black')
        self.bottom_title.place(x=125, y=60) 
        #===========================================================================
        #========================2: id, passwd 등등 회원가입========================
        self.l1 = Label(self.bottom, text='아이디', font='airal 15 bold')
        self.l1.place(x=100, y=135)
                                                    
        self.t1 = Entry(self.bottom, width=60, bd=4, textvariable=self.UserId)
        self.t1.insert(0, "아이디를 입력해주세요.")
        self.t1.place(x=200, y=135)
        
        self.l2 = Label(self.bottom, text='비밀번호', font='airal 15 bold')
        self.l2.place(x=100, y=190)
        
        self.t2 = Entry(self.bottom, width=60, bd=5, textvariable=self.Userpasswd)
        self.t2.insert(0, "비밀번호를 입력해주세요.")
        self.t2.place(x=200, y=190)
        
        self.l3 = Label(self.bottom, text='이름', font='airal 15 bold')
        self.l3.place(x=100, y=240)
        
        self.t3 = Entry(self.bottom, width=60, bd=5, textvariable=self.name)
        self.t3.insert(0, "이름을 영문으로 입력해주세요.")
        self.t3.place(x=200, y=240)
    
        self.l4 = Label(self.bottom, text='학번', font='airal 15 bold')
        self.l4.place(x=100, y=290)
        
        self.t4 = Entry(self.bottom, width=60, bd=5, textvariable=self.identi)
        self.t4.insert(0, "학번을 입력해주세요.")
        self.t4.place(x=200, y=290)   
        
        self.l5 = Label(self.bottom, text='학과', font='airal 15 bold')
        self.l5.place(x=100, y=340)
        
        self.t5 = Entry(self.bottom, width=60, bd=5, textvariable=self.major)
        self.t5.insert(0, "학과를 입력해주세요.")
        self.t5.place(x=200, y=340)   

        #============================================================================
        #==============================회원가입, 새로고침, 종료======================
        test = '회원가입\n&\n얼굴 데이터\n수집'
        
        self.btnSignUp = Button(self.bottom, text=test, height=4,
                               width = 10, font='arial 12 bold',
                               command=self.generate_dataset)
        self.btnSignUp.place(x=100, y=400)
        
        self.btnSignUp = Button(self.bottom, text='로그인\n페이지', height=4,
                               width = 10, font='arial 12 bold',
                               command=self.go_login)
        self.btnSignUp.place(x=250, y=400)
        
        self.btnReset = Button(self.bottom, text="새로고침", height=4,
                                font='arial 12 bold', width=10,
                                command=self.Reset)
        self.btnReset.place(x=400, y=400)
        
        self.btnExit = Button(self.bottom, text='종료', height =4,
                               width = 10, font='arial 12 bold',
                               command=self.iExit)
        self.btnExit.place(x=550, y=400)
    
    def generate_dataset(self):
        if(self.t1.get()=="" or self.t1.get() == "아이디를 입력해주세요." or self.t2.get()=="" or self.t3.get()=="" or self.t4.get() =="" or self.t5.get() == ""):
            messagebox.showinfo('입력오류', '아이디, 비밀번호, 이름, 학번, 전공 5 가지 모두를 입력해주세요.')
            self.t1.focus()
        else:
            mydb = pymysql.connect(
                host="localhost",
                port=3306,
                user="root",
                passwd="root",
                db="dcu_member",
                charset='utf8'
            )
            mycursor = mydb.cursor()
            mycursor.execute("SELECT * FROM last_member")
            myresult = mycursor.fetchall()
            id = 1
            for x in myresult:
                id += 1
           
            sql = """
               INSERT INTO last_member(id, user_Id, user_passwd, user_name, student_id, student_major) 
               VALUES(%s, %s, %s, %s, %s, %s)
            """
            val = (id, self.t1.get(), self.t2.get(), self.t3.get(), self.t4.get(), self.t5.get())
            mycursor.execute(sql, val)
            mydb.commit()
            mydb.close()
            
            face_classifier = MTCNN()
            def face_cropped(img):
                cropped_face = None
                faces = face_classifier.detect_faces(img)

                if faces is ():
                    return None

                for face in faces:
                    x, y, w, h = face['box']
                    cropped_face = img[y:y+h, x:x+w]

                return cropped_face

            cap = cv2.VideoCapture(0, cv2.CAP_MSMF)

            img_id = 0

            while True:
                ret, frame = cap.read()
                if face_cropped(frame) is not None:
                    img_id += 1
                    face = cv2.resize(face_cropped(frame), (200, 200))
                    face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                    file_name_path = "data/user." + str(id) + "." + str(img_id) + ".jpg"
                    cv2.imwrite(file_name_path, face)
                    cv2.putText(face, str(img_id), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

                    cv2.imshow("Cropped face", face)
                    if cv2.waitKey(1) == 13 or int(img_id) == 20:
                        break
                        
            cap.release()
            cv2.destroyAllWindows()
            messagebox.showinfo('Reuslt', '데이터 수집을 성공했습니다.')
            people1 = Two()    
 
    def go_login(self):
        people = Two()
        
    def Reset(self):
        self.UserId.set("")
        self.Userpasswd.set("")
        self.name.set("")
        self.identi.set("")
        self.major.set("")
        self.t1.focus()
    
    def iExit(self):    
        self.iExit = messagebox.askyesno('로그인', "종료 하시겠습니까?")
        if self.iExit > 0:
            self.master.destroy()
        else:
            command = Application()
            return 
        
#============================MyPeople Class 즉 두 번째 클래스==============
class Two(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.UserId = StringVar()
        self.Userpasswd = StringVar()
        self.geometry("760x800+0+0")
        self.title('얼굴 인식 출석 시스템 - 로그인')
        self.resizable(False, False)
                # frame
        self.top = Frame(self, height=200, bg="white")
        self.top.pack(fill=X)
        
        #  bottom
        self.bottom = Frame(self, height=600, bg="#326fa8")
        self.bottom.pack(fill=X)
        

        self.heading = Label(self.top, text="얼굴 인식 출석 시스템", 
                             font='arial 30 bold',
                             bg='white', fg='black')
        self.heading.place(x=180, y=75)
            
        # datetime 
        self.date_lbl = Label(self.top, text=date,
                             font='arial 15 bold', bg='white', fg='black')
        self.date_lbl.place(x=650, y=0)
        
        #===============Login name, passwd Label and Entry======================
        self.bottom_title = Label(self.bottom, text='2 : 로그인 페이지',
                                 font='arial 30 bold', bg='#326fa8'
                                 ,fg='black')
        self.bottom_title.place(x=200, y=5) 
        
        self.bottom_title = Label(self.bottom, text='아이디와 비밀번호를 입력해주세요.',
                                 font='arial 25 bold', bg='#326fa8'
                                 ,fg='black')
        self.bottom_title.place(x=125, y=60) 
        #===========================================================================
        #========================2: id, passwd 등등 회원가입========================
        self.idl = Label(self.bottom, text='아이디', font='airal 15 bold')
        self.idl.place(x=100, y=175)
                                                    
        self.idt= Entry(self.bottom, width=55, bd=4, textvariable=self.UserId)
        self.idt.insert(0, "아이디를 입력해주세요.")
        self.idt.place(x=200, y=175)
        
        self.pdl = Label(self.bottom, text='비밀번호', font='airal 15 bold')
        self.pdl.place(x=100, y=250)
                                                    
        self.pdt= Entry(self.bottom, width=55, bd=4, textvariable=self.Userpasswd)
        self.pdt.insert(0, "비밀번호를 입력해주세요.")
        self.pdt.place(x=200, y=250)      


        
        btnadd = Button(self.bottom, text='로그인', height=4, width=12,
                        font='Sans 12 bold',
                        command=self.go_three)
        btnadd.place(x=100, y= 400)
        
        btnreset = Button(self.bottom, text='새로고침', height=4, width=12,
                           font='Sans 12 bold',
                           command=self.Reset)
        btnreset.place(x=300, y=400) 
        
        btnexit = Button(self.bottom, text='종료', height=4, width=12,
                           font='Sans 12 bold',
                           command=self.iExit)
        btnexit.place(x=500, y=400) 
    
#     def three_go(self):
#         people = Webcam()
    
    def Reset(self):
        self.UserId.set("")
        self.Userpasswd.set("")
        self.idt.focus()
    
    def iExit(self):    
        self.iExit = messagebox.askyesno('로그인', "종료 하시겠습니까?")
        if self.iExit > 0:
            self.master.destroy()
        else:
#             command = Two()
            self.idt.focus()
            return 
        
    def go_three(self):
        mydb = pymysql.connect(
            host="localhost",
            port=3306,
            user="root",
            passwd="root",
            db="dcu_member",
            charset='utf8'
        )
        mycursor = mydb.cursor()
        if(self.UserId.get()=="아이디를 입력해주세요." or self.Userpasswd.get()=="비밀번호를 입력해주세요."):
            messagebox.showinfo('입력오류', '아이디, 비밀번호 2 가지 모두를 입력해주세요.')
            self.idt.focus()
        else:
            sql = """
                SELECT user_name FROM last_member WHERE user_id=%s AND user_passwd=%s
            """
            val = (self.UserId.get(), self.Userpasswd.get())
            mycursor.execute(sql, val)
            s = mycursor.fetchone()
            
            if s == None:
                messagebox.showinfo('로그인 실패', '로그인이 실패했습니다.')
                self.UserId.set("")
                self.Userpasswd.set("")
                self.idt.focus()
                
            else:
                s = '' + ''.join(s)
                c_s = str(s) + '님 로그인을 성공했습니다.'
                messagebox.showinfo('로그인 성공', c_s)
                people = Webcam()
                
        mydb.commit()
        mydb.close()

class Webcam(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("760x800+0+0")
        self.title('얼굴 인식 출석 시스템 - 데이터 수집 & 웹캠 & 출석 확인')
        self.resizable(False, False)
                # frame
        self.top = Frame(self, height=200, bg="white")
        self.top.pack(fill=X)
        
        #  bottom
        self.bottom = Frame(self, height=600, bg="#326fa8")
        self.bottom.pack(fill=X)
        

        self.heading = Label(self.top, text="얼굴 인식 출석 시스템", 
                             font='arial 30 bold',
                             bg='white', fg='black')
        self.heading.place(x=180, y=75)
            
        # datetime 
        self.date_lbl = Label(self.top, text=date,
                             font='arial 15 bold', bg='white', fg='black')
        self.date_lbl.place(x=650, y=0)
        
        #===============Login name, passwd Label and Entry======================
        self.bottom_title = Label(self.bottom, text='3 : 데이터 학습 & 웹캠 페이지',
                                 font='arial 30 bold', bg='#326fa8'
                                 ,fg='black')
        self.bottom_title.place(x=125, y=5) 
        
        self.bottom_title = Label(self.bottom, text='첫 번째 데이터 학습을 눌러주세요.',
                                 font='arial 25 bold', bg='#326fa8'
                                 ,fg='black')
        self.bottom_title.place(x=125, y=100) 
        
        self.bottom_title = Label(self.bottom, text='두 번째 웹캠 시작을 눌러주세요.',
                                 font='arial 25 bold', bg='#326fa8'
                                 ,fg='black')
        self.bottom_title.place(x=125, y=175)
        
        self.bottom_title = Label(self.bottom, text='세 번째 출석 체크확인을 눌러주세요.',
                                 font='arial 25 bold', bg='#326fa8'
                                 ,fg='black')
        self.bottom_title.place(x=125, y=250)
        
        train = Button(self.bottom, text='1>데이터 학습', height=4, width=12,
                    font='Sans 12 bold',
                    command=self.train_classifier)
        train.place(x=100, y=400)
        
        webcam = Button(self.bottom, text='2>웹캠 시작!', height=4, width=12,
                           font='Sans 12 bold',
                           command=self.detect_face)
        webcam.place(x=250, y=400)
    
        att = Button(self.bottom, text='3>출석 체크확인', height=4, width=12,
                           font='Sans 12 bold',
                           command=self.go_four)
        att.place(x=400, y=400) 
        
        exit = Button(self.bottom, text='종료', height=4, width=12,
                           font='Sans 12 bold',
                           command=self.iExit)
        exit.place(x=550, y=400) 
        
    
    def go_four(self):
        people = Four()
    
    def detect_face(self):
        def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf):
            
            features = None
            features = classifier.detect_faces(img)

            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            coords = []

            for feature in features:
                x, y, w, h = feature['box']
                cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)
                id, pred = clf.predict(gray_image[y:y+h, x:x+w])
                confidence = int(100 * (1 - pred / 300))
                mydb = pymysql.connect(
                    host="localhost",
                    port=3306,
                    user="root",
                    passwd="root",
                    db="dcu_member",
                    charset='utf8'
                )
                mycursor = mydb.cursor()

                mycursor.execute("SELECT user_name from last_member where id=" + str(id))
                s = mycursor.fetchone()
                s = '' + ''.join(s)
                c_s = s + '님 출석체크를 완료했습니다.'

                if confidence > 80:
                    cv2.putText(img, s + str(confidence) + "%",
                                (x, y-5), cv2.FONT_HERSHEY_SIMPLEX,
                                0.8,
                                color,
                                1,
                                cv2.LINE_AA)
                    if confidence >= 85:
                        mycursor.execute("UPDATE last_member SET readcount = readcount + 1 WHERE user_name= '" + s + "'")
                        mydb.commit()
                        mydb.close()
                        messagebox.showinfo('Result', c_s)
                        messagebox.showinfo('Result', '종료를 원하시면 Enter를 눌러 주세요.')

                        
                else:
                    cv2.putText(img, "Unknown",
                                (x, y-5),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.8,
                                (0, 0, 255),
                                1,
                                cv2.LINE_AA)
                
                
                coords = [x, y, w, h]
            return coords
    
        def recognize(img, clf, faceCascade):
            coords = draw_boundary(img,
                                   faceCascade,
                                   1.1, # scaleFactor
                                   10,  # minNeighbors
                                   (255, 255, 255),
                                   "Face",
                                   clf)
            return img

        faceCascade = MTCNN()
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.read("classifier.xml")

        video_capture = cv2.VideoCapture(0, cv2.CAP_MSMF)

        while True:
            ret, img = video_capture.read()
            img = recognize(img, clf, faceCascade)
            cv2.imshow("face detection", img)

            if cv2.waitKey(1) == 13 or 0xFF == ord('q'): 
                break
            
        video_capture.release()
        cv2.destroyAllWindows()
        self.bottom_title.focus()
        
    def iExit(self):    
        self.iExit = messagebox.askyesno('로그인', "종료 하시겠습니까?")
        if self.iExit > 0:
            self.master.destroy()
        else:
            command = Webcam()
            return 
        
    def train_classifier(self):
        data_dir = "C:/Users/330-15/Desktop/20_1_computer/20_1_CreativeFusion/PyQt5/data"
        path = [os.path.join(data_dir, f) for f in os.listdir(data_dir)]
        faces = []
        ids = []

        for image in path:
            img = Image.open(image).convert('L');
            imageNp = np.array(img, 'uint8')
            # user.1.1~200 
            id = int(os.path.split(image)[1].split(".")[1])
            faces.append(imageNp)
            ids.append(id)
        ids = np.array(ids)

        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.train(faces, ids)
        clf.write("classifier.xml")
        messagebox.showinfo('Result', '데이터 학습을 완료했습니다.')
        self.bottom_title.focus()
        
class Four(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("760x800+0+0")
        self.title('데이터 학습, 웹캠')
        self.resizable(False, False)
                # frame
        self.top = Frame(self, height=200, bg="white")
        self.top.pack(fill=X)
        
        self.middle = Frame(self, height=150, bg="#326fa8")
        self.middle.pack(fill=X)
        
        #  bottom
        self.bottom = Frame(self, height=450, bg="#326fa8")
        self.bottom.pack(fill=X)
        

        self.heading = Label(self.top, text="얼굴 인식 출석 시스템", 
                             font='arial 30 bold',
                             bg='white', fg='black')
        self.heading.place(x=180, y=75)
            
        # datetime 
        self.date_lbl = Label(self.top, text=date,
                             font='arial 15 bold', bg='white', fg='black')
        self.date_lbl.place(x=650, y=0)
        
        self.bottom_title = Label(self.middle, text='4 : 출석 명단 확인',
                                 font='arial 30 bold', bg='#326fa8'
                                 ,fg='black')
        self.bottom_title.place(x=200, y=5) 
        
        self.scroll = Scrollbar(self.bottom, orient=VERTICAL)
        
        self.listBox = Listbox(self.bottom, activestyle='underline',
                               width=40, height=27, font='arial 12 bold')
        self.listBox.grid(row=0, column=0, padx=(40, 0))
        self.scroll.config(command=self.listBox.yview)
        self.listBox.config(yscrollcommand=self.scroll.set)
        
        self.scroll.grid(row=0, column=1, sticky=N+S)
        
        btnadd = Button(self.bottom, text="이전 페이지", width=10, height=4,
                       font='arial 12 bold', command=self.previous)
        btnadd.place(x= 550, y = 0)
        
        btnExit = Button(self.bottom, text="종료", width=10, height=4,
                        font='arial 12 bold', command=self.iExit)
        btnExit.place(x=550,  y =  150)
        
        self.bottom_title = Label(self.middle, text='자신의 이름을 확인하고 종료를 눌러주세요.',
                                 font='arial 25 bold', bg='#326fa8'
                                 ,fg='black')
        self.bottom_title.place(x=50, y=100) 
        
        mydb = pymysql.connect(
            host="localhost",
            port=3306,
            user="root",
            passwd="root",
            db="dcu_member",
            charset='utf8'
        )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM last_member WHERE readcount >= 1 ORDER BY id DESC")
        persons = mycursor.fetchall()
        count = 1
        self.listBox.insert(0, "번호" + "       " + "이름" + "       " + "전공")
        for person in persons:
            self.listBox.insert(count, str(person[0]) + "       " + 
                                str(person[3])  + "       " + str(person[5]))
    
    def previous(self):
        people = Webcam()
        
    def iExit(self):    
        self.iExit = messagebox.askyesno('출석확인', "종료 하시겠습니까?")
        if self.iExit > 0:
            messagebox.showinfo("감사합니다", "이용해 주셔서 감사합니다.")
            self.master.destroy()
        
def main():
    root = Tk()
    app = Application(root)
    root.title("얼굴 인식 출석 프로그램")
    root.geometry("760x800+0+0")
    root.resizable(False, False)    
    root.mainloop()
    
if __name__ == '__main__':
    main()
    