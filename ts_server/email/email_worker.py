
import logging
import random
import redis
import threading
from cPickle import loads, dumps
import time
import os
import requests

class EmailWorker(threading.Thread):
	def __init__(self, threadID, event):
		super(EmailWorker, self).__init__()
		self.threadID=os.getpid()+threadID
		self.stopped = event
		self.r = redis.Redis()
		self.setDaemon(True)
		self.channel_name = 'email_worker:'+str(self.threadID)

	def run(self):
		logging.info("EmailWorker [ID]:%s"%str(self.threadID))
		while not self.stopped.wait(10):
			kw = self.r.hgetall("email")
			self.r.delete("email")
			logging.info("Sending emails to %d recipients"%len(kw))
			# self.send(kw)

	def send(self, kw):
		for u in kw.keys():
			data = loads(kw[u])
			temp = self.template(data['recipes'],data['username'])
			sent = self.send_simple_message(data['email'],data['username'],temp)
			logging.info("email send to %s"%data['email'])

	def template(self,recipes,username):
		s = str(recipes)[1:-1].replace("'","")
		return """Dear %s,\n\tYour menu looks delicious. This week, you are having: \n\n%s.\n\
		Want a different menu? visit: http://timesavorapp.com/\n\
		If you have any questions or concern, please don't hesitate to mail us back.\n\
		Cheers,\nChef Sal"""%(username,s)

	
	def send_simple_message(self,email,name,msg):
		return requests.post(
			"https://api.mailgun.net/v2/mg.timesavorapp.com/messages",
			auth=("api", "key-9y7c3fgcidcnqzopu-psjg0nq3wbg7h3"),
			data={"from": "Chef Sal <chefsal@mg.timesavorapp.com>",
				"to": [email],
				"subject": "Hello, %s - your updated meals this week"%name,
				"text": msg})

