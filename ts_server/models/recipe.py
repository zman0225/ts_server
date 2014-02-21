#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: ziyuanliu
# @Date:   2014-02-20 11:59:15
# @Last Modified by:   ziyuanliu
# @Last Modified time: 2014-02-20 15:47:20
from utils.utils import datetime_now

from mongoengine import *

class Recipe(DynamicDocument):
	name = StringField(max_length=30, verbose_name='food name', required=True)
	category = StringField(max_length=30, verbose_name='food category')
	description = StringField(max_length=300, verbose_name='food description')
	time_required = IntField()
	servings = IntField()
	date_added = DateTimeField(default=datetime_now,verbose_name='recipe date added')

	#instruction and ingredients
	#this is a sorted list so it should always be in this order
	instruction = SortedListField(default=[],verbose_name='recipe preparation')

	#the ingredients list will be in the following format NAME:amount 
	# amount will be in the following format - NUMBER:UNIT
	ingredients = DictField()

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

def NewRecipe(name, description='', category=category, instructions = [], servings=0, time_required=0, ingredients={}):
	try:
		Recipe._by_name(username=username)
		raise RecipeExists
	except RecipeNotFound:
		a = Recipe(name=name, description='', category=category, instructions = [], servings=0, time_required=0, ingredients={})
		a.save()
		return a

class RecipeNotFound(Exception): pass
class RecipeExists(Exception): pass



