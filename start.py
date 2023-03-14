from tkinter import *
import threading, os, subprocess, sqlite3
from PIL import Image
import pandas as pd
from tkinter import messagebox
import sys

win = Tk()
win.configure(background='linen')
win.geometry('650x400')

detectingPng = PhotoImage(file='Ui/Det.png')
addNewPng = PhotoImage(file='Ui/AddNew.png')
reTrainPng = PhotoImage(file='Ui/ReTrain.png')
checkPng = PhotoImage(file='Ui/Check.png')
helpPng = PhotoImage(file='Ui/Help.png')
settingsPng = PhotoImage(file='Ui/Settings.png')
QuitPng = PhotoImage(file='Ui/quit.png')

count = 0
show_detector = BooleanVar() # show_detector = False
show_detector.set(True)
process = None
sd = None


def addUser():

	def startEnr():
		z = str(en.get())
		if len(z) >15:
			z = z[:10]
		print(z)
		# def c(name):
		# 	call(["python","addUser.py", name])
		# processs = threading.Thread(target=c,args=(z,))
		# processs.start()
		process = subprocess.Popen([sys.executable,'addUser.py',z])
		print('running')

	addwin = Tk()
	addwin.geometry('200x200')
	lb = Label(addwin,text='Name : ')
	lb.pack()
	en = Entry(addwin)
	en.pack()
	bt = Button(addwin,text='Start Enrolling',command=startEnr)
	bt.pack()
	addwin.mainloop()

def trainer():
	process = subprocess.Popen([sys.executable,'trainer.py'])
	print('running')

def fun_delete(Id):
	res = messagebox.askquestion('Delete a Face !', 'Do you really want to Delete this face ? ')

	if res == 'yes' :
		conn = sqlite3.connect('DataBase/FaceBase.db')
		try:
			cmd = "DELETE FROM People WHERE ID = "+str(Id)
			cursor = conn.execute(cmd)
			conn.commit()
		except:
			print('Something went wrong')
		conn.close()
		print('Deleted...',Id)

	else :
		print('Nothing happens')

	

def delete_a_face():
	conn = sqlite3.connect('DataBase/FaceBase.db')
	cmd = "SELECT * FROM People"
	cursor = conn.execute(cmd)

	ttl = Toplevel()
	ttl.geometry('400x600')
	t = Label(ttl,text='Enter the Name to delete',font=('airal',17),fg='white',bg='red')
	t.pack(pady=(20,0))
	for i in cursor:
		bt = Label(ttl,text=i[0]+f'{ {i[1]} }',font=('arial',15))
		bt.pack(padx=10,pady=15,side='left',anchor='nw')

	fr = Frame(ttl)
	fr.pack(side='left')

	lb = Label(fr,text='Enter Id here :',font=('arial',14))
	lb.pack()

	en = Entry(fr)
	en.pack(pady=20)

	btn = Button(fr,text='Delete',command=lambda : fun_delete(str(en.get())))
	btn.pack()

	conn.close()
	ttl.mainloop()

def settings():
	global show_detector
	sp = Toplevel()
	sp.geometry('200x200')

	c = Checkbutton(sp,text='Show Realtime attendance',variable=show_detector,onvalue=True,offvalue=False)
	c.pack(pady=20)

	df = Button(sp,text='Delete A Face',command=delete_a_face)
	df.pack()

	bx = Button(sp,text='Close',command=lambda : sp.destroy())
	bx.pack(pady=20)

def start():
	global process, show_detector, win, sd
	s_d = show_detector.get()
	if s_d == True:
		process = subprocess.Popen([sys.executable,'detector.py','0'])
		print('running')
		pass
	if s_d == False:
		process = subprocess.Popen([sys.executable,'detector.py','1'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
		win.withdraw()
		print('running')

	def close():
		global win, sd, process
		try:
			process.terminate()
			win.deiconify()
			sd.destroy()
		except:
			print('...')

	def ani():
		global count
		if count == 0:
			im2 = an1
		if count == 1:
			im2 = an2
		if count == 2:
			im2 = an3
		l.configure(image=im2)
		count +=1
		if count == 3:
			count = 0
		sd.after(700,ani)

	if s_d == False:
		sd = Tk()
		an1 = PhotoImage(file='Ui/GIF/started1.png',master=sd)
		an2 = PhotoImage(file='Ui/GIF/started2.png',master=sd)
		an3 = PhotoImage(file='Ui/GIF/started3.png',master=sd)
		l = Label(sd)
		l.config(image='')
		l.pack()
		stpbtn = Button(sd,text='Stop',bg='red',fg='white',command=close)
		stpbtn.pack(expand=True,fill='both')
		ani()
		win.withdraw()
		sd.mainloop()

def check():
	process = subprocess.Popen([sys.executable,'showAttendance.py'])
	print('running')
	


frUpper = Frame(win,borderwidth=4,relief='flat',bg='deep sky blue')
frUpper.pack(expand=True,fill='both')

frDown = Frame(win,borderwidth=4,relief='flat',bg='deep sky blue')
frDown.pack(expand=True,fill='both')

frUpperl = Frame(frUpper,relief='flat',bg='deep sky blue')
frUpperl.pack(side='left',expand=True,fill='both')

frUpperr = Frame(frUpper,relief='flat',bg='deep sky blue')
frUpperr.pack(side='right',expand=True,fill='both')

btnStart = Button(frUpperl,image=detectingPng,bg='deep sky blue',command=start,relief='flat')
btnStart.pack(expand=True,fill='both')

btnAdd = Button(frUpperr,image=addNewPng,bg='deep sky blue',command=addUser,relief='flat')
btnAdd.pack(expand=True,fill='both')

btntrain = Button(frUpperr,image=reTrainPng,bg='deep sky blue',command=trainer,relief='flat')
btntrain.pack(expand=True,fill='both')

btnCheck = Button(frUpperr,image=checkPng,bg='deep sky blue',command=check,relief='flat')
btnCheck.pack(expand=True,fill='both')

btndoc = Button(frUpperl,image=helpPng,bg='deep sky blue',command=check,relief='flat')
btndoc.pack(side='left',expand=True)

btnsetting = Button(frUpperl,image=settingsPng,bg='deep sky blue',command=settings,relief='flat')
btnsetting.pack(side='left',expand=True)

btnquit = Button(frUpperl,image=QuitPng,bg='deep sky blue',command=lambda : win.destroy(),relief='flat')
btnquit.pack(side='left',expand=True)

win.mainloop()

