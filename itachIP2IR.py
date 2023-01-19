import pandas as pd
import socket
import supersling_config as ssc

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
    keyMap = None
    buttonMap = None
    
    def __init__(self) -> None:
        # button press config
        self.buttonMap = ssc.button_config()
        # Key Press config
        self.keyMap = ssc.key_config()
        # IR codes
        self.itachCodes = pd.read_csv('ir_codes_itach.txt',delimiter="|",names=['remote_type','itachCode','nothing'],on_bad_lines='skip')
        # Database
        self.dattDB = pd.read_csv('datt_lite_DB.txt',delimiter="|",comment='#',names=['STB_ID','iTach_IP','iTach_port','stb_type','STB_INFO','STB_IP','IsActive'],on_bad_lines='skip')
    
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
        # print("getting IP",data)
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
        
        # print("get all rack info",rack)  
        return rack
    
    '''get all STB in Particular Rack'''
    def getRackInfo(self,rack):
        # print("rack info ",rack)
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
        try:
            self.sendData(self.buttonMap[str(btnNumber)])
        except:
            print("Not correct button Press ",btnNumber)
            pass
              

    '''Key Press'''
    def OnKeyPress(self,key):
        try:
            self.sendData(self.keyMap[key.lower()])
        except:
            print("Not correct Key Press ",key)
            pass
        