#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
"""
Modulo: 
"""
__author__ = 'Sergio Cioban Filho'
__version__ = '1.0'
__date__ = '19/06/2015 06:41:40 PM'

from lib.grove_lcd_rgb import GROVE_LCD_RGB
from lib.button import BUTTON
from lib.wifi_controller import do_wifi_scan, do_wifi_info
from lib.navigation_menu import NAVIGATION_MENU
from lib.cloud import CLOUD
from time import sleep, time
from copy import copy


send_info_data = {}

def send_info():
    global send_info_data
    if len(send_info_data) > 0:
        cloud = CLOUD()
        cloud.send_info(copy(send_info_data))
        send_info_data = {}

def wifi_info_callback(cell_info):
    global send_info_data
    new_cell_info = do_wifi_info(cell_info)
    send_info_data[time()] = new_cell_info
    return new_cell_info

lcd = GROVE_LCD_RGB()
btn = BUTTON()
nav_menu = NAVIGATION_MENU(lcd, btn)
nav_menu.poll()
nav_menu.set_scan_callback(do_wifi_scan)
nav_menu.set_get_wifi_callback(wifi_info_callback)
nav_menu.set_send_info_callback(send_info)

try:
    while 1 == 1:
        btn.read()
        sleep(0.150)
        nav_menu.poll()
except KeyboardInterrupt:
    pass

