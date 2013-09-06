import os
import socket
import ssl
import time
import re
from random import choice
import serial
host = "freenode.net"
port = 6697
room = "#techlabeducation"
boss = "treeherder!jane@"
joined = 0
handles = []
people = set()
readbuffer = ""
irc_nick_re = "/(?<=[^a-z_\-\[\]\\^{}|`])[a-z_\-\[\]\\^{}|`][a-z0-9_\-\[\]\\^{}|`]*/i"

device_list = ['/dev/ttyACM0', '/dev/ttyACM1', '/dev/ttyACM2', '/dev/ttyACM3', '/dev/tts/ACM0','/dev/tts/ACM1' ,0,1,2,3] 
positives = ["Yessir", "o.k.", "Sure thing, hoss.","i live to serve.", "i'm on it", "Got it.", "right.", "of course.","your will is my command", "I thought you would never ask.", "roger", "can-do!", "as you wish."]  
negatives = ["i simply cannot be fucked to help you, friend.", "No, sorry, I can't do that" , "i'd rather not", "definitely not going to happen.","i will not!", "Negatory.", "sorry, boss.", "Sadly, I should have to decline for now", "i tried as hard as i could, please don't hate me", "i cannot perform that function at this time", "i must regretfully inform you that that may be impossible."]
directives =["~quit", "~reload", "~report", "~takeoverz"]
retort = ["no, you.", "whatever", "hey, stop highlighting me!", "i don't answer to you, peon.", "get real, dude.", "come at me, bro.", "LOL don't be mad"]
greeting = ["we've missed you, ", "welcome, ", "hello, ", "hiya, ", "greetings ", "salutations, ", "YO YO YO YO YO YO ", "sup ", "I knew you'd be back, ", "welcome back, " "hey, howdy ", "waddup ", "hii "]




irc = socket.socket()		#create the socket
s=ssl.wrap_socket(irc)			#wrapping the socket for ssl



class BOT():
	def __init__(self, nickname, realname, identity):		#keeping options open for child classes
		self.nick = nickname
		self.name = realname
		self.ident = identity
		self.password = ""
		
	def answer(self, ans):		# this is a place holder function 
		if ans == 1:
			ans = choice(positives)
			return ans
		if ans == 0:
			ans = choice(negatives)
			return ans
		if ans == 2:
			ans = choice(retort)
			return ans
		if ans == 3:
			ans = choice(greeting)
			return ans
		
	def begin(self,_host,_port):		#trivial, but critical
		try:
			s.connect((_host,_port))
			time.sleep(1)
		except:
                        print("connection error.")
                        raise  #thanks, sarper
		else:
			print("Connected")
			return
		finally:
			time.sleep(1)
			
	def chop(self,z):		#parser apples stole from twisted
		self.prefix = ''
		trailing = []
		if not z:
			raise BaseException
		if z[0] == ':':
			self.prefix, z = z[1:].split(' ', 1)
		if z.find(' :') != -1:
			z, trailing = z.split(' :', 1)
			self.args = z.split()
			self.args.append(trailing)
		else:
			self.args = z.split()
		self.command = self.args.pop(0)
		return self.prefix, self.command, self.args
		
	def join(self,chan):					#method to join a channel
		s.send("JOIN {0}\r\n".format(chan)) 
	
	
	def register(self):		#register with ircd
		s.send("NICK {0}\r\n".format(self.nick))
		time.sleep(0.2)
		s.send("USER {0} {1} shit :{2}\r\n".format(self.name, self.ident, self.ident))
		time.sleep(0.2)
		s.send("PRIVMSG nickserv identify {0}\r\n".format(self.password))
		return
	
		
	def sndmsg(self,chan,msg):			#method for sending IRC messages
		channel = chan.strip("\r\n")
		s.send("PRIVMSG {0} {1}\r\n".format(channel, msg))
		
		
		
	def drive(self):   			#this is where it comes together
		readbuffer = s.recv(1024)
		while '\r\n' in readbuffer:
			idx = readbuffer.find('\r\n') + 2
			words = self.chop(readbuffer[:idx])
			readbuffer = readbuffer[idx:]
			print words
			joined = 0
			if (host in self.prefix):		#just a bunch of conditions for actions after connecting
				joined == 0
			if (self.command == '353'):
				o =  self.args[-1].split(' ')
				if o:
					handles.append(o)			
			if(joined == 0):
				self.join(room)
				joined == 1
				
			if (self.command == 'PING'):					#ping
				s.send('PONG {0}\r\n'.format(self.args[0]))
				print "sent pong:PONG {0}r\n".format(self.args[0])
				print time.clock
				#timer.counter()
				continue
                        elif (self.command == 'KICK') and (self.nick not in self.prefix):
                                joined == 0
                                self.join(self.args[0])
                        elif (self.command =='KILL') and (self.nick in self.args):
                                os.execlp("./engine.py", 'somebot')
                                continue
                        	continue
			elif (self.command == "JOIN"):
				if (self.nick in self.prefix):
					self.sndmsg(room, "hello, cruel world")
				elif self.nick not in self.prefix:
					x = self.prefix.split('!')
					self.sndmsg(self.args[0],"{0}{1}".format(self.answer(3), x[0]))
					handles.append(x[0])
					
			elif (self.command == 'PRIVMSG') and (self.prefix != boss):  # owner commands
 				for key in self.args:		
 					if (self.nick in key):
 					 	self.sndmsg(self.args[0],"{0}".format(self.answer(2)))
 					 	
			elif (self.command == 'PRIVMSG') and (self.prefix == boss):  # owner commands
 				for key in self.args:
					if ('~quit' in key):
						try:
							self.sndmsg(self.args[0], "fairwell, cruel world.")
							self.s.send(self.args[0], "QUIT I am  eternally obedient.\r\n")
							quit(2)
						except:
							self.answer(0)

					elif ('~reload' in key):
						self.sndmsg(self.args[0], "{0}".format(self.answer(1)))
						time.sleep(1)
						s.send("QUIT hasta la vista, baby.\r\n")
						s.close
						time.sleep(1)
						import engine.py
						reload(engine)
					elif('herp' in key):
						self.sndmsg(self.args[0], "derps\r\n")
					elif('derp' in key):
						self.sndmsg(self.args[0], "herps\r\n")
					elif('~enter' in key):
						self.join(self.args[1]) 
					elif('~raw' in key):
						s.send("NAMES {0}\r\n".format(self.args[0]))
						time.sleep(5)
						self.sndmsg(self.args[0], "{0}".format(self.args[-1:]))
			
					elif ('~rollcall' in key):  #check to see if in the list first?  good advice.
						s.send("NAMES {0}\r\n".format(self.args[0]))
						for handle in [handles]:
							people.add([handle])
							
							self.sndmsg(self.args[0],"{0}".format(handle))
								
								
bot = BOT('abramowitz','nancy','nursebot')
bot.begin(host,port)
bot.register()
bot.join(room)
while True:
	bot.drive()
