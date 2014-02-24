#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: ziyuanliu
# @Date:   2014-02-20 11:50:08
# @Last Modified by:   ziyuanliu
# @Last Modified time: 2014-02-23 15:27:52

import tornado.web
import os.path
import redis
import logging
from adapter.administration import connect_to_db
from lib.redissession import RedisSessionStore
from controllers.apihandler import ApiHandler
from controllers.webhandler import WebHandler

# import threading
secureCookieSecret = "sph7r2uf"
class Application(tornado.web.Application):
	def __init__(self):
		self.mongo_db = connect_to_db("ts-server")
		self.redis = redis.StrictRedis()
		self.session_store = RedisSessionStore(self.redis)
		handlers = [
			(r"/",WebHandler),
			(r"/api",ApiHandler),
		]

		#ideally load shit from .ini file...
		settings = dict(
			cookie_secret=secureCookieSecret,
            template_path=os.path.join(os.path.dirname(__file__), "../templates"),
            static_path=os.path.join(os.path.dirname(__file__), "../static"),
            xsrf_cookies=False,
            debug=True,
			)
		
		tornado.web.Application.__init__(self,handlers,**settings)