#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: ziyuanliu
# @Date:   2014-03-27 18:23:27
# @Last Modified by:   ziyuanliu
# @Last Modified time: 2014-03-28 08:07:11
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
			"o:tag":tag,
			"o:campaign":"c7umr",
			"o:tracking": True})

if __name__ == '__main__':
	connect_to_db("ts-server",'23.253.209.158',27017,'ts_server','a2e7rqej')
	subscribed = 0

	for acc in Account.objects:
		if acc.subscribed:

			email = acc.email
			username = acc.username
			rand = random.randint(0,2)
			subjects = ["%s: Here's what you're cooking next week!"%username,"%s: Cooking next week will be SO easy"%username,"%s: Guess what? You're ready for dinner next week!"%username]
			campaign = ["first","second","third"]

			plan = acc.current_plan
			plan = plan.menu_plan if plan is not None else None

			try:
				if plan is not None:
					recipe_list = [get_recipe_name_by_id(re) for re in plan]
					temp = template(recipe_list,acc.username)
					
					send_simple_message(email,temp,subjects[rand],campaign[rand])
					print "sent to %s"%username
			except Exception as e:
				print e
