
import mouse
import keyboard
from threading import Thread
import time

def play(mouse_events,keyboard_events:list[keyboard.KeyboardEvent]):
    ptime=0
    #time1=0
    #time2=0
    events=mouse_events+keyboard_events

    events.sort(key=lambda x:x.time)

    for e in events:
        print(e)
        if ptime!=0:
            dtime=e.time-ptime
            #time1=time.time()
            #time_elapse_between_event=time2-time1
            #print(time_elapse_between_event)
            #ts=dtime-time_elapse_between_event
            #print(ts)
            time.sleep(dtime)
        ptime=e.time
        if type(e)==mouse.MoveEvent:
            #mouse.move(e.x,e.y)            
            mouse.play([e])
            #time2=time.time()
        elif type(e)==keyboard.KeyboardEvent:
            keyboard.play([e])

def _start_recording():
    mouse_events = []  
    print('wait')
    while True:
        key=keyboard.read_key()
        print(key)
        if key=='f12':
            mouse_events = []            
            mouse.hook(mouse_events.append)
            keyboard.start_recording()
            keyboard.wait("f12")
            mouse.unhook(mouse_events.append)
            keyboard_events = keyboard.stop_recording()  #Stopping the recording. Returns list of events
            del keyboard_events[-1]
            #print(keyboard_events)
            #print(mouse_events)
            print('end recording')
            time.sleep(1)
            continue
        elif key=='f11':
            play(mouse_events,keyboard_events)
            continue

        pass
    
    

def start_recording():
    
    t2=Thread(target=_start_recording,daemon=True)
    t2.start()
    print('out')
