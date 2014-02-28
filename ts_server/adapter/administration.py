#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: ziyuanliu
# @Date:   2013-12-08 15:28:33
# @Last Modified by:   ziyuanliu
# @Last Modified time: 2014-02-26 21:27:03
########################################################################################################
from mongoengine import connect

def connect_to_db(connection_name, host=None, port=None, username=None, password=None):
	if host is not None and port is not None:
		return connect(connection_name, host=host, port=port)
	if username is not None and password is not None:
		return connect(connection_name, host=host, port=port, username=username, password=password)
	return connect(connection_name)

def reset_db(connection_name):
	db = connect(connection_name)
	db.drop_database(connection_name)

def connect_to_remote_db(connection_name, ip, port, user, password):
	return connect(connection_name, host=ip,port=port,username=user,password=password)

