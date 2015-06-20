#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
"""
Modulo: 
"""
__author__ = 'Sergio Cioban Filho'
__version__ = '1.0'
__date__ = '19/07/2014 22:43:02'
#__all__ = ('wifi_is_connected','wifi_connect',
#	'wifi_disconnect', 'get_interface_ip', 'add_ap_addr')

import sys
from subprocess import Popen, PIPE
from time import sleep, time
import fcntl
import struct
import socket
from Queue import Queue

###################
# iwlist scan parser from (with some adaptations):
# iwlistparse.py
# Hugo Chargois - 17 jan. 2010 - v.0.1
# Parses the output of iwlist scan into a table
# https://bbs.archlinux.org/viewtopic.php?id=88967
###################

#ssid_queue = Queue(maxsize=0)

def get_name(cell):
    return matching_line(cell,"ESSID:")[1:-1]

def get_level(cell):
    level = matching_line(cell,"Quality=").split()[2].split('=')[1].split('/')
    return level[0]
    #test = str(int(round(float(level[0]) / float(level[1]) * 100))).rjust(3) + " %"
    #return str(test)

def get_address(cell):
    return matching_line(cell,"Address: ")

def sort_cells(cells):
    sortby = "Level"
    reverse = False
    cells.sort(None, lambda el:el[sortby], reverse)

def matching_line(lines, keyword):
    """Returns the first matching line in a list of lines. See match()"""
    for line in lines:
        matching=match(line,keyword)
        if matching!=None:
            return matching
    return None

def match(line,keyword):
    """If the first part of line (modulo blanks) matches keyword,
    returns the end of that line. Otherwise returns None"""
    line=line.lstrip()
    length=len(keyword)
    if line[:length] == keyword:
        return line[length:]
    else:
        return None

rules={"Name":get_name,
       "Level": get_level,
       "Address":get_address,
       }

def parse_cell(cell):
    """Applies the rules to the bunch of text describing a cell and returns the
    corresponding dictionary"""
    parsed_cell={}
    for key in rules:
        rule=rules[key]
        parsed_cell.update({key:rule(cell)})
    return parsed_cell

def get_wifi_list():
    iwlist_out = ''
    try:
        pid = Popen(['/sbin/iwlist', 'wlan0', 'scan'], stdout=PIPE,
                    close_fds=True)
        iwlist_out = pid.communicate()[0].split('\n')
    except Exception:
        pass

    return iwlist_out

def get_wifi_info(cell_info=None):
    if cell_info is None:
        return None

    iwlist_out = ''
    try:
        essid = cell_info['Name']
        pid = Popen(['/sbin/iwlist', 'wlan0', 'scanning', 'essid', "%s" % essid ], stdout=PIPE,
                    close_fds=True)
        iwlist_out = pid.communicate()[0].split('\n')
        sleep(0.5)
    except Exception:
        pass

    return iwlist_out

def do_wifi_info(cell_info=None,debug=False):
    ret = {}
    ret['Address'] = cell_info['Address']
    ret['Level'] = 100
    ret['Name'] = cell_info['Name']

    info_cells=[[]]
    info_parsed_cells=[]
    for line in get_wifi_info(cell_info):
        info_cell_line = match(line,"Cell ")
        if info_cell_line != None:
            info_cells.append([])
            line = info_cell_line[-27:]
        info_cells[-1].append(line.rstrip())

    info_cells=info_cells[1:]

    for info_cell in info_cells:
        info_cell_dict = parse_cell(info_cell)
        #if debug:
        #    from pprint import pprint
        #    pprint(cell_dict)
        info_parsed_cells.append(info_cell_dict)
    #sort_cells(info_parsed_cells)
    if debug:
        from pprint import pprint
        pprint(info_parsed_cells)

    try:
        from pprint import pprint

        for parsed_cell in info_parsed_cells:
            if parsed_cell['Name'] == cell_info['Name']:
                ret = parsed_cell
                break
    except:
        pass

    return ret

def do_wifi_scan(debug=False):
    cells=[[]]
    parsed_cells=[]
    for line in get_wifi_list():
        cell_line = match(line,"Cell ")
        if cell_line != None:
            cells.append([])
            line = cell_line[-27:]
        cells[-1].append(line.rstrip())

    cells=cells[1:]

    for cell in cells:
        cell_dict = parse_cell(cell)
        #if debug:
        #    from pprint import pprint
        #    pprint(cell_dict)
        parsed_cells.append(cell_dict)
    sort_cells(parsed_cells)
    if debug:
        from pprint import pprint
        pprint(parsed_cells)

    return parsed_cells
    #for ap in parsed_cells:
    #    #{'Level': '100 %', 'Name': 'KEY_CLIENT_01', 'Address': 'F8:1A:67:E6:77:8}
    #    if 'Name' in ap.keys():
    #        if debug:
    #            print "Add %s in queue" % ap['Name']
    #        ssid_queue.put(ap['Name'])

#def get_ssid():
#    ret = None
#    if ssid_queue.empty() == True:
#        do_wifi_scan()
#
#    if ssid_queue.empty() == False:
#        ssid = ssid_queue.get()
#        ssid_queue.task_done()
#        ret = ssid
#    return ret


def get_interface_ip(ifname):
    ip = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ip = socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915,
                    struct.pack('256s', ifname[:15]))[20:24])
        s.close()
    except:
        pass
    return ip

######################################################################



if __name__ == '__main__':
    #cells = do_wifi_scan(debug=False)
    info = do_wifi_info(cell_info={'Address': '6C:B5:6B:14:14:68', 'Level': '-44', 'Name': 'HD0001'},debug=False)
    cell=[' Address: A0:CF:5B:FA:66:FF',
            '                    Channel:149',
            '                    Frequency:5.745 GHz',
            '                    Quality=39/70  Signal level=-71 dBm']
    from pprint import pprint
    pprint(info)

