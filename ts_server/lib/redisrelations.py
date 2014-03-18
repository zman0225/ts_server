#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: ziyuanliu
# @Date:   2014-02-25 19:43:32
# @Last Modified by:   ziyuanliu
# @Last Modified time: 2014-03-17 14:18:10

import redis

from ts_server.models.recipe import *
r = redis.Redis()

# keeps a set of all of the availiable food categories
def set_all_categories(all_recipes):
	for recipe in all_recipes:
		cat = str(recipe.category)
		r.sadd('categories',cat.title())
		recipe_id = str(recipe.pk)
		add_to_category(recipe_id,cat,recipe.name)

def map_id_to_name(recipe_id,name):
	r.hset(recipe_id,"name",name)

def add_to_category(recipe_id,category,name):
	r.sadd(category,recipe_id)
	map_id_to_name(recipe_id,name)

def get_recipe_name_by_id(recipe_id):
	return r.hget(recipe_id,"name")

def get_recipe_by_category(category):
	return list(r.smembers(category))

def get_categories():
	return r.smembers('categories')

def add_ingredient_to_redis(item,category):
	r.hsetnx('ingredients',item,category)

def add_ingredients_to_redis(kw):
	return r.msetnx(kw)

def get_ingredient_category(item):
	return r.hget('ingredients',item)

def ingredient_exist(item):
	return r.hexists('ingredients',item)