#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: ziyuanliu
# @Date:   2014-02-23 15:23:56
# @Last Modified by:   ziyuanliu
# @Last Modified time: 2014-02-28 00:34:23

from basehandler import BaseHandler
import tornado.ioloop
from tornado.escape import url_escape
import logging
import json
from adapter import *

#mixpanel analytics
from mixpanel import Mixpanel

mp = Mixpanel('96985230011fa4df100eeb76e01b969e')

#format of a request - {'command',{PACKET}}, authentication through cookie session storage
#format of a return - {'return':[T/F], error:[MESSAGE], return_code:[0...n], message:[]}
#code: 0 - registration/login successful
#code: 1 - preference set 
class WebHandler(BaseHandler):
	def get(self):
		name = self.get_argument("recipe_name", default=None, strip=False)
		if name:
			print name
		else:
			self.render("index.html")

class ImageHandler(BaseHandler):
	def get(self,**kwargs):
		print kwargs['recipe_name']
		recipe_name=kwargs['recipe_name'].replace('+',' ')
		(ct,p) = get_picture_by_name(recipe_name)
		self.set_header('Content-type', ct)
		self.set_header('Content-length', len(p))
		self.write(p)
		self.finish()

