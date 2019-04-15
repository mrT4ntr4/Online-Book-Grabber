from Tkinter import *
import requests
from bs4 import BeautifulSoup
import urllib
from tkMessageBox import showinfo
import time
from io import BytesIO
import re
import itertools
import webbrowser
import ttk
import sys
import os
from PIL import Image, ImageTk



root = Tk()
root.withdraw()
root.title("Online Book Grabber")
root.iconbitmap("favicon.ico")
root.option_add('*font', ('Helvetica', 12, 'bold'))



width = root.winfo_screenwidth()
height = root.winfo_screenheight()-200



x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry('{}x{}+{}+{}'.format(width, height, x, y))



bookArr=[]
downArr=[]
md5=[]
merged=[]
titleArr=[]
randomArr=[]
#http://gen.lib.rus.ec/search.php?req=web&lg_topic=libgen&open=0&view=simple&res=100&phrase=1&column=def

def leftclick(event):
	w.config(text="Mouse wheel Scrolling enabled")
	root.after(2000, lambda : w.config(text="Click on the text to enable Mouse Scroll"))

def search(text_widget, keyword1,keyword2, tag):
	pos = '1.0'
	while True:
		kb = T.search(keyword1, pos, END)
		mb = T.search(keyword2, pos, END)

		if not kb:
			break
		pos = '{}+{}c'.format(kb, len(keyword1))

		T.tag_add(tag, kb, pos)
		if not mb:
			break
		pos = '{}+{}c'.format(mb, len(keyword2))
		T.tag_add(tag, mb, pos)





def retrieve_input():
	inputValue=textBox.get()
	T.delete('1.0', END)
	response = requests.get("http://gen.lib.rus.ec/search.php?req="+inputValue+"&lg_topic=libgen&open=0&view=simple&res=100&phrase=1&column=def")
	doc = BeautifulSoup(response.text, 'html.parser')
	
	table_rows = doc.find_all('tr')

	bookArr[:]=[]
	downArr[:]=[]
	md5[:]=[]
	merged[:]=[]
	titleArr[:]=[]
	randomArr[:]=[]

	x=1
	for tr in table_rows:
		td = tr.find_all('td', {"width" : "500"})
		row = [i.text for i in td]
		content = ", ".join(row)

		randomArr.append(tr.find_all('td'))

		if len(row) != 0:
			T.insert(END, "\n"+str(x)+"  => "+content+"          "+randomArr[x+2][7].text + "          " +randomArr[x+2][8].text + "\n")
 			search(T, 'Kb','Mb', 'failed')
 			search(T, 'pdf','epub', 'passed')
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
	#try:
	T2.delete('1.0', END)
	noInputLabel.config(text="")
	serial=textBox2.get()
	merged = list(itertools.chain(*md5))
	merged2 = list(itertools.chain(*titleArr))
	titleArr_unUnicoded =  [ x.encode('ascii', errors='replace') for x in merged2 ]
	
	file_name = titleArr_unUnicoded[int(serial)-1].replace("?","") +".pdf"

	print file_name
	T2.insert(END, "Downloading "+file_name +"  ... .. .")
	root.update_idletasks()
	md5hash = str(merged[int(serial)-1])
	response2 = requests.get("http://library1.org/_ads/"+md5hash)

	doc2 = BeautifulSoup(response2.text, 'html.parser')
	link_elem = doc2.find('a')
	img_elem = doc2.find('img')['src']
	img_url = "http://library1.org"+img_elem


	response = requests.get(img_url)
	img_data = response.content
	img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))
	top = Toplevel(bg="black")
	top.title("Online Book Grabber")
	


	label = Label(top,highlightbackground="light sky blue", highlightcolor="light sky blue", highlightthickness=10,image=img, relief="solid",background='light sky blue')
	label2 = Label(top,font=("Courier", 20,"bold"),text="Are you sure you want to Download :",foreground='light sky blue',bg='black')
	label.photo = img

	label.pack(side=BOTTOM,padx=80,pady=20)
	label2.pack(side=TOP,padx=80,pady=20)
	top.update()

	file_url = link_elem['href']
	'''d = urllib.urlopen(file_url)
	content_size =  d.info()['Content-Length']
	r = requests.get(file_url, stream = True) 
	
	pb_hd = ttk.Progressbar(top, orient='horizontal', mode='determinate')
  	pb_hd.pack(expand=True, side=TOP)
	pb_hd['maximum'] = int(content_size)
	i=1
	'''
	with open(file_name,"wb") as pdf: 
		for chunk in r.iter_content(chunk_size=1000): 
		# writing one chunk at a time to pdf file
			if chunk:
				pdf.write(chunk)
				'''time.sleep(0.05)
				pb_hd['value'] = i
				pb_hd.update()
				i=i+1'''
	status_label = Label(top,text="Download Completed !!")
	status_label.pack(side=TOP)
	webbrowser.open('file://' + os.path.realpath(file_name))

'''	
	except :
		noInputLabel.config(text="Please Enter Something in Search First")

	if serial=="":
		noInputLabel.config(text="Please Enter Something First")
'''
showinfo("Status","Checking for Internet Connectivity ...")

try :
	chk_link = "http://gen.lib.rus.ec"
	urllib.urlopen(chk_link)
	showinfo("Status", "Successfully Connected to gen.lib.rus.ec")
	root.deiconify()

except :
	showinfo("Status", "Problem Connecting to gen.lib.rus.ec")
	root.destroy()  
	
w = Label(root, text="Book Grabber using Tkinter and BeautifulSoup")
w.config(font=("Courier", 25,"bold"))
w.pack(side=TOP)


textBox=Entry(root,relief=RIDGE,borderwidth=2,justify='center')

textBox.pack(side=TOP,pady=7)
searchBtn=Button(root, height=1, width=20, text="Search" ,bg="grey", fg="black",command=lambda: retrieve_input())

searchBtn.pack(side=TOP,pady=4)
textBox2=Entry(root,relief=RIDGE,borderwidth=2,justify='center')
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
T.bind("<Button-1>", leftclick)
S.pack(side=RIGHT, fill=Y)
T.pack(side=LEFT, fill=Y)
S.config(command=T.yview)
T.config(yscrollcommand=S.set)
T.tag_config('failed', foreground='red')
T.tag_config('passed', foreground='yellow')




mainloop(  )    	