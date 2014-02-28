#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: ziyuanliu
# @Date:   2014-02-20 12:20:14
# @Last Modified by:   ziyuanliu
# @Last Modified time: 2014-02-28 10:43:16

from models.account import *
from models.recipe import *
from models.plan import *
from lib.redisrelations import get_recipe_by_category

import logging
import redis
import random
import cPickle

r = redis.Redis()

def new_account(username,password,ip_addr,email):
	try:
		account = register(username,password,ip_addr,email)
		logging.info("Account created [%s]"%account.username)
		return account
	except Exception as e:
		logging.info("Account already exists! "+str(e))
		return False

def new_ts_account(username, password, ip_addr, gender, age, email):
	acc = new_account(username,password,ip_addr,email)
	if acc:
		acc.gender = gender;
		acc.age = int(age)
		acc.email = email
		acc.save()
		logging.info("account created!")
		return acc
	else:
		return False

def set_preferences(uid,prefs,meals):
	acc = Account._by_id(uid)
	acc.set_preference(prefs)
	acc.set_meals(meals)

def get_preferences(uid):
	acc = Account._by_id(uid)
	return (acc.preference,acc.meals)

def get_all_categories():
	return list(r.smembers('categories'))

def get_picture_by_name(name):
	r = Recipe._by_name(name)
	return get_picture_by_id(rid=None,recipe_obj=r)
	# return (r.image.content_type,r.image.read())

def get_picture_by_id(rid,recipe_obj=None):
	rid = str(rid) if rid is not None else str(recipe_obj.pk)
	key = "image:"+str(rid)
	if r.exists(key):
		# logging.info("exists!")
		r.expire(key,120)
		kw = cPickle.loads(r.get(key))
		return (kw['content_type'],kw['img'])
	else:
		re = recipe_obj if recipe_obj is not None else Recipe._by_id(rid) 

		content_type = re.image.content_type
		img = re.image.read()

		kw = {"content_type":content_type,"img":img}
		pickled_object = cPickle.dumps(kw)
		r.setex(key,pickled_object,120)
		return (content_type,img)

def get_recipe_by_id(name):
	pass

def get_recipe_by_id(rid, recipe_obj=None):
	rid = str(rid) if rid is not None else str(recipe_obj.pk)
	key = "recipe:"+str(rid)
	if r.exists(key):
		logging.info("exists!")
		r.expire(key,240)
		kw = cPickle.loads(r.get(key))
		return kw
	else:
		re = recipe_obj if recipe_obj is not None else Recipe._by_id(rid) 

		kw = {"name":re.name,"category":re.category,"description":re.description,"time_required":re.time_required,
			"source":re.source,"servings":re.servings,"instruction":re.instruction, "ingredients":re.ingredients}
		pickled_object = cPickle.dumps(kw)
		r.setex(key,pickled_object,240)
		return kw

def new_recipe(name, description='', category="", instructions = [], servings=0, 
	time_required=0, ingredients={},source="",image=None):
	add_recipe(name=name, description=description, category=category, instructions = instructions, servings=servings, 
		time_required=time_required, ingredients=ingredients,source=source,image=image)

def login(username,password):
	return validate_login(username,password)

# Move to processing server

def create_plan(uid):
	acc = Account._by_id(uid)
	pref = acc.preference
	meals = acc.meals
	plans = []
	for i in range(meals):

		ind = random.randint(0,len(pref)-1) if len(pref)>0 else 0
		recipes = get_recipe_by_category(pref[ind])

		re_ind = random.randint(0,len(recipes)-1) if len(pref)>0 else 0
		counter = 0
		while recipes[re_ind] in plans:
			re_ind = random.randint(0,len(recipes)-1) if len(pref)>0 else 0
			counter = counter + 1
			if counter == 20:
				ind = random.randint(0,len(pref)-1) if len(pref)>0 else 0
				recipes = get_recipe_by_category(pref[ind])
				counter = 0

		plans.append(recipes[re_ind])


	pref = new_plan(uid,plans)
	return pref;
	# new_plan(uid,recipe_list)






