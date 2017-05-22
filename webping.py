#!/usr/bin/env python
# webping.py
# (c) carlos@lacnic.net 20170522
#

import click
import os
import sys
import subprocess
import time
import getpass
import pycurl

### CONFIGURABLE VARIABLES
cmd_chrome = "/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome " 
cmd_chrome += "--headless --disable-gpu --screenshot %s"
cmd_airport = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I"
cmd_curl_influx = "curl -i -XPOST \"http://189.76.124.2:8086/write?db=evento&u=agente&p=evento201705\" --data-binary @influx.txt"
### 

FNULL = open(os.devnull, 'w')
influx_file = open("influx.txt", "w")

def mean(numbers):
	"""Calcular el promedio de un array de numeros"""
	return float(sum(numbers)) / max(len(numbers), 1)

def get_measurement_source():
	src = {}
	uname = os.uname()
	src['hname'] = uname[1]
	#
	username = getpass.getuser()
	src['username'] = username
	#
	wifi_data = get_wifi_info()
	src['bssid'] = wifi_data[1]
	src['ssid'] = wifi_data[0]
	return src
## end get_measurement_source

def get_wifi_info():
	ssid = 'noname_ssid'
	bssid = 'noname_bssid'
	wifi_raw_data = subprocess.check_output(cmd_airport, shell=True)
	rd1 = wifi_raw_data.split("\n")
	print len(rd1)
	for ff in rd1:
		rd2 = ff.split(":")
		#print rd2,len(rd2)
		#print ff
		if len(rd2)>=2:
			f1 = rd2[0].strip()
			f2 = rd2[1].strip()
			#print rd2
			if f1.endswith("SSID"):
				ssid = f2
			if f1.endswith("BSSID"):
				bssid = ":".join(rd2[1:6])
				bssid = bssid.strip()
	# end for
	return [ssid,bssid]
	
## end get wifi info

@click.command()
@click.option('--count', default=1, help='Numero de pruebas a realizar')
@click.option('--url', default='https://www.google.com',
              help='URL del sitio a webpingear')
@click.option('--output', default='results.txt', help='Nombre del archivo con los resultados de la medida')

def webping(count, url, output):
	click.echo('WebPinging %s %s times' % (url, count))
	measurements = {'url': url, 't0': [], 'dt': []}
	for x in range(count):
		t0 = time.time()
		subprocess.call(cmd_chrome % (url), shell=True, stdout=FNULL, stderr=FNULL)
		t1 = time.time()
		measurements['t0'].append(t0)
		measurements['dt'].append(t1-t0)
		print "%s | %s " % (t0, t1-t0)
	# end for
	# print summary
	src = get_measurement_source()
	avgtime = mean(measurements['dt'])
	avgts = int(mean(measurements['t0']))
	print "Pinged %s times from source %s, avg dt is %s" % (count, src, avgtime)
	# print influx line
	influx_file.write("webping,url=%s,uname=%s,ssid=%s,bssid=%s loadtime=%s %s000000000\n" % (url, src['username'], src['ssid'], src['bssid'], avgtime, avgts ))
	subprocess.call(cmd_curl_influx, shell=True)	
# end webping
        
# end webping
if __name__ == '__main__':
    webping()