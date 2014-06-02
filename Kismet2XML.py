#!/usr/bin/env python

import sys
import os
try:
    from elementtree import ElementTree
except:
    from xml.etree import ElementTree


#Combine Func.
def combine_xml(files):
    first = None
    for filename in files:
        data = ElementTree.parse(os.path.join(sys.argv[1],filename)).getroot()
        if first is None:
            first = data
        else:
            first.extend(data)
    if first is not None:
        return ElementTree.tostring(first)


try:
   files = [f for f in os.listdir(sys.argv[1]) if os.path.isfile(os.path.join(sys.argv[1],f)) and f.endswith('.netxml')]
   data = combine_xml(files)
except:
   print sys.argv[0] + " {kismet logfile}"
   sys.exit(1)


detection = ElementTree.fromstring(data)

# KML Header
print """<?xml version="1.0" encoding="UTF-8"?>
    <detection-run>"""

myList = [];
for node in detection.getchildren():
   try:
       ssid = node.find('SSID')
       essid = ssid.find('essid').text
       essid = essid.replace('&','')
   except AttributeError:
       #hidden SSID
       essid = "{unknown SSID}"

   try:
       channel = node.find('channel').text
   except AttributeError:
       #hidden SSID
       channel = "{unknown channel}"

   try:
       maxrate = ssid.find('max-rate').text
   except AttributeError:
       maxrate = "{unknown maxrate}"

   try:
       #need to loop through them
       encryption = ssid.find('encryption').text
   except:
       encryption = "{unknown encryption}"

   try:
       gps = node.find('gps-info')
   except:
       gps = "{unknown gps}"
                
   try:
       lon = gps.find('max-lon').text
   except:
       lon = "{unknown lon}"

   try:
       lat = gps.find('max-lat').text
   except:
       lat = "{unknown lat}"

   try:
       bssid = node.find('BSSID').text
       if lon != '{unknown lon}' and lon != '0.000000':
           myList.append("""
           <wireless-network>
           <lon>%s</lon>
           <lat>%s</lat>
           <BSSID>%s</BSSID>
           <channel>%s</channel>
           <max-rate>%s</max-rate>
           <encryption>%s</encryption>
           <essid>%s</essid>
           </wireless-network>
            """ % \
                     (lon,lat,bssid,channel,maxrate,encryption,essid));
   except AttributeError:
       #hidden SSID
       bssid = "{unknown BSSID}"


myList = list(set(myList))
for i in myList:
    print i


print """</detection-run>"""
