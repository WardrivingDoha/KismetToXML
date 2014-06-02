#!/usr/bin/env python

import sys

try:
    from elementtree import ElementTree
except:
    from xml.etree import ElementTree


try:
    file = sys.argv[1]
    data = open(file,'r').read()
except:
   print sys.argv[0] + " {kismet logfile}"
   sys.exit(1)


detection = ElementTree.fromstring(data)

# KML Header
print """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://earth.google.com/kml/2.0">
<Document>
   <name>Kismet Log </name>
      <Folder>
         <name> Kismet Log Points </name>""" 

for node in detection.getchildren():
   try:
       essid = node.find('essid').text
   except AttributeError:
       #hidden SSID
       essid = "{unknown SSID}"

   try:
       channel = node.find('channel').text
   except AttributeError:
       #hidden SSID
       channel = "{unknown channel}"

   try:
       maxrate = node.find('max-rate').text
   except AttributeError:
       maxrate = "{unknown maxrate}"

   try:
       #need to loop through them
       encryption = node.find('encryption').text
   except:
       encryption = "{unknown encryption}"
   
   try:
       lon = node.find('lon').text
   except:
       lon = "{unknown lon}"

   try:
       lat = node.find('lat').text
   except:
       lat = "{unknown lat}"

   try:
       bssid = node.find('BSSID').text
       if lon != '{unknown lon}' and lon != '0.000000':
          print """
           <Placemark>
           <description><![CDATA[
           <p style="font-size:8pt;font-family:monospace;">(%s , %s)</p>
           <ul>
           <li> BSSID : %s </li>
           <li> Channel : %s </li>
           <li> Max Rate : %s </li>
           <li> Encrypt : %s </li>
           </ul>
           ]]>
           </description>
           <name>%s</name>
           <Point>
           <extrude>1</extrude>
           <altitudeMode>relativeToGround</altitudeMode>
           <coordinates>%s,%s,0</coordinates>
           </Point>
           </Placemark> """ % \
                     (lon,lat,essid,lon,lat)
   except AttributeError:
       #hidden SSID
       bssid = "{unknown BSSID}"


# KML Footer
print """  %s</Folder>
 </Document>
    </kml>"""
