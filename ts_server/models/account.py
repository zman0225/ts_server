#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: ziyuanliu
# @Date:   2014-02-20 11:53:49
# @Last Modified by:   ziyuanliu
# @Last Modified time: 2014-02-24 15:07:31

from lib.authentication import constant_time_compare
from utils.utils import datetime_now
from utils.utils import *
from mongoengine import *
import bcrypt

workfactor = 12
class Account(Document):
	username = StringField(max_length=20, unique=True, required=True)
	password = StringField(max_length=200, required=True)
	first_name = StringField(max_length=30, verbose_name='first name')
	last_name = StringField(max_length=30, verbose_name='last name')
	email = StringField(max_length=30, verbose_name='email address',unique=True)
	date_joined = DateTimeField(default=datetime_now,verbose_name='date joined')
	age = IntField()
	gender = StringField(max_length=30)
	#food preference 
	preference = ListField(default=[],verbose_name='Food/Taste preference')

	@classmethod
	def _by_id(cls,uid):
		try:
			a = cls.objects(pk=uid)
			if a.count()==1:
				return a[0]
			else:
				raise AccountNotFound,'Account %s' % uid
		except Exception as e:
			logging.debug(e)

	@classmethod
	def _by_username(cls,username):
		a = cls.objects(username=username)
		if a.count()==1:
			return a[0]
		else:
			raise AccountNotFound,'Account %s' % username

	@classmethod
	def _by_email(cls,email):
		a = cls.objects(email=email)
		if a.count()==1:
			return a[0]
		else:
			raise AccountNotFound,'Account %s' % email

def register(username, password, remote_ip,email):
	try:
		a = Account._by_username(username=username)
		raise AccountExists, "%s is already in the database"
	except AccountNotFound:
		a = Account(username=username,password=bcrypt_password(password),registration_ip=remote_ip,email=email)
		a.save()
		return a
		
def bcrypt_password(password):
    salt = bcrypt.gensalt(log_rounds=workfactor)
    return bcrypt.hashpw(password, salt)

def change_password(account, newpassword):
    account.password = bcrypt_password(newpassword)
    account.update()
    return True

def validate_login(username, password):
	try:
		a = None
		if '@' in username:
			a = Account._by_email(username)
		else:
			a = Account._by_username(username)
		if validate_password(a, password):
			return a
		else:
			return False
	except AccountNotFound:
		return False

def validate_password(a, password):
	#security against time attacks
	expect_hash = bcrypt.hashpw(password,a.password)
	if not constant_time_compare(a.password,expect_hash):
		return False

	wf = int(a.password.split("$")[2])
	if wf == workfactor:
		return a
	else:
		return False

class AccountNotFound(Exception): pass
class AccountExists(Exception): pass


