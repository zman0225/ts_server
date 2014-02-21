#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: ziyuanliu
# @Date:   2014-02-20 12:20:14
# @Last Modified by:   ziyuanliu
# @Last Modified time: 2014-02-20 20:52:45

from models.account import *

import logging

def new_account(username,password,ip_addr):
	try:
		account = register(username,password,ip_addr)
		logging.debug("Account created [%s]"%account.username)
		return account
	except Exception as e:
		logging.debug("Account already exists!")
		return False

def login(username,password):
	return validate_login(username,password)

