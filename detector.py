import cv2, sqlite3, sys
import numpy as np
from datetime import datetime, date, timedelta
import pandas as pd
from playsound import playsound
import threading, subprocess

faceDetect = cv2.CascadeClassifier('Cascades\\haarcascade_frontalface_default.xml')
cam = cv2.VideoCapture(0)

rec = cv2.face.LBPHFaceRecognizer_create()
rec.read('recognizer/traningData.yml')

id = 0
done = []
dateadded = False
# font = cv2.cv.InitFont(cv2.cv.CV_FONT_HERSHEY_COMPLEX_SMALL,1,1,0,1)

try:
	show = int(sys.argv[1])
except:
	show = 0

print(show)

def getProfile(id):
	conn = sqlite3.connect('DataBase/FaceBase.db')
	cmd = "SELECT * FROM People WHERE ID = "+str(id)
	cursor = conn.execute(cmd)
	profile = None
	for row in cursor:
		profile = row
	conn.close()
	return profile


def markAtten(name,id):
	global done, dateadded
	if name in done:
		pass 
	else:
		# yesterday = str(date.today() - timedelta(days=1))
		# today = str(date.today())
		# time = datetime.now()
		# time = time.strftime("%H:%M:%S")

		# if dateadded == False:
		# 	o = open('extras/names.txt','a')
		# 	o.write('----------------'+'\n')
		# 	o.close()

		# 	o = open('extras/time.txt','a')
		# 	o.write('----------------'+'\n')
		# 	o.close()

		# 	dateadded = True

		# o = open('extras/names.txt','a')
		# o.write(str(name)+'\n')
		# o.close()

		# o = open('extras/time.txt','a')
		# o.write(str(time)+'\n')
		# o.close()

		# if not name in done:
		conn = sqlite3.connect('DataBase/FaceBase.db')
		cmd = "SELECT * FROM People WHERE ID = "+str(id)
		cursor = conn.execute(cmd)
		profile = None
		for row in cursor:
			profile = row
		num = int(profile[2])
		new = num+1
		def c():
			playsound('Ui/Audios/granted.wav')
		processs = threading.Thread(target=c)
		processs.start()
		cmd="UPDATE People SET Attendance="+str(new)+" WHERE ID = "+str(id)
		conn.execute(cmd)
		conn.commit()
		conn.close()
		done.append(name)

while(True):
	ret, img = cam.read()
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	faces = faceDetect.detectMultiScale(gray,1.8,5)
	for (x,y,w,h) in faces:
		cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
		id, conf = rec.predict(gray[y:y+h,x:x+w])
		profile = getProfile(id)
		print(profile)
		if profile != None:
			# id, conf = rec.predict(gray[y:y+h,x:x+w])
			# cv2.putText(cv2.cv.fromarray(img),str(id),(x,y+h+50),font,(0,0,255))
			print('Id is {}, name is {} with confidence of {}'.format(str(profile[1]),str(profile[0]),conf))
			markAtten(profile[0],profile[1])
			print(done)

	if show == 0:
		cv2.imshow('face',img)
	if cv2.waitKey(1) == ord('q'):
		break;
cam.release()
cv2.destroyAllWindows()

