from Tkinter import *
import requests
from bs4 import BeautifulSoup
import urllib
from tkMessageBox import showinfo
import time
import re
import itertools
import webbrowser
import os

root = Tk()
root.withdraw()
root.title("Z-Library Python App")
root.iconbitmap("favicon.ico")
root.option_add('*font', ('Helvetica', 12, 'bold'))


width = root.winfo_screenwidth()
height = root.winfo_screenheight()

bookArr=[]
downArr=[]
md5=[]
merged=[]
titleArr=[]
#http://gen.lib.rus.ec/search.php?req=web&lg_topic=libgen&open=0&view=simple&res=100&phrase=1&column=def


def retrieve_input():
	inputValue=textBox.get("1.0","end-1c")
	T.delete('1.0', END)
	response = requests.get("http://gen.lib.rus.ec/search.php?req="+inputValue+"&lg_topic=libgen&open=0&view=simple&res=100&phrase=1&column=def")
	doc = BeautifulSoup(response.text, 'html.parser')
	
	table_rows = doc.find_all('tr')
	x=1
	for tr in table_rows:
		td = tr.find_all('td', {"width" : "500"})
		row = [i.text for i in td]
		content = ", ".join(row)
		if len(row) != 0:
			T.insert(END, "\n"+str(x)+"  => "+content)
			titleArr.append(row)
			x=x+1
		links = tr.findAll('a', href=re.compile("^book"))
		
		for a in links:	
			bookArr.append("http://gen.lib.rus.ec/"+str(a['href']))
				
#  \=(.*)$ 
	for x in bookArr:
		md5.append(re.findall(r'\=(.*)$', x))
	noInputLabel.config(text="")
	if inputValue=="":
		noInputLabel.config(text="Please Enter Something First")

def down_input():
	try:
		T2.delete('1.0', END)
		noInputLabel.config(text="")
		serial=textBox2.get("1.0","end-1c")
		merged = list(itertools.chain(*md5))
		merged2 = list(itertools.chain(*titleArr))
		titleArr_unUnicoded =  [ x.encode('ascii', errors='replace') for x in merged2 ]
		file_name = titleArr_unUnicoded[int(serial)-1]+".pdf"
		T2.insert(END, "Downloading "+file_name +"  ... .. .")
		root.update_idletasks()
		md5hash = str(merged[int(serial)-1])
		response2 = requests.get("http://library1.org/_ads/"+md5hash)

		doc2 = BeautifulSoup(response2.text, 'html.parser')
		link_elem = doc2.find('a')
		file_url = link_elem['href']
		r = requests.get(file_url, stream = True) 
	  

		with open(file_name,"wb") as pdf: 
			for chunk in r.iter_content(chunk_size=1024): 
			# writing one chunk at a time to pdf file 
				if chunk: 
					pdf.write(chunk)
		webbrowser.open('file://' + os.path.realpath(file_name))

	except:
		noInputLabel.config(text="Please Enter Something in Search First")

	if serial=="":
		noInputLabel.config(text="Please Enter Something First")

showinfo("Status","Checking for Internet Connectivity ...")

try :
	chk_link = "http://gen.lib.rus.ec"
	urllib.urlopen(chk_link)
	showinfo("Status", "Successfully Connected to B-ok.org")
	root.deiconify()

except :
	showinfo("Status", "Problem Connecting to B-ok.org")

	root.destroy()  




	
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
T2 = Text(root, height=3, width=width/3,background='black',fg='orange')
T2.pack(side=BOTTOM,pady=10)
S = Scrollbar(root)
T = Text(root, height=20, width=width/3,background='black',fg='green')
S.pack(side=RIGHT, fill=Y)
T.pack(side=LEFT, fill=Y)
S.config(command=T.yview)
T.config(yscrollcommand=S.set)

mainloop(  )    	