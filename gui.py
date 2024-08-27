import os
import dearpygui.dearpygui as dpg
from dearpygui.demo import show_demo
import numpy as np
from config import read_config
from datalist_window import show_data_window
from process_window import show_process_window
from recording import start_recording
#dpg.add

Config=read_config()
data_path=Config['DEFAULT']['data_path']


'''
with dpg.font_registry():
    with dpg.font("C:\Windows\Font\mingliu.ttc",20) as font:
        #dpg.add_font_range_hint(dpg.mvFontRangeHint_Chinese_Full)
        dpg.bind_font(font)'''

dpg.create_context()

with dpg.font_registry():
    #dpg.add_font("mingliu.ttc",20,default_font=True)
    with dpg.font("mingliu.ttc",12) as font:
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Chinese_Full)
        dpg.bind_font(font)

dpg.create_viewport()

dpg.setup_dearpygui()


#show_data_window(data_path)




#show_demo()
dpg.show_viewport()







show_process_window()
#start_recording()
dpg.start_dearpygui()

dpg.destroy_context()