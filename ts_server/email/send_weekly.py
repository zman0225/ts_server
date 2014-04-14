#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: ziyuanliu
# @Date:   2014-03-27 18:23:27
# @Last Modified by:   ziyuanliu
# @Last Modified time: 2014-04-04 00:26:25
# a script

from ts_server.models.account import *
from ts_server.models.recipe import *

from ts_server.lib.redisrelations import get_recipe_name_by_id
from ts_server.adapter.administration import connect_to_db

import requests
import logging
import random
# def send(self, kw):
# 		for u in kw.keys():
# 			data = loads(kw[u])
# 			temp = self.template(data['recipes'],data['username'])
# 			sent = self.send_simple_message(data['email'],data['username'],temp)
# 			logging.info("email send to %s"%data['email'])

def template(recipes,username):
	s = str(recipes)[1:-1].replace("'","")
	return """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
	<html><body><h2>Dear %s,</h2><h4>Your current menu looks delicious.</h4> <p>This week, you had: <b>%s</b>.\
	<br>Preparing for the upcoming week? visit: <a href="http://www.timesavorapp.com">TimeSavor</a>\
	<br>If you have any questions or concern, please don't hesitate to email us back.\
	</p><h4>Cheers,</h4> <h3>TimeSavor</h3></body></html>"""%(username,s)


def send_simple_message(email, msg, subject = None, tag = None):
	return requests.post(
		"https://api.mailgun.net/v2/mg.timesavorapp.com/messages",
		auth=("api", "key-9y7c3fgcidcnqzopu-psjg0nq3wbg7h3"),
		data={"from": "TimeSavor <chefsal@mg.timesavorapp.com>",
			"to": [email],
			"subject": subject,
			"html": msg,
			"o:campaign":tag,
			"o:deliverytime": "Fri, 4 Apr 2014 08:00:00 -0500",
			"o:tracking": True})


 

def send_request(email, msg, subject = None, tag = None):
	return requests.post(
		"https://api.mailgun.net/v2/mg.timesavorapp.com/messages",
		auth=("api", "key-9y7c3fgcidcnqzopu-psjg0nq3wbg7h3"),
		data={"from": "Salman from TimeSavor <chefsal@mg.timesavorapp.com>",
			"to": [email],
			"subject": subject,
			"text": msg,
			"o:campaign":tag,
			"o:tracking": True})

if __name__ == '__main__':
	connect_to_db("ts-server",'23.253.209.158',27017,'ts_server','a2e7rqej')
	subscribed = 0
	print "connected"
	for acc in Account.objects:
		if acc.subscribed:

			email = acc.email
			username = acc.username
			rand = random.randint(0,2)
			tests = ['c8lv7','c8lv8','c8lv9']

# 			subjects = ['Would you help a student entrepreneur?','Our site didn\'t make planning effortless? Help us do better','Still wish you were better prepared?']
# 			msg = """Hi!  I'm Salman,\n graduating senior at Dartmouth College and founder of Time Savor.\n

# Our website is our first stab at making dinner planning effortless.  We know there's a lot to improve.  \n

# Would you mind briefly chatting with me so we can make something that will actually make your life easier?  \n

# Feel free to leave your phone number if you want me to call you whenever, or we can try to schedule a time.  \n

# Salman\n

# P.S. Honestly, the whole reason I'm doing this is to help people eat better.  My top priority is to  build something that can help the world."""
# 			send_request(email,msg,subjects[rand],tests[rand])
# 			print "sent to %s"%username
			subjects = ["%s: Here's what you're cooking next week!"%username,"%s: Cooking next week will be SO easy"%username,"%s: Guess what? You're ready for dinner next week!"%username]
			campaign = ["first","second","third"]

			plan = acc.current_plan
			plan = plan.menu_plan if plan is not None else None

			try:
				if plan is not None:
					recipe_list = [get_recipe_name_by_id(re) for re in plan]
					temp = template(recipe_list,username)
					send_simple_message(email,temp,subjects[rand],tests[rand])
					print "sent to %s"%username
			except Exception as e:
				print e
