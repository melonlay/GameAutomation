
import mouse
import keyboard
from threading import Thread
import time
import pydirectinput
from pynput import mouse as mouse2
 
import win32api
import win32gui
import pyautogui

class MoveEvent:
    def __init__(self,dx=0,dy=0,time=0):
        self.x=dx
        self.y=dy
        self.dx=dx
        self.dy=dy
        self.time=time

    def __str__(self):
        return f'MoveEvent(({self.dx},{self.dy}),time={self.time})'

def global_break(key='f10'):
    if keyboard.is_pressed(key):
        print('force exit replay')
        time.sleep(1)
        return True
    return False

def play_mouse(mouse_events):
    firstRecordTime=0
    firstPlayTime=time.time()
    events=mouse_events
    Xmin,Ymin,Xmax , Ymax=win32gui.GetWindowRect(win32gui.FindWindow(None, utils.WNAME))
    print('start replay mouse')
    for e in events:
        dtime=0
        if global_break():
            return
        if firstRecordTime==0:
            firstRecordTime=e.time
            #time.sleep(dtime)
            #print(dtime)
        else:
            dRecordTime=e.time-firstRecordTime
            dPlayTime=time.time()-firstPlayTime
            if dRecordTime-dPlayTime>0.005:
                time.sleep(max(dRecordTime-dPlayTime,0))

        ptime=e.time
        if type(e)==MoveEvent:
            if global_break():
                return        
            mouse._os_mouse.move_relative(e.dx,e.dy)
    print('end replay mouse')
    
def play_keyboard(keyboard_events:list[keyboard.KeyboardEvent]):
    firstRecordTime=0
    firstPlayTime=time.time()
    events=keyboard_events

    #events.sort(key=lambda x:x.time)
    Xmin,Ymin,Xmax , Ymax=win32gui.GetWindowRect(win32gui.FindWindow(None, utils.WNAME))
    print('start replay keyboard')
    for e in events:
        dtime=0
        if firstRecordTime==0:
            firstRecordTime=e.time
            #time.sleep(dtime)
            #print(dtime)
        else:
            dRecordTime=e.time-firstRecordTime
            dPlayTime=time.time()-firstPlayTime
            if dRecordTime-dPlayTime>0.005:
                time.sleep(max(dRecordTime-dPlayTime,0))
        if global_break():
            return
        if type(e)==keyboard.KeyboardEvent:
            keyboard.play([e])    
    print('end replay keyboard')        


import pyWinhook as pyHook

import utils


STORAGE=[]
RECORDING=False
def record_when_captured_mouse():#gets color of whats under Key cursor on right click   
    global STORAGE,RECORDING 
    print('start recording mouse')
    prevX,prevY=0,0
    Xmin,Ymin,Xmax , Ymax=win32gui.GetWindowRect(win32gui.FindWindow(None, utils.WNAME))
    print(Xmin,Ymin,Xmax , Ymax)
    t1=0
    t2=0
    while RECORDING:  
        t1=time.time()
        if t2!=0:
            time.sleep(0.01-(t2-t1))
        t2=time.time()
        Xpos,Ypos=mouse._os_mouse.get_position()
        if prevX==0 and prevY==0:
            (dx,dy)=(0,0)
        else:
            (dx,dy)=(Xpos-prevX,Ypos-prevY)
        STORAGE.append(MoveEvent(dx,dy,time.time()))
        if Xpos<100 or Xpos>Xmax-100:
            win32api.SetCursorPos((Xmax//2,Ypos))
        if Ypos<100  or Ypos>Ymax-100:
            win32api.SetCursorPos((Xpos,Ymax//2))
        prevX,prevY = win32api.GetCursorPos()

        '''Xpos, Ypos = win32api.GetCursorPos()
        
        #print(Xpos, Ypos)
        if prevX==0 and prevY==0:
            (dx,dy)=(0,0)
        else:
            (dx,dy)=(Xpos-prevX,Ypos-prevY)
        STORAGE.append(MoveEvent(dx,dy,time.time()))
        if Xpos<100 or Xpos>Xmax-100:
            win32api.SetCursorPos((Xmax//2,Ypos))
        if Ypos<100  or Ypos>Ymax-100:
            win32api.SetCursorPos((Xpos,Ymax//2))
        prevX,prevY = win32api.GetCursorPos()
        time.sleep(0.01)'''
        
        #print(mouse._os_mouse.get_position())
    print('end recording mouse')

def record_mouse():
    while RECORDING:        
        Xpos, Ypos = win32api.GetCursorPos()
        #print(Xpos, Ypos)
        if Xpos<100:
            win32api.SetCursorPos((800,Ypos))
        time.sleep(0.01)

def _start_recording_mouse():
    global STORAGE,RECORDING 
    STORAGE=[]  
    RECORDING=True
    t=Thread(target=record_when_captured_mouse,daemon=True)
    t.start()
def _stop_recording_mouse(): 
    global STORAGE,RECORDING 
    RECORDING=False

def _start_recording():
    global STORAGE,RECORDING
    print('wait')
    REPLAYING=False
    while True:
        key=keyboard.read_key()
        print(key)
        if key=='f12':
            print('start recording')                
            _start_recording_mouse()


            keyboard.start_recording()
            keyboard.wait("f12")
            #hm.UnhookMouse()
            _stop_recording_mouse()
            print(STORAGE)
            keyboard_events = keyboard.stop_recording()  #Stopping the recording. Returns list of events
            pressed=set()
            new_keyboard_events=[]
            for e in keyboard_events:
                #print(e.name,e.event_type)
                if e.name=='f12':
                    continue                
                if e.event_type=='down':
                    if e.name in pressed:
                        pass
                        #continue                    
                    else:
                        pressed.add(e.name)
                elif e.event_type=='up':
                    if e.name in pressed:                        
                        pressed.remove(e.name)
                new_keyboard_events.append(e)


            for e in new_keyboard_events:
                print(e.name,e.event_type,e.time)
            #del keyboard_events[-1]
            #print(keyboard_events)
            #print(mouse_events)
            print('end recording')
            #for e in mouse_events:
            #    print(e)
            #print(mouse_events)
            time.sleep(1)
            continue
        elif key=='f11':
            t1=Thread(target=play_mouse,args=(STORAGE,),daemon=True)
            t2=Thread(target=play_keyboard,args=(new_keyboard_events,),daemon=True)
            #play_mouse(STORAGE,new_keyboard_events)
            #play_mouse(STORAGE,new_keyboard_events)
            t1.start()
            t2.start()
            t1.join()
            t2.join()
            continue

        pass
    
    

def start_recording():
    
    t2=Thread(target=_start_recording,daemon=True)
    t2.start()
    print('out')

storage = []

'''def on_move(x,y):
    global storage
    json_object = {'action':'moved', 'x':x, 'y':y, '_time':time.time()}
    storage.append(json_object)
    print(json_object)
    mouse2._os_mouse.move_to(400,400)

def pyn():
    mouse_listener = mouse2.Listener(
        on_move=on_move)
    mouse_listener.start()'''
   
   

if __name__=='__main__':

    
    
    while True:
        time.sleep(1)
        pass