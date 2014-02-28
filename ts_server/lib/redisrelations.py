#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: ziyuanliu
# @Date:   2014-02-25 19:43:32
# @Last Modified by:   ziyuanliu
# @Last Modified time: 2014-02-27 21:54:00

import redis

from models.recipe import *
r = redis.Redis()

# keeps a set of all of the availiable food categories
def set_all_categories(all_recipes):
	for recipe in all_recipes:
		cat = str(recipe.category)
		r.sadd('categories',cat.title())
		recipe_id = str(recipe.pk)
		add_to_category(recipe_id,cat)

def add_to_category(recipe_id,category):
	r.sadd(category,recipe_id)

def get_recipe_by_category(category):
	return list(r.smembers(category))
