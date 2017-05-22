#!/usr/bin/env python
# webping.py
# (c) carlos@lacnic.net 20170522
#

import click
import os
import sys
import subprocess
import time

cmd_chrome = "/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome " 
cmd_chrome += "--headless --disable-gpu --screenshot %s"
FNULL = open(os.devnull, 'w')

def mean(numbers):
	"""Calcular el promedio de un array de numeros"""
	return float(sum(numbers)) / max(len(numbers), 1)

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
	print "Pinged %s times, avg dt is %s" % (count, mean(measurements['dt']))

        
# end webping

if __name__ == '__main__':
    webping()