import pandas as pd
import socket

# globals
remote_type = 0
itach_port = 0
code = 0
repeat = 0
itach_IP = 0
data = 0
itachCode = 0

# IR codes
itachCodes = pd.read_csv('ir_codes_itach.txt',delimiter="|",names=['remote_type','itachCode','nothing'],on_bad_lines='skip')

# Database 
dattDB = pd.read_csv('datt_lite_DB.txt',delimiter="|",skiprows=1,names=['STB_ID','iTach_IP','iTach_port','stb_type','STB_INFO','STB_IP','IsActive'],on_bad_lines='skip')
print(dattDB)
# irk functionality
def getData(stb_no):
    global remote_type,itach_IP,itach_port
    data = dattDB.iloc[stb_no]
    remote_type = data.get("stb_type")
    itach_port = data.get("iTach_port")
    itach_IP = data.get("iTach_IP")

def sendData(onPress):
    global remote_type,itach_IP,itach_port
    out = 0
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Charter Motorola:guide
    data = getItachCodes("Charter Motorola:"+ str(onPress))
    # "sendir,1:"+ itach port number +",111,frequency,repeat,1,"+ itach code +"\r"
    dataToSend = "sendir,1:"+ str(itach_port) +",111,38109,1,1,"+ data +"\r"
    s.connect((itach_IP, 4998))
    s.sendall(dataToSend.encode())
    out = str(s.recv(1024).decode())
    s.close()
    return out

def getItachCodes(remote_data):
    data = itachCodes.loc[itachCodes['remote_type']==remote_data]
    data = data['itachCode'].tolist()
    itachCode = "{}".format(*data)
    return itachCode

def getSTBIP(stbno):
    data = dattDB.iloc[stbno].get("STB_IP")
    return data
    
def getRTSP(stbno):
    IP = getSTBIP(stbno)
    return "rtsp://root:admin@"+ IP +"/axis-media/media.amp"

def getSTBInfo(stbno):
    return dattDB.iloc[stbno].get("STB_INFO")

def getAllInfo():
    data =  dattDB["STB_INFO"].to_list()
    rack = []
    for item in data:
        item = item.split("-")
        rack.append(item)
    # print(rack)
    return rack
    
def getRackInfo(rack):
    data = getAllInfo()
    return [item[3] for item in data if item[0] == rack]

def fetchSTB(rack):
    # get all STB_ID of specified Rack
    return [k for k,v in dict(zip(dattDB['STB_ID'].to_list(),[item[0] for item in getAllInfo()])).items() if v==rack] 

def getRackCount():
    data = getAllInfo()
    return pd.unique([item[0] for item in data])
    

# Remote Function
def OnRemotePress(btnNumber):
    code = ""
    if btnNumber == 0:
        code = "power"
        err = sendData(code)
        
    elif btnNumber > 2 and btnNumber < 12:
        code = str(btnNumber-2)
        err = sendData(code)
        
    elif btnNumber == 12:
        code = "dayback"
        err = sendData(code)
        
    elif btnNumber == 13:
        code = "0"
        err = sendData(code)
        
    elif btnNumber == 14:
        code = "dayforward"
        err = sendData(code)
        
    elif btnNumber == 15:
        code = "volumeup"
        err = sendData(code)
        
    elif btnNumber == 16:
        code = "arrowup"
        err = sendData(code)
        
    elif btnNumber == 17:
        code = "vod"
        err = sendData(code)
        
    elif btnNumber == 18:
        code = "arrowleft"
        err = sendData(code)
        
    elif btnNumber == 19:
        code = "ok"
        err = sendData(code)
        
    elif btnNumber == 20:
        code = "arrowright"
        err = sendData(code)
        
    elif btnNumber == 21:
        code = "volumedown"
        err = sendData(code)
        
    elif btnNumber == 22:
        code = "arrowdown"
        err = sendData(code)
        
    elif btnNumber == 23:
        code = "ondemand"
        err = sendData(code)
        
    elif btnNumber == 24:
        code = "a"
        err = sendData(code)
        
    elif btnNumber == 25:
        code = "b"
        err = sendData(code)
        
    elif btnNumber == 26:
        code = "c"
        err = sendData(code)
        
    elif btnNumber == 27:
        code = "rewind"
        err = sendData(code)
        
    elif btnNumber == 28:
        code = "play"
        err = sendData(code)
        
    elif btnNumber == 29:
        code = "fastforward"
        err = sendData(code)
        
    elif btnNumber == 30:
        code = "record"
        err = sendData(code)
        
    elif btnNumber == 31:
        code = "pause"
        err = sendData(code)
        
    elif btnNumber == 32:
        code = "stop"
        err = sendData(code)
        
    elif btnNumber == 33:
        code = "exit"
        err = sendData(code)
        
    elif btnNumber == 34:
        code = "guide"
        err = sendData(code)
        
    elif btnNumber == 35:
        code = "info"
        err = sendData(code)
        
    elif btnNumber == 36:
        code = "last"
        err = sendData(code)
    elif btnNumber == 37:
        code = "mute"
        err = sendData(code)
    elif btnNumber == 38:
        code = "menu"
        err = sendData(code)
    return

def OnKeyPress(key):
    code = ""
    print(key)
    if key == 'g' or key == 'G': # guide
        code = "guide"
        err = sendData(code)
        
    elif key == 'Escape': # exit
        code = "exit"
        err = sendData(code)
        
    elif key == 'space' or key =='Return': # select
        code = "select"
        err = sendData(code)
        
    elif key == 'p' or key == 'P': # power
        code = "power"
        err = sendData(code)
        
    elif key == '1': # number 1
        code = "1"
        err = sendData(code)
        
    elif key == '2': # number 2
        code = "2"
        err = sendData(code)
        
    elif key == '3': # number 3
        code = "3"
        err = sendData(code)
        
    elif key == '4': # number 4
        code = "4"
        err = sendData(code)
        
    elif key == '5': # number 5
        code = "5"
        err = sendData(code)
        
    elif key == '6': # number 6
        code = "6"
        err = sendData(code)
        
    elif key == '7': # number 7
        code = "7"
        err = sendData(code)
        
    elif key == '8': # number 8
        code = "8"
        err = sendData(code)
        
    elif key == '9': # number 9
        code = "9"
        err = sendData(code)
        
    elif key == '0': # number 0
        code = "0"
        err = sendData(code)
        
    elif key == 'plus': # channel up
        code = "channelup"
        err = sendData(code)
        
    elif key == 'minus': # channel down
        code = "channeldown"
        err = sendData(code)
        
    elif key == 'm' or key == 'M': # mute
        code = "mute"
        err = sendData(code)
        
    elif key == 'i' or key == 'I': # info
        code = "info"
        err = sendData(code)
        
    elif key == 'u' or key == 'U': # menu
        code = "menu"
        err = sendData(code)
        
    elif key == 'v'or key == 'V': # vod
        code = "vod"
        err = sendData(code)
        
    elif key == 'Up': # arrow up
        code = "arrowup"
        err = sendData(code)
        
    elif key == 'Down': # arrow down
        code = "arrowdown"
        err = sendData(code)
        
    elif key == 'Left': # arrow left
        code = "arrowleft"
        err = sendData(code)
        
    elif key == 'Right': # arrow right
        code = "arrowright"
        err = sendData(code)
        
    elif key == 'bracketright': # ]
        code = "dayforward"
        err = sendData(code)
        
    elif key == 'bracketleft': # [
        code = "dayback"
        err = sendData(code)
        
    elif key == 'a' or key == 'A': # A
        code = "a"
        err = sendData(code)
        
    elif key == 'b' or key == 'B': # B
        code = "b"
        err = sendData(code)
        
    elif key == 'c' or key == 'C': # C
        code = "c"
        err = sendData(code)
        
    elif key == 'w' or key == 'W': # swap
        code = "swap"
        err = sendData(code)
        
    elif key == 'r' or key == 'R': # record
        code = "record"
        err = sendData(code)
        
    elif key == 'x' or key == 'X': # stop
        code = "stop"
        err = sendData(code)
        
    elif key == 'comma': # rewind
        code = "rewind"
        err = sendData(code)
        
    elif key == 'slash': # play
        code = "play"
        err = sendData(code)
         
    elif key == 'semicolon': # pause
        code = "pause"
        err = sendData(code)
        
    elif key == 'period': # fast-forward
        code = "fastforward"
        err = sendData(code)
        
    elif key == 'f' or key == 'F': # fav
        code = "fav"
        err = sendData(code)
        
    elif key == 'd' or key == 'D': # list
        code = "list"
        err = sendData(code)
        
    elif key == 'l' or key == 'L': # last
        code = "last"
        err = sendData(code)
        
    # elif key == 'h' or key == 'H': # help
    #     code = "help"
    #     err = sendData(code)
        
    elif key == 'e' or key == 'E': # live
        code = "live"
        err = sendData(code)
        
    elif key == 'Prior': # page up
        code = "pageup"
        err = sendData(code)
        
    elif key == 'Next': #  page down
        code = "pagedown"
        err = sendData(code)
        
    elif key == 'greater': # volume up
        code = "volumeup"
        err = sendData(code)
        
    elif key == 'less': # volume down
        code = "volumedown"
        err = sendData(code)
        
    
    
