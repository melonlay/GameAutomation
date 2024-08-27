import dearpygui.dearpygui as dpg
import os
import PIL
import numpy as np


#on clicking the image, display the image on the image panel
def on_click(sender, app_data,user_data):
    width, height, channels, data = dpg.load_image(user_data)
    dpg.delete_item('image',children_only=True)
    dpg.delete_item('texture')
    with dpg.texture_registry():
        dpg.add_raw_texture(width=width,height=height,default_value=data,tag='texture')
        dpg.add_image("texture",parent='image')

def show_data_window(data_path):
    with dpg.window(label="FileList", pos=(0,0),width=400,height=800):
        def recursive_list_file_and_folder(folder):
            fn_list=os.listdir(folder)
            for fn in fn_list:
                full_path=f'{folder}/{fn}'
                if os.path.isdir(full_path):
                    with dpg.collapsing_header(label=fn):
                        recursive_list_file_and_folder(full_path)
                else:
                    dpg.add_selectable(label=fn,tag=full_path,callback=on_click)
                    dpg.set_item_user_data(full_path,full_path)

        recursive_list_file_and_folder(data_path)    
        #dpg.add_selectable(label='a')
    
    with dpg.window(label="Image", pos=(400,0),height=800,width=800,tag='image'):
        #dpg.add_static_texture(width=width, height=height, default_value=data, tag="texture_tag")
        empty=np.ones( (1,800*800*3),dtype=np.float32 )
        #print(empty)
        #print(empty)
        #width, height, channels, data = dpg.load_image('./dummy.png')
        #print(type(empty),type(data))
        with dpg.texture_registry():
            dpg.add_raw_texture(width=800,height=800,default_value=empty,tag='texture',format=dpg.mvFormat_Float_rgb)
            dpg.add_image("texture",parent='image')
        #dpg.add_image
        pass
    