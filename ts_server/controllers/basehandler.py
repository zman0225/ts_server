#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: ziyuanliu
# @Date:   2014-02-20 12:17:33
# @Last Modified by:   ziyuanliu
# @Last Modified time: 2014-03-02 01:01:02

from ts_server.lib.redissession import Session
from ts_server.lib.authentication import *
from ts_server.adapter import *

import json
import tornado.web

#format of a request - {'command',{PACKET}}, authentication through cookie session storage
#format of a return - {'return':[T/F], error:[MESSAGE], return_code:[0...n], packet:[]}
class BaseHandler(tornado.web.RequestHandler):
	def initialize(self):
		self._SESSION_KEY=None
		self.ERROR = {}
		self.return_packet = {}
		self.req = None
		self.req_val = None

	def get_current_user(self):
		return self.get_secure_cookie('SID')

	def validate(self):
		sessionid = self.get_secure_cookie('SID')
		if sessionid is not None:
			logging.info("VALID")
			logging.info('session is %s'%sessionid)
			self._SESSION_KEY = sessionid
			return True
		else:
			self.clear_all_cookies()
			logging.info("NOT VALID")
			return False

	def load_session(self,account):
		self.session['username'] = account.username
		self.session['AID'] = str(account.pk)
		logging.info("loading session "+str(self.session['username'])+" "+str(self.session['AID']))

	def load_request(self):
		try:
			kw = json.loads(self.request.body)
			self.req,self.req_val = kw.popitem()
		except ValueError:
			self.write(self.json_packet(False, error="bad json request received %s"%self.request.body))
			self.finish()

	def json_packet(self, retval, error = None, return_code = None, packet = None):
		kw = {'return':retval}
		if not retval and error is not None:
			kw['error'] = error
		elif retval and error is None:
			kw.update({'return_code':return_code, 'packet':packet})
		else:
			raise Exception, "bad parameters for json_packet"

		return kw
		
	def return_authentication_status(self,boolean):
		kw={}
		kw['status']='succeeded' if boolean else 'failed'
		logging.info("authentication %s"%kw['status'])
		return kw

	def return_invalid(self,message):
		kw={}
		kw['ERROR']=message
		return json.dumps(kw)

	@property
	def session(self):
		sessionid = self._SESSION_KEY
		return Session(self.application.session_store,sessionid)

