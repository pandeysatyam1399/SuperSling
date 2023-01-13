from tkinter import *
from tkinter import Image 
import cv2  
from functools import partial  
from PIL import Image,ImageTk 
from itachIP2IR import *
from subprocess import call
import glob
#from tester import *

RACKNUMBER = 0

window = Tk()  
window.configure(bg="#000000")
# window.state('zoomed')

window.title("SuperSling 0.1.0")

def key_pressed(key):
    if key.char == key.keysym:
        OnKeyPress(key.char)
    else:
        OnKeyPress(key.keysym)

window.bind("<Key>",key_pressed)

mainFrame = Frame(window,bg="#000000")
mainFrame.grid(row=0,column=0)

btnArr =[]
remoteBtn = []
STB_NAME = StringVar()
STB_NAME = " STB NAME "

# video frame
videoFrame = Frame(mainFrame, width=940, height = 703,background= "#000000")
videoFrame.grid(row=2, column=0, padx=5, pady=2)
videoName = Label(videoFrame,text= STB_NAME,background= "#000000",width=100,height=3,fg="#FFFFFF",font=('Bold',16))
videoName.pack()
videoLabel = Label(videoFrame,background= "#000000")
videoLabel.pack()

# Rack Info
def getRack(*args):
    global RACKNUMBER
    RACKNUMBER = clicked.get()

# Remote Frame
remoteFrame = Frame(mainFrame,width=200,height=700)
remoteFrame.grid(row=0,column=100,rowspan=20,columnspan=3)

btnImageArr = []
j = 0

for img in glob.glob("images/*.png"):
    btnImageArr.append(cv2.imread(img))
    btnImageArr[j] = cv2.resize(btnImageArr[j],(45,45))
    btnImageArr[j] = ImageTk.PhotoImage( Image.fromarray(btnImageArr[j]))
    j+=1    

for i in range(0,39):
    remoteBtn.append(Button(remoteFrame,image=btnImageArr[i],bg="#000000",command=partial(OnRemotePress,i)))
    remoteBtn[i].grid(row=i//3, column=i%3)

# Single Window
def render_single_view(stb_no):
    if stb_no<16:
        stbNum = ( stb_no + 16 * ( int( RACKNUMBER.split(" ")[1] ) - 1) )
    else:
        stbNum = stb_no
    video_url = getRTSP(stbNum)
    stb_name = getSTBInfo(stbNum)
    print (video_url)  
    vcap = cv2.VideoCapture(video_url)
    videoName.config(text=str(stb_name))
    getData(stbNum)
    while(1):
        img = vcap.read()[1]
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        img = cv2.resize(img,(1280,720))
        img = ImageTk.PhotoImage(Image.fromarray(img))
        videoLabel['image'] = img
        window.update()  

# Supersling Monitor
def renderAll():
    out = call(["python","{}".format('multistreamsolution.py'),"{}".format(RACKNUMBER)])
    print(out)

# STB selection window
def optionView():
    top = Toplevel()
    top.title("STB Selector")
    top.configure(bg="#000000")
    centerFrame = Frame(top,width=1280,height=720,bg="#000000")
    centerFrame.grid(row=0,column=0,padx=20,pady=100)
    rackFrame = Frame(centerFrame,width=200,height=700,bg="#373737")
    rackFrame.grid(row=0,column=0)
    stbFrame = Frame(centerFrame,width=1040,height=700,bg="#373737")
    stbFrame.grid(row=0,column=1)
    btnRack = []
    rackInfo = []
    
    def accessAndDestroy(stb_no,rackNum):
        global RACKNUMBER
        top.quit()
        top.destroy()
        RACKNUMBER = rackNum
        clicked.set(RACKNUMBER)
        render_single_view(stb_no)
    
    def rackView(rackNum):
        btnStb = []
        stbCount = fetchSTB(rackNum)
        for i in rackInfo[int(rackNum.split(" ")[1])-1]:
            btnStb.append(Button(stbFrame,text=i,font=('Bold',14),width=30,pady=10,fg= "#fdfdfd" , activeforeground= "#9e4cef",activebackground= "#9e4cef",background= "#621ee8"))
        for i in range(0,len(btnStb)):
            btnStb[i].config(command=partial(accessAndDestroy,stbCount[i]-1,rackNum))
            if i % 4==0:
                btnStb[i].grid(row=i//4,column=i%4)
            else:
                btnStb[i].grid(row=i//4,column=i%4)
    
    cnt = getRackCount()
    for i in cnt:
        rackInfo.append(getRackInfo(i))
        btnRack.append(Button(rackFrame,text=i,font=('Bold',14),pady=10,command=partial(rackView,i),fg= "#fdfdfd" , activeforeground= "#9e4cef",activebackground= "#9e4cef",background= "#621ee8"))
    for i in range(0,len(btnRack)):
        btnRack[i].grid(row=i,column=0)
    
    rackView('Rack 1')

# Button Frame
btnFrame = Frame(mainFrame, width=200, height = 5)
btnFrame.grid(row=0, column=0, padx=5, pady=2)

clicked = StringVar()
clicked.trace_add('write',getRack)
clicked.set("Rack 1")

rackBtn = OptionMenu(btnFrame, clicked ,*list(getRackCount()))
rackBtn.config(height=2 , width= 12,fg= "#fdfdfd" , activeforeground= "#9e4cef",activebackground= "#9e4cef",background= "#BF55EC")
btnArr.append(rackBtn)          
btnArr[0].grid(row=0, column=0)

# 16 buttons
for i in range(0,18):
    if i < 16:
        btnArr.append(Button(btnFrame,text = "STB "+str(i+1),command = partial(render_single_view,i) , height=2 , width= 8,fg= "#fdfdfd" , activeforeground= "#9e4cef",activebackground= "#9e4cef",background= "#621ee8"))
        btnArr[i+1].grid(row=0, column=i+1)
    elif i == 16:
        btnArr.append(Button(btnFrame,text = "All STB",command =renderAll ,height=2, width=10 , fg= "#fdfdfd", activeforeground= "#9e4cef",activebackground= "#9e4cef",background= "#621ee8"))  
        btnArr[i+1].grid(row=0, column=i+1)
    else:
        btnArr.append(Button(btnFrame,text = "INFO",command =optionView ,height=2, width=10 , fg= "#fdfdfd", activeforeground= "#9e4cef",activebackground= "#9e4cef",background= "#621ee8"))  
        btnArr[i+1].grid(row=0, column=i+1)

def RunSuperSling():
    render_single_view(0)

    window.mainloop()
