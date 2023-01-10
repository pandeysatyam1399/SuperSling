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
        # print(err)
    elif btnNumber > 2 and btnNumber < 12:
        code = str(btnNumber-2)
        err = sendData(code)
        # print(err)
    elif btnNumber == 12:
        code = "dayback"
        err = sendData(code)
        # print(err)
    elif btnNumber == 13:
        code = "0"
        err = sendData(code)
        # print(err)
    elif btnNumber == 14:
        code = "dayforward"
        err = sendData(code)
        # print(err)
    elif btnNumber == 15:
        code = "volumeup"
        err = sendData(code)
        # print(err)
    elif btnNumber == 16:
        code = "arrowup"
        err = sendData(code)
        # print(err)
    elif btnNumber == 17:
        code = "vod"
        err = sendData(code)
        # print(err)
    elif btnNumber == 18:
        code = "arrowleft"
        err = sendData(code)
        # print(err)
    elif btnNumber == 19:
        code = "ok"
        err = sendData(code)
        # print(err)
    elif btnNumber == 20:
        code = "arrowright"
        err = sendData(code)
        # print(err)
    elif btnNumber == 21:
        code = "volumedown"
        err = sendData(code)
        # print(err)
    elif btnNumber == 22:
        code = "arrowdown"
        err = sendData(code)
        # print(err)
    elif btnNumber == 23:
        code = "ondemand"
        err = sendData(code)
        # print(err)
    elif btnNumber == 24:
        code = "a"
        err = sendData(code)
        # print(err)
    elif btnNumber == 25:
        code = "b"
        err = sendData(code)
        # print(err)
    elif btnNumber == 26:
        code = "c"
        err = sendData(code)
        # print(err)
    elif btnNumber == 27:
        code = "rewind"
        err = sendData(code)
        # print(err)
    elif btnNumber == 28:
        code = "play"
        err = sendData(code)
        # print(err)
    elif btnNumber == 29:
        code = "fastforward"
        err = sendData(code)
        # print(err)
    elif btnNumber == 30:
        code = "record"
        err = sendData(code)
        # print(err)
    elif btnNumber == 31:
        code = "pause"
        err = sendData(code)
        # print(err)
    elif btnNumber == 32:
        code = "stop"
        err = sendData(code)
        # print(err)
    elif btnNumber == 33:
        code = "exit"
        err = sendData(code)
        # print(err)
    elif btnNumber == 34:
        code = "guide"
        err = sendData(code)
        # print(err)
    elif btnNumber == 35:
        code = "info"
        err = sendData(code)
        # print(err)
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


