#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: ziyuanliu
# @Date:   2014-03-14 17:07:36
# @Last Modified by:   ziyuanliu
# @Last Modified time: 2014-03-14 21:20:14

from mongoengine import *

import logging
from ts_server.utils import datetime_now

class Ingredient(DynamicDocument):
	name = StringField(verbose_name='ingredient name', required=True, unique=True)
	thumbnail = StringField()
	category = StringField(verbose_name='ingredient category')
	description = StringField(verbose_name='ingredient description')
	date_added = DateTimeField(default=datetime_now,verbose_name='Ingredient date added')

	@classmethod
	def _by_id(cls,rid):
		try:
			a = cls.objects(pk=rid)
			if a.count()==1:
				return a[0]
			else:
				raise IngredientNotFound,'Ingredient %s' % rid
		except Exception as e:
			logging.debug(e)

	@classmethod
	def _by_name(cls,name):
		a = cls.objects(name=name)
		if a.count()==1:
			return a[0]
		else:
			raise IngredientNotFound,'Ingredient %s' % name

	@classmethod
	def _by_category(cls,name):
		a = cls.objects(category=name)
		if a.count()>0:
			return a
		else:
			raise IngredientNotFound,'category %s' % name

def new_ingredient(name="", thumbnail='',description='', category=""):
	try:
		Ingredient._by_name(name)
		raise IngredientExists
	except IngredientNotFound:
		
		a = Ingredient(name=name, thumbnail=thumbnail,description=description, category=category)
		a.save()
		return a


class IngredientNotFound(Exception): pass
class IngredientExists(Exception): pass
