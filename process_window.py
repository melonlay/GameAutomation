import dearpygui.dearpygui as dpg
import os
import PIL
import numpy as np
import win32gui
import win32ui
import psutil
import ctypes
import cv2
from utils import capture_win_alt
from time import sleep
from threading import Thread
from collections import deque
from recording import start_recording

selected=""
current=""

def playVideo():
    global selected,current,buffer
    
    while True:
        #print(selected)
        if selected=="":
            continue        
        try:
            if selected!=current:
                img=capture_win_alt(selected)
                height,width,channel=img.shape
                ratio=min(800/width,800/height)
                img=cv2.resize(img,None,fx=ratio,fy=ratio)
                height,width,channel=img.shape
                data=np.reshape(img,(1,height*width*channel))            
            
                print('change')
                dpg.delete_item('video',children_only=True)
                dpg.delete_item('texture_video')
                with dpg.texture_registry():
                    dpg.add_raw_texture(width=width,height=height,default_value=data,tag='texture_video',format=dpg.mvFormat_Float_rgb)
                    dpg.add_image("texture_video",parent='video')
                current=selected
            else:
                img=capture_win_alt(selected,change=False)
                height,width,channel=img.shape
                ratio=min(800/width,800/height)
                img=cv2.resize(img,None,fx=ratio,fy=ratio)
                height,width,channel=img.shape
                data=np.reshape(img,(1,height*width*channel))      
                #sleep(0.05)
                dpg.set_value('texture_video',value=data)
                pass
        except Exception as e:
            print(e)
        

def winEnumHandler( hwnd, ret):
    if win32gui.IsWindowVisible( hwnd ):
        str=win32gui.GetWindowText( hwnd )
        #print(len(str))
        if len(str)>0:
            ret.append(str)
            #print ( hex( hwnd ), win32gui.GetWindowText( hwnd ) )
    
#on clicking the image, display the image on the image panel
def on_click(sender, app_data,user_data):
    global selected
    selected=user_data

def refresh(sender, app_data,user_data):
    dpg.delete_item('process',children_only=True)
    window_list=[]
    win32gui.EnumWindows( winEnumHandler, window_list )    
    for window in window_list:
        dpg.add_button(label=window,tag=window,callback=on_click,parent='process')
        dpg.set_item_user_data(window,window)

def recording(sender, app_data,user_data):
    start_recording()


def show_process_window():
    with dpg.window(label="WindowList", pos=(0,0),width=400,height=800):       
        dpg.add_button(label='refresh',tag='refresh',callback=refresh)
        dpg.add_button(label='recording',tag='recording',callback=recording)
        window_list=[]
        win32gui.EnumWindows( winEnumHandler, window_list )
        with dpg.collapsing_header(label='process',tag='process'):
            for window in window_list:
                dpg.add_button(label=window,tag=window,callback=on_click)
                dpg.set_item_user_data(window,window)
        
       
        #dpg.add_selectable(label='a')
    
    with dpg.window(label="video", pos=(400,0),height=800,width=800,tag='video'):
        #dpg.add_static_texture(width=width, height=height, default_value=data, tag="texture_tag")
        empty=np.ones( (1,800*800*3),dtype=np.float32 )
        #print(empty)
        with dpg.texture_registry():
            dpg.add_raw_texture(width=800,height=800,default_value=empty,tag='texture_video',format=dpg.mvFormat_Float_rgb)
        dpg.add_image("texture_video")
        #dpg.add_image
        print('aaa')
        t=Thread(target=playVideo,daemon=True)
        t.start()
        