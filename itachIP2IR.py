import pandas as pd
import socket

class itach:
    remote_type = None
    itach_port = None
    code = None
    repeat = None
    itach_IP = None
    data = None
    itachCode = None
    itachCodes = None
    dattDB = None
    
    def __init__(self) -> None:
        # IR codes
        self.itachCodes = pd.read_csv('ir_codes_itach.txt',delimiter="|",names=['remote_type','itachCode','nothing'],on_bad_lines='skip')
        # Database
        self.dattDB = pd.read_csv('datt_lite_DB.txt',delimiter="|",skiprows=1,names=['STB_ID','iTach_IP','iTach_port','stb_type','STB_INFO','STB_IP','IsActive'],on_bad_lines='skip')
    
    '''get Data From DB'''
    def getData(self,stb_no) -> None:
        data = self.dattDB.iloc[stb_no]
        self.remote_type = data.get("stb_type")
        self.itach_port = data.get("iTach_port")
        self.itach_IP = data.get("iTach_IP")
        self.data = self.getAllInfo()
    
    '''send to itach'''   
    def sendData(self,onPress) -> None:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Charter Motorola:guide
        if self.itachCode == None:
            self.getItachCodes("Charter Motorola:"+ str(onPress))
        else:
            pass
        # "sendir,1:"+ itach port number +",111,frequency,repeat,1,"+ itach code +"\r"
        dataToSend = "sendir,1:"+ str(self.itach_port) +",111,38109,1,1,"+ self.itachCode +"\r"
        s.connect((self.itach_IP, 4998))
        s.sendall(dataToSend.encode())
        
        self.itachCode = None
        
        if len(str(s.recv(1024).decode())) == 0:
            print("Error while sending itach code to ",self.itach_IP)
            
        s.close()
    
    '''get itach frequency codes'''
    def getItachCodes(self,remote_data) -> None:
        data = self.itachCodes.loc[self.itachCodes['remote_type']==remote_data]
        data = data['itachCode'].tolist()
        self.itachCode = "{}".format(*data)
    
    '''get STB IP'''    
    def getSTBIP(self,stbno):
        data = self.dattDB.iloc[stbno].get("STB_IP")
        return data
    
    '''get RTSP Link'''
    def getRTSP(self,stbno):
          IP = self.getSTBIP(stbno)
          return "rtsp://root:admin@"+ IP +"/axis-media/media.amp"
    
    '''get STB info'''
    def getSTBInfo(self,stbno):
        return self.dattDB.iloc[stbno].get("STB_INFO")
    
    '''get all STB info'''
    def getAllInfo(self):
        rack = []
        
        for item in self.dattDB["STB_INFO"].to_list():
            item = item.split("-")
            rack.append(item)
            
        return rack
    
    '''get all STB in Particular Rack'''
    def getRackInfo(self,rack):
        return [item[3] for item in self.data if item[0]==rack]
    
    '''get STB FROM rack'''
    def fetchSTB(self,rack):
        # get all STB_ID of specified Rack
        return [k for k,v in dict(zip(self.dattDB['STB_ID'].to_list(),[item[0] for item in self.getAllInfo()])).items() if v==rack] 
       
    '''get Rack Count'''
    def getRackCount(self):
        data = self.getAllInfo()
        return pd.unique([item[0] for item in data])
    
    '''Remote Press'''
    def OnRemotePress(self,btnNumber) -> None:
        if btnNumber == 0:
            self.code = "power"
            self.sendData(self.code)
            
        elif btnNumber > 2 and btnNumber < 12:
            self.code = str(btnNumber-2)
            self.sendData(self.code)
            
        elif btnNumber == 12:
            self.code = "dayback"
            self.sendData(self.code)
            
        elif btnNumber == 13:
            self.code = "0"
            self.sendData(self.code)
            
        elif btnNumber == 14:
            self.code = "dayforward"
            self.sendData(self.code)
            
        elif btnNumber == 15:
            self.code = "volumeup"
            self.sendData(self.code)
            
        elif btnNumber == 16:
            self.code = "arrowup"
            self.sendData(self.code)
            
        elif btnNumber == 17:
            self.code = "vod"
            self.sendData(self.code)
            
        elif btnNumber == 18:
            self.code = "arrowleft"
            self.sendData(self.code)
            
        elif btnNumber == 19:
            self.code = "ok"
            self.sendData(self.code)
            
        elif btnNumber == 20:
            self.code = "arrowright"
            self.sendData(self.code)
            
        elif btnNumber == 21:
            self.code = "volumedown"
            self.sendData(self.code)
            
        elif btnNumber == 22:
            self.code = "arrowdown"
            self.sendData(self.code)
            
        elif btnNumber == 23:
            self.code = "ondemand"
            self.sendData(self.code)
            
        elif btnNumber == 24:
            self.code = "a"
            self.sendData(self.code)
            
        elif btnNumber == 25:
            self.code = "b"
            self.sendData(self.code)
            
        elif btnNumber == 26:
            self.code = "c"
            self.sendData(self.code)
            
        elif btnNumber == 27:
            self.code = "rewind"
            self.sendData(self.code)
            
        elif btnNumber == 28:
            self.code = "play"
            self.sendData(self.code)
            
        elif btnNumber == 29:
            self.code = "fastforward"
            self.sendData(self.code)
            
        elif btnNumber == 30:
            self.code = "record"
            self.sendData(self.code)
            
        elif btnNumber == 31:
            self.code = "pause"
            self.sendData(self.code)
            
        elif btnNumber == 32:
            self.code = "stop"
            self.sendData(self.code)
            
        elif btnNumber == 33:
            self.code = "exit"
            self.sendData(self.code)
            
        elif btnNumber == 34:
            self.code = "guide"
            self.sendData(self.code)
            
        elif btnNumber == 35:
            self.code = "info"
            self.sendData(self.code)
            
        elif btnNumber == 36:
            self.code = "last"
            self.sendData(self.code)
        elif btnNumber == 37:
            self.code = "mute"
            self.sendData(self.code)
        elif btnNumber == 38:
            self.code = "menu"
            self.sendData(self.code)   

    '''Key Press'''
    def OnKeyPress(self,key):
        if key == 'g' or key == 'G': # guide
            self.code = "guide"
            self.sendData(self.code)
            
        elif key == 'Escape': # exit
            self.code = "exit"
            self.sendData(self.code)
            
        elif key == 'space' or key =='Return': # select
            self.code = "select"
            self.sendData(self.code)
            
        elif key == 'p' or key == 'P': # power
            self.code = "power"
            self.sendData(self.code)
            
        elif key == '1': # number 1
            self.code = "1"
            self.sendData(self.code)
            
        elif key == '2': # number 2
            self.code = "2"
            self.sendData(self.code)
            
        elif key == '3': # number 3
            self.code = "3"
            self.sendData(self.code)
            
        elif key == '4': # number 4
            self.code = "4"
            self.sendData(self.code)
            
        elif key == '5': # number 5
            self.code = "5"
            self.sendData(self.code)
            
        elif key == '6': # number 6
            self.code = "6"
            self.sendData(self.code)
            
        elif key == '7': # number 7
            self.code = "7"
            self.sendData(self.code)
            
        elif key == '8': # number 8
            self.code = "8"
            self.sendData(self.code)
            
        elif key == '9': # number 9
            self.code = "9"
            self.sendData(self.code)
            
        elif key == '0': # number 0
            self.code = "0"
            self.sendData(self.code)
            
        elif key == 'plus': # channel up
            self.code = "channelup"
            self.sendData(self.code)
            
        elif key == 'minus': # channel down
            self.code = "channeldown"
            self.sendData(self.code)
            
        elif key == 'm' or key == 'M': # mute
            self.code = "mute"
            self.sendData(self.code)
            
        elif key == 'i' or key == 'I': # info
            self.code = "info"
            self.sendData(self.code)
            
        elif key == 'u' or key == 'U': # menu
            self.code = "menu"
            self.sendData(self.code)
            
        elif key == 'v'or key == 'V': # vod
            self.code = "vod"
            self.sendData(self.code)
            
        elif key == 'Up': # arrow up
            self.code = "arrowup"
            self.sendData(self.code)
            
        elif key == 'Down': # arrow down
            self.code = "arrowdown"
            self.sendData(self.code)
            
        elif key == 'Left': # arrow left
            self.code = "arrowleft"
            self.sendData(self.code)
            
        elif key == 'Right': # arrow right
            self.code = "arrowright"
            self.sendData(self.code)
            
        elif key == 'bracketright': # ]
            self.code = "dayforward"
            self.sendData(self.code)
            
        elif key == 'bracketleft': # [
            self.code = "dayback"
            self.sendData(self.code)
            
        elif key == 'a' or key == 'A': # A
            self.code = "a"
            self.sendData(self.code)
            
        elif key == 'b' or key == 'B': # B
            self.code = "b"
            self.sendData(self.code)
            
        elif key == 'c' or key == 'C': # C
            self.code = "c"
            self.sendData(self.code)
            
        elif key == 'w' or key == 'W': # swap
            self.code = "swap"
            self.sendData(self.code)
            
        elif key == 'r' or key == 'R': # record
            self.code = "record"
            self.sendData(self.code)
            
        elif key == 'x' or key == 'X': # stop
            self.code = "stop"
            self.sendData(self.code)
            
        elif key == 'comma': # rewind
            self.code = "rewind"
            self.sendData(self.code)
            
        elif key == 'slash': # play
            self.code = "play"
            self.sendData(self.code)
            
        elif key == 'semicolon': # pause
            self.code = "pause"
            self.sendData(self.code)
            
        elif key == 'period': # fast-forward
            self.code = "fastforward"
            self.sendData(self.code)
            
        elif key == 'f' or key == 'F': # fav
            self.code = "fav"
            self.sendData(self.code)
            
        elif key == 'd' or key == 'D': # list
            self.code = "list"
            self.sendData(self.code)
            
        elif key == 'l' or key == 'L': # last
            self.code = "last"
            self.sendData(self.code)
            
        # elif key == 'h' or key == 'H': # help
        #     self.code = "help"
        #     self.sendData(self.code)
            
        elif key == 'e' or key == 'E': # live
            self.code = "live"
            self.sendData(self.code)
            
        elif key == 'Prior': # page up
            self.code = "pageup"
            self.sendData(self.code)
            
        elif key == 'Next': #  page down
            self.code = "pagedown"
            self.sendData(self.code)
            
        elif key == 'greater': # volume up
            self.code = "volumeup"
            self.sendData(self.code)
            
        elif key == 'less': # volume down
            self.code = "volumedown"
            self.sendData(self.code)
            
    