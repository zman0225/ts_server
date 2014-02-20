#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: ziyuanliu
# @Date:   2013-12-08 15:28:33
# @Last Modified by:   ziyuanliu
# @Last Modified time: 2013-12-10 18:37:47
########################################################################################################
from mongoengine import connect

def connect_to_db(connection_name):
	return connect(connection_name)

def reset_db(connection_name):
	db = connect(connection_name)
	db.drop_database(connection_name)

def connect_to_remote_db(connection_name, ip, port, user, password):
	return connect(connection_name, host=ip,port=port,username=user,password=password)

