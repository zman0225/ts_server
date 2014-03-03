#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: ziyuanliu
# @Date:   2014-02-20 12:25:25
# @Last Modified by:   ziyuanliu
# @Last Modified time: 2014-03-03 10:40:58

from basehandler import BaseHandler
import tornado.ioloop
from tornado import web
import logging
import json
from ts_server.adapter import *

#mixpanel analytics
from ts_server.lib.analytics import mp

#format of a request - {'command',{PACKET}}, authentication through cookie session storage
#format of a return - {'return':[T/F], error:[MESSAGE], return_code:[0...n], message:[]}
#code: 0 - registration/login successful
#code: 1 - preference set 
class ApiHandler(BaseHandler):
	def initialize(self):
		super(ApiHandler,self).initialize()
		self.cases = {'login':self.login,
						'register':self.register,
						'set_preferences':self.set_preferences,
						'get_preferences':self.get_preferences,
						'validate_cookie':self.validate_cookie,
						'get_categories':self.get_categories,
						'get_recipes':self.get_recipes,
						'get_latest_plan':self.get_latest_plan,
						'generate_menu':self.generate_menu,
						'set_subscribed':self.set_subscribed
					}

	def post(self):
		self.load_request()
		if self.req is None:
			return
		try:
			self.cases[self.req](**self.req_val)
			return
		except ValueError:
			logging.debug("BAD REQUEST %s"%self.request.body)
		
		# self.finish()

	def validate_cookie(self,*args, **kwargs):
		if self.validate() and self.session.__contains__('username'):
			self.write(self.json_packet(retval=True, return_code = 0, packet = {'display_name':self.session['username']}))
		else:
			self.write(self.json_packet(retval=False, error = "terrible cookie"))
		# self.finish()

	def register(self,username, password, gender, user_age, email):
		ip_addr = self.request.remote_ip
		account = new_ts_account(username, password, ip_addr, gender, user_age, email)
		if account is not False:
			# session_key = generate_session_key(account.pk)
			self._SESSION_KEY = str(account.pk)
			self.load_session(account)
			self.set_secure_cookie('SID',str(account.pk))
			self.write(self.json_packet(retval=True, return_code = 0, packet = {'display_name':self.session['username']}))
			# mp.track(self._SESSION_KEY, 'user registered')
		else:
			logging.debug("ACCOUNT exists")
			self.write(self.json_packet(retval=False, error = "Account already exists"))
		# self.finish()

	def login(self,username,password):
		
		account = login(username,password)
		if account is False:
			self.write(self.json_packet(retval=False, error = "Login information is incorrect"))
		else:
			self.set_secure_cookie('SID',str(account.pk))
			self._SESSION_KEY = str(account.pk)
			
			self.load_session(account)
			self.write(self.json_packet(retval=True, return_code = 0, packet = {'display_name':self.session['username']}))
			mp.track(self._SESSION_KEY, 'user login')
		# self.finish()

	def set_preferences(self,preference,meals):
		if not self.validate():
			return self.validate_cookie()

		logging.info("setting food preference %s %s"%(str(preference),str(meals)))

		if isinstance(preference,list):
			set_preferences(self.session['AID'],preference,meals)
			self.write(self.json_packet(retval=True, return_code = 1, packet = {}))
			# mp.track(self._SESSION_KEY, 'user set preference')
		else:
			logging.info("Invalid interest format %s"%preference)
			self.write(self.json_packet(retval=False, error = "Invalid interest format %s"%preference))
		# self.finish()

	def get_preferences(self,values):
		if not self.validate():
			return self.validate_cookie()
		(prefs,meals,isSubscribed) = get_preferences(self.session['AID'])
		self.write(self.json_packet(retval=True, return_code = 1, packet = {'preference':prefs,'meals':meals,"subscribed":isSubscribed}))
		# self.finish()

	def get_categories(self,values):
		self.write(self.json_packet(retval=True, return_code = 0, packet = {'categories':get_all_categories()}))
		# self.finish()
		
	def get_recipes(self,rid):
		recipes = []
		for r in rid:
			recipes.append(get_recipe_by_id(r))
		self.write(self.json_packet(retval=True, return_code = 0, packet = {'recipes':recipes}))
		# self.finish()

	@web.asynchronous
	def generate_menu(self,values):
		if not self.validate():
			return self.validate_cookie()
		plan = create_plan(self.session['AID'])

		self.write(self.json_packet(retval=True, return_code = 0, packet = {'plan':plan.menu_plan}))
		self.finish()

	@web.asynchronous
	def get_latest_plan(self,values):
		if not self.validate():
			return self.validate_cookie()

		plan = get_latest_plan(self.session['AID'])
		self.write(self.json_packet(retval=True, return_code = 0, packet = {'plan':plan.menu_plan}))
		self.finish()

	def set_subscribed(self,values):
		if not self.validate():
			return self.validate_cookie()

		value = True if values=='true' else False
		set_subscribed(self.session['AID'],value)
		# self.finish()








