#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
"""
Modulo: 
"""
__author__ = 'Sergio Cioban Filho'
__version__ = '1.0'
__date__ = '19/06/2015 03:46:03 PM'

import mraa
from time import time

class _data:
    last_interrupt = time()
    DEBOUNCE_TIME = 0.2 # seconds

def pin_callback(args):
    if (time() - _data.last_interrupt) < _data.DEBOUNCE_TIME:
        return
    button.read()
    _data.last_interrupt = time()

class BUTTON:
    gpio = {
            8: None,
            9: None,
            10: None,
            11: None,
            12: None
            }
    gpio_value = {}
    ext_read_callback = None

    def __new__(self, *args, **kwargs):
        if not hasattr(self, '_instance'):
            self._instance = super(hardware_controller, self).__new__(self,
                    *args, **kwargs)
        return self._instance

    def __init__(self):
        self.setup_pins()

    def set_read_callback(self, function=None):
        print 'Test'
        if function is not None:
            self.ext_read_callback = function

    def setup_pins(self):
        for pin_num, gpio_obj in self.gpio.iteritems():
            gpio_obj_tmp = mraa.Gpio(pin_num)
            gpio_obj_tmp.dir(mraa.DIR_IN)
            gpio_obj_tmp.mode(mraa.MODE_PULLUP)
            gpio_obj_tmp.isr(mraa.EDGE_FALLING, pin_callback, None)
            self.gpio[pin_num] = gpio_obj_tmp

    def read(self):
        for pin_num, gpio_obj in self.gpio.iteritems():
            self.gpio_value[pin_num] = gpio_obj.read()

        if self.ext_read_callback is not None:
            self.ext_read_callback()

if __name__ == '__main__':
    def test():
        print('Apertou')

    from pprint import pprint
    from time import sleep
    button = BUTTON()
    button.set_read_callback(test)

    sleep(20)
