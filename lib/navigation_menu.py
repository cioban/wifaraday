#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
"""
Modulo: 
"""
__author__ = 'Sergio Cioban Filho'
__version__ = '1.0'
__date__ = '19/06/2015 05:08:32 PM'

from time import time
from copy import deepcopy


class NAVIGATION_MENU:
    lcd = None
    button = None
    force_clean = False

    KEY_LEFT = 8
    KEY_RIGHT = 9
    KEY_UP = 10
    KEY_DOWN = 11
    KEY_OK = 12

    menu_screens = [
        {'name': 'init', 'enable': True, 'lock': False },
        {'name': 'scan_wifi', 'enable': True, 'lock': False },
        {'name': 'wifi_total', 'enable': False, 'lock': False },
        {'name': 'wifi_list', 'enable': False, 'lock': False },
        ]
    menu_pos = 0
    last_menu_pos = -1

    wifi_pos = 0
    scan_callback = None
    get_wifi_callback = None
    send_info_callback = None
    wifi_cells = None
    info_toggle = False
    last_info_toggle = False

    toggle_time = time()

    def __init__(self, lcd, button):
        self.lcd = lcd
        self.button = button

    def set_scan_callback(self, function=None):
        if function is not None:
            self.scan_callback = function

    def set_get_wifi_callback(self, function=None):
        if function is not None:
            self.get_wifi_callback = function

    def set_send_info_callback(self, function=None):
        if function is not None:
            self.send_info_callback = function

    def get_screen_data(self, screen_id=None, screen_name=None):
        screen_data = None
        if screen_id is None and screen_name is None:
            return None

        try:
            if screen_id is not None and screen_id >= 0:
                screen_data = self.menu_screens[screen_id]
            else:
                for data in self.menu_screens:
                    if data['name'] == screen_name:
                        screen_data = data
                        break
        except:
            pass

        return screen_data

    def menu_pos_common(self, up):
        while True:
            if self.menu_pos < 0:
                self.menu_pos = len(self.menu_screens) - 1
            if self.menu_pos >= len(self.menu_screens):
                self.menu_pos = 0

            screen_data = self.get_screen_data(screen_id=self.menu_pos)
            if screen_data['enable']:
                self.lock = screen_data['lock']
                break

            if up:
                self.menu_pos += 1
            else:
                self.menu_pos -= 1

        if not self.lock:
            self.lcd.clear()

    def menu_pos_up(self):
        screen_data = self.get_screen_data(screen_id=self.menu_pos)
        if not screen_data['lock']:
            self.menu_pos += 1
            self.lock = False
        else:
            self.lock = True

        self.menu_pos_common(up=True)

    def menu_pos_down(self):
        screen_data = self.get_screen_data(screen_id=self.menu_pos)
        if not screen_data['lock']:
            self.menu_pos -= 1
            self.lock = False
        else:
            self.lock = True

        self.menu_pos_common(up=False)

    def screen_init(self, data_list=None):
        self.lcd.line1("   wifaraday    ")
        self.lcd.line2(": wifi scanner :")
        return True

    def screen_scan_wifi(self, data_list=None):
        self.lcd.clear()
        self.lcd.line1("Press OK to scan")
        if self.button.gpio_value[self.KEY_OK] == 0:
            if self.scan_callback is not None:
                self.lcd.blue()
                self.lcd.line2("Scanning...")
                self.wifi_cells = self.scan_callback()
                self.lcd.status_ok()
                self.wifi_pos = 0
        return True

    def screen_wifi_total(self, data_list=None):
        self.lcd.clear()
        self.lcd.line1(": Wifi APs")
        self.lcd.line2(" Total: %d" % len(self.wifi_cells))

        return True

    def screen_wifi_list(self, data_list=None):
        if self.info_toggle == False:
            if self.button.gpio_value[self.KEY_UP] == 0:
                self.wifi_pos_up()
            elif self.button.gpio_value[self.KEY_DOWN] == 0:
                self.wifi_pos_down()

        if self.button.gpio_value[self.KEY_OK] == 0:
            if time() - self.toggle_time > 1:
                self.info_toggle = not self.info_toggle
                self.toggle_time = time()

        cell_info = self.wifi_cells[self.wifi_pos]
        if self.info_toggle == False:
            lcd_str = ">%s" % (cell_info['Name'][:15])
        else:
            if self.get_wifi_callback is not None and \
                    self.last_info_toggle == True:
                cell_info = deepcopy(self.get_wifi_callback(
                        deepcopy(self.wifi_cells[self.wifi_pos])))
            self.last_menu_pos = -1

            lcd_str = "+%s %s" % \
                (cell_info['Name'][:11], cell_info['Level'])

        self.lcd.clear()
        if self.info_toggle == False:
            self.lcd.white()
            self.lcd.line1(": Choose wifi ")
        else:
            self.lcd.blue()
            self.lcd.line1(": Wifi info ")

        self.lcd.line2(lcd_str)
        if self.last_info_toggle == True and \
                self.info_toggle == False and \
                self.send_info_callback is not None:
            self.send_info_callback()
        self.last_info_toggle = self.info_toggle
        return True

    def poll(self, data_list=None):
        key_value = self.button.gpio_value

        for menu in self.menu_screens:
            if menu['name'] == 'wifi_list' or \
                    menu['name'] == 'wifi_total':
                if self.wifi_cells is None or \
                        len(self.wifi_cells) < 1:
                    menu['enable'] = False
                else:
                    menu['enable'] = True

        for key, value in key_value.iteritems():
            if value == 0:
                if self.info_toggle == True:
                    self.last_menu_pos = -1
                    break

                self.lcd.white()

                if key == self.KEY_RIGHT:
                    self.menu_pos_up()
                elif key == self.KEY_LEFT:
                    self.menu_pos_down()
                elif key in [self.KEY_OK, self.KEY_UP, self.KEY_DOWN]:
                    self.last_menu_pos = -1

        if self.menu_pos == self.last_menu_pos:
            return True

        screen_data = self.get_screen_data(screen_id=self.menu_pos)
        if screen_data is None:
            self.screen_error()
            return False

        screen_name = screen_data['name']
        self.last_menu_pos = self.menu_pos

        if self.force_clean:
            self.force_clean = False
            self.lcd.clear()

        menu_function = eval('self.screen_'+screen_name)
        return menu_function(data_list)

    def screen_error(self):
        self.lcd.clear()
        self.lcd.red()
        self.lcd.line1('  ::wifaraday:: ')
        self.lcd.line1('      ERROR     ')

    def wifi_pos_common(self, up):
        if self.wifi_pos < 0:
            self.wifi_pos = len(self.wifi_cells) - 1
        if self.wifi_pos >= len(self.wifi_cells):
            self.wifi_pos = 0

    def wifi_pos_up(self):
        self.wifi_pos += 1
        self.wifi_pos_common(up=True)

    def wifi_pos_down(self):
        self.wifi_pos -= 1
        self.wifi_pos_common(up=False)

if __name__ == '__main__':
    from grove_lcd_rgb import GROVE_LCD_RGB
    from button import BUTTON
    from time import sleep

    lcd = GROVE_LCD_RGB()
    btn = BUTTON()
    nav_menu = NAVIGATION_MENU(lcd, btn)
    nav_menu.poll()

    try:
        while 1 == 1:
            btn.read()
            sleep(0.180)
            nav_menu.poll()
    except KeyboardInterrupt:
        pass
    #except Exception, e:
    #    print "ERROR:", str(e)
    #nav_menu.screen_shutdown()
