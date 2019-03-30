import PIL.ImageGrab
from twilio.rest import Client
import smtplib
import cv2
import numpy as np
import os
import datetime
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('C:/Users/SONY/project/trainer/trainer.yml')
cascadePath = 'C:/Users/SONY/env1/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascadePath)
font = cv2.FONT_HERSHEY_SIMPLEX

id = 0

names = ['None', 'pushpak', 'yash', 'abc'] 
cam = cv2.VideoCapture(0)

return_value, image = cam.read()
cv2.imwrite('opencv.png', image)
cam.set(3, 640) # set video widht
cam.set(4, 480) # set video height
# Define min window size to be recognized as a face
minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)
while True:
    ret, img =cam.read()
    #img = cv2.flip(img, -1) # Flip vertically
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
    faces = faceCascade.detectMultiScale( 
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (int(minW), int(minH)),
       )
    for(x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
        # Check if confidence is less them 100 ==> "0" is perfect match 
        if (confidence < 100):
            id = names[id]
            dt = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
            kid = id
            kid1=id + dt
            flag = 1
            confidence = "  {0}%".format(round(100 - confidence))
        else:
            id = "unknown" 
            dt = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
            uid = id
            uid1=id + dt
            flag = 0
            confidence = "  {0}%".format(round(100 - confidence)) #max = inrange(60-70)

        cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
        cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
    
    cv2.imshow('camera',img) 
    k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break
print("\nExiting Program")
cam.release()
cv2.destroyAllWindows()

def message_known():
    account_sid = 'AC678355dbc9065815580330667d47d2a8'
    auth_token = 'a31c0cd5a3ea7d66a544d46d36434e2d'
    client = Client(account_sid, auth_token)

    text = client.messages \
    .create(
         body=kid1,
         from_='+19372034675',
         to='+919599831779'
         #to='+918950520220'
     )
    print(text.sid)

def message_unknown():
    account_sid = 'AC678355dbc9065815580330667d47d2a8'
    auth_token = 'a31c0cd5a3ea7d66a544d46d36434e2d'
    client = Client(account_sid, auth_token)

    text = client.messages \
    .create(
         body=uid1,
         from_='+19372034675',
         #to='+918950520220'
         to='+919599831779'
     )
    print(text.sid)

def known():
    fromaddr = "rpi.major@gmail.com"
    toaddr = "pushpak237@gmail.com"

    # instance of MIMEMultipart 
    msg = MIMEMultipart() 

    # storing the senders email address 
    msg['From'] = fromaddr 

    # storing the receivers email address 
    msg['To'] = toaddr 

    # storing the subject 
    msg['Subject'] = "face recognition"

    # string to store the body of the mail 
    body = "person = " + kid + " at" + " " + dt

    # attach the body with the msg instance 
    msg.attach(MIMEText(body, 'plain')) 

    # open the file to be sent 
    filename = "opencv.png"
    attachment = open(r"C:\Users\SONY\project\opencv.png", "rb") 

    # instance of MIMEBase and named as p 
    p = MIMEBase('application', 'octet-stream') 

    # To change the payload into encoded form 
    p.set_payload((attachment).read()) 

    # encode into base64 
    encoders.encode_base64(p) 

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 

    # attach the instance 'p' to instance 'msg' 
    msg.attach(p) 

    # creates SMTP session 
    s = smtplib.SMTP('smtp.gmail.com', 587) 

    # start TLS for security 
    s.starttls() 

    # Authentication 
    s.login(fromaddr, "qwerty123#") 

    # Converts the Multipart msg into a string 
    text = msg.as_string() 

    # sending the mail 
    s.sendmail(fromaddr, toaddr, text) 

    # terminating the session 
    s.quit() 

def unknown():
    fromaddr = "rpi.major@gmail.com"
    toaddr = "pushpak237@gmail.com"

    # instance of MIMEMultipart 
    msg = MIMEMultipart() 

    # storing the senders email address 
    msg['From'] = fromaddr 

    # storing the receivers email address 
    msg['To'] = toaddr 

    # storing the subject 
    msg['Subject'] = "face recognition"

    # string to store the body of the mail 
    body = "person = " + uid + " at" + " " + dt

    # attach the body with the msg instance 
    msg.attach(MIMEText(body, 'plain')) 

    # open the file to be sent 
    filename = "opencv.png"
    attachment = open(r"C:\Users\SONY\project\opencv.png", "rb") 

    # instance of MIMEBase and named as p 
    p = MIMEBase('application', 'octet-stream') 

    # To change the payload into encoded form 
    p.set_payload((attachment).read()) 

    # encode into base64 
    encoders.encode_base64(p) 

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 

    # attach the instance 'p' to instance 'msg' 
    msg.attach(p) 

    # creates SMTP session 
    s = smtplib.SMTP('smtp.gmail.com', 587) 

    # start TLS for security 
    s.starttls() 

    # Authentication 
    s.login(fromaddr, "qwerty123#") 

    # Converts the Multipart msg into a string 
    text = msg.as_string() 

    # sending the mail 
    s.sendmail(fromaddr, toaddr, text) 

    # terminating the session 
    s.quit() 




if(flag==1):
        message_known()
        known()
else:
        message_unknown()
        unknown()
