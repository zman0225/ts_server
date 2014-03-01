#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: ziyuanliu
# @Date:   2014-02-20 11:46:18
# @Last Modified by:   ziyuanliu
# @Last Modified time: 2014-02-28 23:46:43


import logging
import tornado.options
import tornado.ioloop
import tornado.options

from ts_server.models.recipe import *
from lib.redisrelations import set_all_categories
from tornado.options import define, options
from config.middleware import Application

def load_recipes():
	all_recipes = Recipe.objects()
	set_all_categories(all_recipes)

def main():
	define("port", default=8888, help="run on the given port", type=int)
	tornado.options.parse_command_line()
	app=Application()
	load_recipes()
	app.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
	main()

