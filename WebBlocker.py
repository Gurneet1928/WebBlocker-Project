#!/usr/bin/env python
# coding: utf-8

# In[14]:


from tkinter import *
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
import mysql.connector
import tkinter as GUI


#-------CONNECTING SQL TO PYTHON NOTEBOOK----------
mydb = mysql.connector.connect(
  host="localhost",            
  user="gurneet",             #CHANGE USERNAME to you own pc's database
  password="admin",           #CHANGE PASSWORD to you own pc's database
  database="websitedb"        #CHANGE DATABASE NAME to you own pc's database
)

mycursor = mydb.cursor(buffered=True)
mycursor.execute("CREATE DATABASE IF NOT EXISTS websitedb")                   #CHECK IF DATABASE EXISTS , otherwise make a new one
mycursor.execute("CREATE TABLE IF NOT EXISTS websitedata(webnum int ,websname VARCHAR(255))")              #CHECK IF TABLE EXISTS , otherwise make a new one
#mycursor.execute("truncate websitedata" )         #IMPORTANT FUNCTION - CAN BE USED TO CLEAR ALL THE DATA IN TABLE IF REQUIRED


#-------WINDOW INTIALIZATION AND GLOBAL VARIABLE DECLARATION----------
window = tk.Tk()
window.title("WEBSITE BLOCKER")
window.geometry('700x500')
wb=StringVar()
webid=IntVar()
k=0
host_path = "C:\Windows\System32\drivers\etc\hosts"  
redirect = "127.0.0.1"
blank=" "
nxt="\n"

#-------FINDING CURRENT COUNT OF WEBSITES AND MAX VALUES----------
mycursor.execute("SELECT MAX(webnum) FROM websitedata")
value = mycursor.fetchone()
print(value)
value=max(value)
print(value)
if value is not None:
    count=value
    i=value
else:
    count=0
    i=0

#-------MAKING TAB FRAME AND CONTROLS----------
TAB_CONTROL = ttk.Notebook(window)
TAB_CONTROL.pack(expand=1, fill="both",pady=10,padx=5)

#-------TAB STYLING----------
s = ttk.Style()
s.configure('TNotebook.Tab', font=('Georgia','10','bold'))
s.configure('TNotebook', font=('URW Gothic L','10','bold'))


#-------Tab1----------
AddWeb = ttk.Frame(TAB_CONTROL)
TAB_CONTROL.add(AddWeb, text='  Add Websites to List  ')

#-------Tab2----------
RemWeb = ttk.Frame(TAB_CONTROL)
TAB_CONTROL.add(RemWeb,text="  Remove Websites From List  ")


#-------Tab3----------
Abus = ttk.Frame(TAB_CONTROL)
TAB_CONTROL.add(Abus,text=" About Program and Us  ")


#-------Tab4----------
Quit = ttk.Frame(TAB_CONTROL)
TAB_CONTROL.add(Quit,text="  Quit Program  ")



#---------------------------------TAB 1/ADD WEBSITES DATA-----------------------------------

#--------------------Instructions to operate----------------
Label(AddWeb, text="\n\nADD THE WEBSITES THAT YOU NEED TO BLOCK",font='Georgia').grid(column=2, row=0, padx=10,pady=10)
Label(AddWeb, text="Make sure to follow the following format",font='Georgia').grid(column=2, row=1, padx=10,pady=5)   
Label(AddWeb, text="www.example.com",font='Georgia').grid(column=2, row=2, padx=10)
Label(AddWeb, text="\tAND THEN CLICK **ADD WEBSITE** BUTTON BELOW",font='Georgia').grid(column=2, row=3, padx=10,pady=5)   

def addweb():  #Function for adding webpage in list,file & messagebox
    webname=wb.get()
    if 'www' not in webname :
        messagebox.showinfo("Failure"," Webiste format not followed !!")
    else:
        global count
        count+=1
        sql = "INSERT INTO websitedata (webnum,websname) VALUES (%s,%s)"
        val = webname
        mycursor.execute(sql,(count,webname,))
        mydb.commit()
        mycursor.execute("SELECT websname from websitedata")
        webdata=mycursor.fetchall() 
        with open(host_path,"r+") as fileptr:  
            content = fileptr.read()
            weblist=list(content)
            addweb=val  
            if val in weblist:  
                pass  
            else:
                addthis=redirect+blank+addweb+nxt
                fileptr.write(addthis) 
                messagebox.showinfo("Success"," Webiste added into list !!")


#--------------MENU FOR ADDING WEBSITE--------------
lab=Label(AddWeb,text="Enter the website here !!",font='Georgia').grid(row=4,column=2)
nam=Entry(AddWeb,textvariable=wb,bd=6,width=45,fg='red',font='Georgia',justify='center').grid(row=5,column=2,padx=10)
sub=Button(AddWeb,text="\t\tAdd website\t\t",bd=6,command=addweb,font='Georgia').grid(row=6,column=2)


#---------------------------------TAB 2/REMOVE WEBSITES DATA-----------------------------------

def clrframe():   #Clears frame before rewriting it
    for widget in refframe.winfo_children():
        widget.destroy()


def updatelist(): #Function of updating list on click of refresh button
    clrframe()
    mycursor.execute("SELECT * FROM websitedata")
    global i
    global k
    for x in mycursor: 
        dat=StringVar()
        dat=x
        e = Label(refframe,text=dat,width=25, fg='blue',font='Georgia', relief=GROOVE,pady=5 ) 
        e.grid(row=k,column=1) 
        k=k+1
            
def remwebs2():  #Function for removing webpages
    val=int(webid.get())
    cmd="SELECT websname FROM websitedata WHERE webnum = %s"
    mycursor.execute(cmd,(val,))
    webdata=mycursor.fetchone()
    if webdata is None:
        messagebox.showinfo("Error"," Webiste does not exist in list !!")
    else:
        remwebname=webdata[0]
        sql = "DELETE FROM websitedata WHERE webnum = %s"
        mycursor.execute(sql,(val,))
        mydb.commit()
        remthis=redirect+blank+webdata[0]+nxt
        with open(host_path, "r") as f:
            lines = f.readlines()
        with open("C:\Windows\System32\drivers\etc\host_path_temp.txt", "w") as f:
            for line in lines:
                if line != remthis:
                    f.write(line)
        with open("C:\Windows\System32\drivers\etc\host_path_temp.txt", "r") as f:
            lines = f.readlines()
        with open(host_path, "w") as f:
            for line in lines:
                f.write(line)
        messagebox.showinfo("Success"," Webiste removed from the list !!")

#-----------SEPERATE FRAME FOR DISPLAYING WEBSITES----------------
refframe = tk.Frame(RemWeb,bg="white") 
refframe.config()  
refframe.grid(row=4,column=1)  


#-------------Code Block for showing webpages---------------
Button(RemWeb,text="Refresh Page",command=updatelist,font='Georgia').grid(row=3,column=1)
Label(RemWeb,text="List of blocked websites!! \n If website not visible\nThen click Refresh Button",font='Georgia',bd=3,width=25,relief=RAISED ).grid(row=0,column=1)
Label(RemWeb,text="\nEnter the S.no of website to be removed and Click the button\n",font='Georgia',relief=RAISED,bd=3).grid(row=0,column=2)
sendwebnum=Button(RemWeb,text="Remove website",command=remwebs2,font='Georgia',relief=RAISED,bd=3 ).grid(row=3,column=2)
Entry(RemWeb,textvariable=webid,font='Georgia',bd=3).grid(row=2,column=2)


#---------------------------------TAB 3/ABOUT US-----------------------------------
Label(Abus,text="\n\tThis is a simple WEB BLOCKER Program with the aim to restrict the user\n\n\tfrom visitng some specific sites on web\n",font='Georgia').grid(row=2,column=2)
Label(Abus,text="\tThis Program is totally made for educational Purpose",font='Georgia').grid(row=3,column=2)
Label(Abus,text="\tThe user is solely responsible for misuse of such programs",font='Georgia').grid(row=4,column=2)
Label(Abus,text="\n\n\n\t About the Programmer",font='Georgia').grid(row=5,column=2)
Label(Abus,text="\tThis program was made by Gurneet Singh as a part of his INT213 Project",font='Georgia').grid(row=6,column=2)
Label(Abus,text="\tThe programmer has a keen interest in coding and technical stuff",font='Georgia').grid(row=7,column=2)
Label(Abus,text="\tThis program was made successful with the help of following websites :: ",font='Georgia').grid(row=8,column=2)
Label(Abus,text="\tgoogle.com \n\n\tstackoverflow \n\n\twww.pythontutorial.net",font='Georgia').grid(row=9,column=2)



#---------------------------------TAB 4/Exit Program-----------------------------------
def quitpro():
    window.destroy()

Label(Quit,text="Click yes if you want to quit the program",font='Georgia',bd=6, relief=GROOVE,height=5,width=50).grid(row=2,column=2)
choice=Button(Quit,text="YESSSS",command=quitpro,font='Georgia',bd=6, relief=RAISED,height=5,width=50).grid(row=3,column=2)



#---------------------------------END OF TABS-----------------------------------
#Calling Main()
window.mainloop()


# In[ ]:




