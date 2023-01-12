from pynput import keyboard
import itachIP2IR as ip2ir

STBNUM = 0

def onPress(key):
    if key == keyboard.Key.esc:
        return False
    try:
        k = key.char
    except:
        k = key.name
    if k in ['1','2','3','4','5','6','7','8','9','0','left','right','up','down','g','p','space','enter','i','v','u','r','a','b','c','d','m']:
        print(STBNUM)
        # ip2ir.getData(STBNUM)
        # ip2ir.OnRemotePressKey(str(k))
        print('key pressed: '+k)

def runner():
    listener = keyboard.Listener(on_press=onPress)
    listener.start()
    listener.join()

  
if __name__=='__main__':
    runner()
    