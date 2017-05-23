# webping
Web page ping based on Chrome headless mode and some python

## Installing

Run:

```
pip install git+https://github.com/carlosm3011/webping
```

## Monitor

Run inside a terminal and a while loop such as this:

```
while true
do
	webping.py --count=3 --url="https://eventos.lacnic.net"
	echo sleeping...
	sleep 60
done

```