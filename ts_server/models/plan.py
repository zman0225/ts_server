#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: ziyuanliu
# @Date:   2014-02-25 00:15:55
# @Last Modified by:   ziyuanliu
# @Last Modified time: 2014-03-01 12:47:57


from ts_server.utils import datetime_now

from mongoengine import *

# let each week start on a sunday, and the days of the week be number from 1 - 7
class Plan(DynamicDocument):
	# the key is the object id and the value is the day (1 - 7)
	menu_plan = ListField(default=[]) 
	owner = ObjectIdField(required=True)
	date_added = DateTimeField(default=datetime_now,verbose_name='recipe date added')

	@classmethod
	def _by_id(cls,rid):
		try:
			a = cls.objects(pk=rid)
			if a.count()==1:
				return a[0]
			else:
				raise RecipeNotFound,'Recipe %s' % rid
		except Exception as e:
			logging.debug(e)

	@classmethod
	def _by_name(cls,name):
		a = cls.objects(name=name)
		if a.count()==1:
			return a[0]
		else:
			raise RecipeNotFound,'Recipe %s' % name

def new_plan(uid,recipe_list=[]):
	week = Plan(owner=uid,menu_plan=recipe_list)
	week.save()
	return week
