import cv2, os, random, sys
import numpy as np
import sqlite3

faceDetect = cv2.CascadeClassifier('Cascades\\haarcascade_frontalface_default.xml')
cam = cv2.VideoCapture(0)

# id = random.randint(1,1000)

o = open('extras/count.txt')
oo = o.read()

id = int(oo) #2
o.close()
sampleNumber = 0

def insertOrUpdate(Id,Name):
	conn = sqlite3.connect('DataBase/FaceBase.db')
	cmd = "SELECT * FROM People WHERE ID="+str(Id)
	cursor = conn.execute(cmd)
	print(cursor)
	isRecordExists = 0
	# row = None
	for row in cursor:
		isRecordExists = 1
	if (isRecordExists == 1):
		cmd="UPDATE People SET Name="+str(Name)+" WHERE ID = "+str(Id)
	else:
		cmd="INSERT INTO People(ID,Name) Values("+str(Id)+","+str(Name)+")"
		o = open('extras/count.txt','w')
		o.write(str(id+1))
		o.close()

	conn.execute(cmd)
	conn.commit()
	conn.close()

name = sys.argv[1]
name = '"'+name+'"'
# name = str(input('Enter Your Name : '))
insertOrUpdate(id,name)

while(True):
	print(sampleNumber)
	ret, img = cam.read()
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	faces = faceDetect.detectMultiScale(gray,1.8,5)
	# os.chdir('dataSet')
	# if not os.path.isdir(str(id)):
	# 	os.mkdir(str(id))
	for (x,y,w,h) in faces:
		sampleNumber +=1
		cv2.imwrite('dataSet/User.'+str(id)+'.'+str(sampleNumber)+'.jpg',gray[y-2:y+h+2,x-2:x+w+2])
		cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
	cv2.imshow('face',img)
	if sampleNumber >=300:
		break
	if cv2.waitKey(1) == ord('q'):
		break;
cam.release()
cv2.destroyAllWindows()