#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: ziyuanliu
# @Date:   2014-02-23 15:23:56
# @Last Modified by:   ziyuanliu
# @Last Modified time: 2014-02-23 15:25:49

from basehandler import BaseHandler
import tornado.ioloop
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
		self.render("index.html")



