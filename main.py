from Tkinter import *
import requests
from bs4 import BeautifulSoup
import os



root = Tk()

#Window Config

root.title("Z-Library Python App")
root.iconbitmap("favicon.ico")
root.option_add('*font', ('Helvetica', 12, 'bold'))

width = root.winfo_screenwidth()
height = root.winfo_screenheight()

downArr=[]



def retrieve_input():
	inputValue=textBox.get("1.0","end-1c")
	T.delete('1.0', END)
	response = requests.get("https://b-ok.cc/s/?q="+inputValue)
	doc = BeautifulSoup(response.text, 'html.parser')
	title_tags = doc.find_all(class_='tdn')
	i=1
	for title in title_tags:
		T.insert(END, i)
		T.insert(END, " => "+title.text.strip())
		T.insert(END, '\n\n')
		i=i+1
	noInputLabel.config(text="")
	if inputValue=="":
		noInputLabel.config(text="Please Enter Something First")


def down_input():
	inputValue=textBox.get("1.0","end-1c")
	response = requests.get("https://b-ok.cc/s/?q="+inputValue)
	doc = BeautifulSoup(response.text, 'html.parser')
	inputValue2=textBox2.get("1.0","end-1c")
	T2.delete('1.0', END)
	noInputLabel.config(text="")
	down_links = doc.find_all(class_='ddownload')
	for a in doc.find_all('a',href=True,class_='ddownload'):	
		downArr.append("https://b-ok.org"+str(a['href']))
	try:
		T2.insert(END, downArr[int(inputValue2)-1])
	except:
		noInputLabel.config(text="Please Enter Something in Search First")

	if inputValue2=="":
		noInputLabel.config(text="Please Enter Something First")
	


w = Label(root, text="Book Grabber using Tkinter and BeautifulSoup")
w.config(font=("Courier", 25,"bold"))
w.pack(side=TOP)


textBox=Text(root, height=1, width=30,relief=RIDGE,borderwidth=2)
textBox.pack(side=TOP,pady=7)
searchBtn=Button(root, height=1, width=20, text="Search" ,bg="grey", fg="black",command=lambda: retrieve_input())

searchBtn.pack(side=TOP,pady=4)
textBox2=Text(root, height=1, width=30,relief=RIDGE,borderwidth=2)
textBox2.pack(side=TOP,pady=7)
downBtn=Button(root, height=1, width=20, text="Download" ,bg="grey", fg="black",command=lambda: down_input())
downBtn.pack(side=TOP,pady=4)

noInputLabel = Label(root, text="",fg='red')
noInputLabel.pack(side=TOP,pady=3)

w = Label(root, text="Enter the respective Serial Number of the book to Download")
w.pack(side=TOP,pady=6)
w = Label(root, text="Click on the text to enable Mouse Scroll")
w.pack(side=BOTTOM)
T2 = Text(root, height=3, width=width/3,background='black',fg='green')
T2.pack(side=BOTTOM,pady=10)
S = Scrollbar(root)
T = Text(root, height=20, width=width/3,background='black',fg='green')
S.pack(side=RIGHT, fill=Y)
T.pack(side=LEFT, fill=Y)
S.config(command=T.yview)
T.config(yscrollcommand=S.set)




mainloop(  )    	