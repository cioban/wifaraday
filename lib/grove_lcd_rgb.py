#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
"""
Modulo: 
"""
__author__ = 'Sergio Cioban Filho'
__version__ = '1.0'
__date__ = '19/06/2015 03:12:07 PM'

import pyupm_i2clcd

class GROVE_LCD_RGB:
    lcd = None

    def __init__(self):
        self.lcd = pyupm_i2clcd.Jhd1313m1(0, 0x3E, 0x62)
        self.lcd.clear()
        self.lcd.setColor(255, 255, 255)
        self.lcd.setCursor(0,0)

    def red(self):
        self.lcd.setColor(255, 0, 0)

    def green(self):
        self.lcd.setColor(0, 255, 0)

    def blue(self):
        self.lcd.setColor(0, 0, 255)

    def white(self):
        self.lcd.setColor(255, 255, 255)

    def line1(self, msg=None):
        if msg == None:
            return
        self.lcd.setCursor(0,0)
        self.lcd.write(msg)

    def line2(self, msg=None):
        if msg == None:
            return
        self.lcd.setCursor(1,0)
        self.lcd.write(msg)

    def status_ok(self):
        self.green()
        self.lcd.setCursor(1,14)
        self.lcd.write('OK')

    def status_nok(self):
        self.red()
        self.lcd.setCursor(1,13)
        self.lcd.write('NOK')

    def clear(self):
        self.lcd.clear()
        #self.lcd.setColor(255, 255, 255)
        self.lcd.setCursor(0,0)


if __name__ == '__main__':
    from time import sleep
    lcd = GROVE_LCD_RGB()
    lcd.red()
    lcd.line1('Test 1')
    lcd.line2('Test 2')

    while 1 == 1:
        lcd.blue()
        sleep(0.5)
        lcd.red()
        sleep(0.5)
        lcd.green()
        sleep(0.5)
        lcd.white()
        sleep(0.5)


