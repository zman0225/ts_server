#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: ziyuanliu
# @Date:   2014-02-20 12:20:14
# @Last Modified by:   ziyuanliu
# @Last Modified time: 2014-02-24 12:39:34

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

def new_ts_account(username, password, ip_addr, gender, age, email):
	acc = new_account(username,password,ip_addr)
	if acc:
		acc.gender = gender;
		acc.age = int(age)
		acc.email = email
		acc.save()
		return acc
	else:
		return False
		
def login(username,password):
	return validate_login(username,password)

