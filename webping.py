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

@click.command()
@click.option('--count', default=1, help='Numero de pruebas a realizar')
@click.option('--url', default='https://www.google.com',
              help='URL del sitio a webpingear')
@click.option('--output', default='results.txt', help='Nombre del archivo con los resultados de la medida')

def webping(count, url, output):
	click.echo('WebPinging %s %s times' % (url, count))
	measurements = []
	for x in range(count):
		t0 = time.time()
		subprocess.call(cmd_chrome % (url), shell=True, stdout=FNULL, stderr=FNULL)
		t1 = time.time()
		print "%s | %s " % (t0, t1-t0)
        
# end webping

if __name__ == '__main__':
    webping()