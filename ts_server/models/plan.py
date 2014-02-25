#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: ziyuanliu
# @Date:   2014-02-25 00:15:55
# @Last Modified by:   ziyuanliu
# @Last Modified time: 2014-02-25 14:55:33

from utils.utils import datetime_now

from mongoengine import *

# let each week start on a sunday, and the days of the week be number from 1 - 7
class plan(DynamicDocument):
	menu = SortedListField(ObjectIdField())

	# the key is the object id and the value is the day (1 - 7)
	menu_plan = DictField(default={}) 
	number = IntField()
	owner = ObjectIdField(required=True)
	subscribed = BooleanField(default=True)
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

