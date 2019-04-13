from Tkinter import *
import requests
from bs4 import BeautifulSoup
import os



root = Tk()

#Window Config

root.title("Z-Library Python App")
root.iconbitmap("favicon.ico")
root.option_add('*font', ('verdana', 12, 'bold'))

width = root.winfo_screenwidth()
height = root.winfo_screenheight()

downArr=[]

def retrieve_input():
	inputValue=textBox.get("1.0","end-1c")
	T.delete('1.0', END)
	response = requests.get("https://b-ok.cc/s/?q="+inputValue)
	doc = BeautifulSoup(response.text, 'html.parser')

	title_tags = doc.find_all(class_='tdn')
	down_links = doc.find_all(class_='ddownload')
	i=1
	for title in title_tags:
		T.insert(END, i)
		T.insert(END, " => "+title.text.strip())
		T.insert(END, '\n\n')
		i=i+1
	for a in doc.find_all('a',href=True,class_='ddownload'):	
		downArr.append(a['href'])
	print u", ".join(downArr)


w = Label(root, text="Book Grabber using Tkinter and BeautifulSoup")
w.config(font=("Courier", 25,"bold"))
w.pack(side=TOP)


textBox=Text(root, height=1, width=30,relief=RIDGE,borderwidth=2)
textBox.pack(side=TOP,pady=7)
searchBtn=Button(root, height=1, width=20, text="Search" ,bg="grey", fg="black",command=lambda: retrieve_input())

searchBtn.pack(side=TOP,pady=4)
textBox2=Text(root, height=1, width=30,relief=RIDGE,borderwidth=2)
textBox2.pack(side=TOP,pady=7)
downBtn=Button(root, height=1, width=20, text="Download" ,bg="grey", fg="black",command=lambda: retrieve_input())
downBtn.pack(side=TOP,pady=4)
w = Label(root, text="Enter the respective Serial Number of the book to Download")
w.pack(side=TOP,pady=6)
w = Label(root, text="Click on the text to enable Mouse Scroll")
w.pack(side=BOTTOM)
S = Scrollbar(root)
T = Text(root, height=18, width=width/3,background='black',fg='green')
S.pack(side=RIGHT, fill=Y)
T.pack(side=LEFT, fill=Y)
S.config(command=T.yview)
T.config(yscrollcommand=S.set)


mainloop(  )    	