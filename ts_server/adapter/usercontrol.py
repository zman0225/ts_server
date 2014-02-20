#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: ziyuanliu
# @Date:   2014-02-20 12:20:14
# @Last Modified by:   ziyuanliu
# @Last Modified time: 2014-02-20 12:20:41

from ts_server.models.account import *

import logging

def new_account(username,password,ip_addr):
	try:
		account = register(username,password,ip_addr)
		logging.debug("Account created [%s]"%account.username)
		return account
	except Exists:
		logging.debug("Account already exists!")
		return False