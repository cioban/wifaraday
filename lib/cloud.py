#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
"""
Modulo: 
"""
__author__ = 'Sergio Cioban Filho'
__version__ = '1.0'
__date__ = '20/06/2015 01:45:09 AM'

import json
import urllib2
from copy import deepcopy

class CLOUD:
    api_url = 'http://mfaraday.azurewebsites.net/api/NetWiFiAnalyser'

    def do_send_info(self, data):
        response = ''
        req = urllib2.Request(self.api_url)
        req.add_header('Content-Type', 'application/json')

        response = urllib2.urlopen(req, data)
        #response.getcode()

    def prepare_json(self, info):
        info_base = info.values()[0]
        json_fields = {
            'MAC': info_base['Address'],
            'SSID': info_base['Name'],
            'SecurityInfo': "Not collected",
            'NetWiFiDataRequestList': [],
            }
        wifi_data = {}
        for timestamp, data in info.iteritems():
            wifi_data['EventDate'] = timestamp
            wifi_data['EventValue'] = int(data['Level'])
            json_fields['NetWiFiDataRequestList'].append(deepcopy(wifi_data))

        return json_fields

    def send_info(self, info):
        json_fields = self.prepare_json(info)

        json_data = json.dumps(json_fields)

        from pprint import pprint
        pprint(json_data)

        try:
            self.do_send_info(json_data)
            #pass
        except Exception, e:
            print 'ERR: %s' % e

if __name__ == '__main__':
    data = {
        12345: {'Address': 'A0:CF:5B:FA:66:FF', 'Level': '-60', 'Name': 'TESLA'},
        12346: {'Address': 'A0:CF:5B:FA:66:FF', 'Level': '-65', 'Name': 'TESLA'},
        12347: {'Address': 'A0:CF:5B:FA:66:FF', 'Level': '-70', 'Name': 'TESLA'},
    }

    cloud = CLOUD()
    cloud.send_info(data)

