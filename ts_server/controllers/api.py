#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: ziyuanliu
# @Date:   2014-02-20 12:25:25
# @Last Modified by:   ziyuanliu
# @Last Modified time: 2014-02-20 15:58:24

from basehandler import BaseHandler
import tornado.ioloop
import logging
import json
from adapter import *

#format of a request - {'command',{PACKET}}, authentication through cookie session storage
#format of a return - {'return':[T/F], error:[MESSAGE], return_code:[0...n], message:[]}
#code: 0 - registration/login successful
#code: 1 - preference set 
class UserHandler(BaseHandler):
	def initialize(self):
		super(UserHandler,self).initialize()
		self.cases = {'login':self.login,
						'register':self.register,
						'set_preferences':self.set_preferences,
					}

	def post(self):
		self.load_request()
		if self.req is None:
			return
		try:
			print "result ",self.req_val, isinstance(self.req_val,dict)
			self.cases[self.req](**self.req_val)
			return
		except ValueError:
			logging.debug("BAD REQUEST %s"%self.request.body)
		
		self.finish()

	def register(self,username,password):
		ip_addr = self.request.remote_ip
		account = new_account(username,password,ip_addr)
		if account is not False:
			# session_key = generate_session_key(account.pk)
			self._SESSION_KEY = str(account.pk)
			self.load_session(account)
			self.set_secure_cookie('SID',str(account.pk))
			self.write(self.json_packet(retval=True, return_code = 0, packet = {}))
		else:
			logging.debug("ACCOUNT exists")
			self.write(self.json_packet(retval=False, error = "Account already exists"))
		self.finish()

	def login(self,username,password):
		account = login(username,password)
		print account, username, password, 'fucking work'
		if account is False:
			self.write(self.json_packet(retval=False, error = "Login information is incorrect"))
		else:
			self.set_secure_cookie('SID',str(account.pk))
			self._SESSION_KEY = str(account.pk)
			
			self.load_session(account)
			self.write(self.json_packet(retval=True, return_code = 0, packet = {}))
		self.finish()

	def set_preferences(self,values):
		logging.info("setting food preference %s"%str(values))
		if not isinstance(values,list):
			try:
				values = json.loads(values)
			except ValueError:
				logging.debug("Not JSON %s"%values)
				return {'status':'failed'}
		if isinstance(values,list):
			set_preferences(self.session['AID'],values)
			self.write(self.json_packet(retval=True, return_code = 1, packet = {}))
		else:
			logging.debug("Invalid interest format %s"%values)
			string = "Invalid interest format %s"%values
			self.write(self.json_packet(retval=False, error = string))
		self.finish()
