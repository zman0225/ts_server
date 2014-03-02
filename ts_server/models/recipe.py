#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: ziyuanliu
# @Date:   2014-02-20 11:59:15
# @Last Modified by:   ziyuanliu
# @Last Modified time: 2014-03-01 15:12:50

from mongoengine import *

import logging
from ts_server.utils import datetime_now

class Recipe(DynamicDocument):
	name = StringField(verbose_name='food name', required=True, unique=True)
	image = FileField(default=None)
	category = StringField(max_length=30, verbose_name='food category')
	description = StringField(verbose_name='food description')
	time_required = DictField()
	source = StringField()
	servings = IntField()
	date_added = DateTimeField(default=datetime_now,verbose_name='recipe date added')

	#instruction and ingredients
	#this is a sorted list so it should always be in this order
	instructions = SortedListField(StringField())

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

	@classmethod
	def _by_category(cls,name):
		a = cls.objects(category=name)
		if a.count()==1:
			return a[0]
		else:
			raise RecipeNotFound,'category %s' % name

	@classmethod
	def _get_image_by_name(cls,name):
		r = cls._by_name(name)
		if r.image:
			image = r.image.read()
			content_type = r.image.content_type
			return (image,content_type)
		return None

	def set_image(self,fs, content_type):
		if self.image:
			self.image.put(fs,content_type=content_type)
		else:
			self.image.replace(fs,content_type=content_type)
		self.save()



def add_recipe(name="", description='', category="", instructions = [], servings=0, 
	time_required={}, ingredients={},source="",image=None):
	try:
		Recipe._by_name(name)
		raise RecipeExists
	except RecipeNotFound:
		
		a = Recipe(name=name, description=description, category=category, instructions=instructions,
			servings=servings, time_required=time_required, ingredients=ingredients, source=source)
		a.save()
		print a.instructions
		if image: 
			a.image.put(image,content_type='image/jpeg')
			a.save()
		return a


class RecipeNotFound(Exception): pass
class RecipeExists(Exception): pass



