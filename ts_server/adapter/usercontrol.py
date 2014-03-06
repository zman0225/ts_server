#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: ziyuanliu
# @Date:   2014-02-20 12:20:14
# @Last Modified by:   ziyuanliu
# @Last Modified time: 2014-03-06 00:34:42

from ts_server.models.account import *
from ts_server.models.recipe import *
from ts_server.models.plan import *
from ts_server.lib.redisrelations import get_recipe_by_category, get_recipe_name_by_id

import logging
import redis
import random
import cPickle
import time

r = redis.Redis()

from ts_server.lib.analytics import mp

def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print '%s function took %0.3f ms' % (f.func_name, (time2-time1)*1000.0)
        return ret
    return wrap

def new_account(username,password,ip_addr,email):
	try:
		account = register(username,password,ip_addr,email)
		logging.info("Account created [%s]"%(str(account.username)))
		return account
	except Exception as e:
		logging.info("Account already exists! "+str(e))
		return False

def new_ts_account(username, password, ip_addr, gender, age, email):
	acc = new_account(username,password,ip_addr,email)
	if acc:
		acc.gender = gender;
		acc.age = int(age)
		acc.email = email.lower()
		acc.save()
		mp.people_set(str(acc.pk), {
		    '$username'    : username,
		    '$email'         : email,
		    '$age'         : age,
		    '$ip'		:ip_addr	
		})
		mp.track(str(acc.pk), 'register')
		logging.info("account %s created!"%(str(acc.pk)))
		return acc
	else:
		return False

def set_preferences(uid,prefs,meals):
	acc = Account._by_id(uid)
	mp.track(uid, 'preference change', {
		'new preferences':prefs,
		'new meals planned':meals,
		'old preferences':acc.preference,
		'old meals planned':acc.meals
		})
	acc.set_preference(prefs)
	acc.set_meals(meals)

def get_preferences(uid):
	logging.info(uid)
	acc = Account._by_id(uid)
	logging.info("sub ret is now "+str(acc.subscribed))
	return (acc.preference,acc.meals,acc.subscribed)

def set_subscribed(uid,val):
	acc = Account._by_id(uid)
	acc.update(set__subscribed=val)
	mp.track(uid, 'subscribed' if val else 'unsubscribed')
	logging.info("sub is now "+str(val))

def get_all_categories():
	return list(r.smembers('categories'))

@timing
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

def get_recipe_by_name(name):
	pass

def get_recipe_by_id(rid, recipe_obj=None):
	rid = str(rid) if rid is not None else str(recipe_obj.pk)
	key = "recipe:"+str(rid)
	if r.exists(key):
		r.expire(key,240)
		kw = cPickle.loads(r.get(key))
		return kw
	else:
		re = recipe_obj if recipe_obj is not None else Recipe._by_id(rid) 
		logging.info(rid)
		kw = {"name":re.name,"category":re.category,"description":re.description,"time_required":re.time_required,
			"source":re.source,"servings":re.servings,"instructions":re.instructions, "ingredients":re.ingredients}

		pickled_object = cPickle.dumps(kw)
		r.setex(key,pickled_object,240)
		return kw

def new_recipe(name, description='', category="", instructions = [], servings=0, 
	time_required=0, ingredients={},source="",image=None):
	add_recipe(name=name, description=description, category=category, instructions = instructions, servings=servings, 
		time_required=time_required, ingredients=ingredients, source=source,image=image)

def login(username,password):
	return validate_login(username,password)

# Move to processing server
def get_latest_plan(uid):
	
	acc = Account._by_id(uid)
	plan = acc.current_plan
	if plan is not None:
		mp.track(uid, 'requesting latest plan')
		return plan
	return create_plan(uid=uid,acc_obj=acc)

def create_plan(uid, acc_obj=None):
	mp.track(uid, 'generating new plan')
	acc = Account._by_id(uid) if acc_obj is None else acc_obj
	pref = acc.preference
	meals = acc.meals
	plans = []
	recipe_name = []
	for i in range(meals):
		ind = random.randint(0,len(pref)-1) if len(pref)>0 else 0
		recipes = get_recipe_by_category(pref[ind])

		if meals > len(recipes) and i==len(recipes)-1:
			break
		re_ind = random.randint(0,len(recipes)-1) if len(pref)>0 else 0
		counter = 0
		while recipes[re_ind] in plans:
			re_ind = random.randint(0,len(recipes)-1) if len(pref)>0 else 0
			counter = counter + 1
			if counter == 20:
				ind = random.randint(0,len(pref)-1) if len(pref)>0 else 0
				recipes = get_recipe_by_category(pref[ind])
				counter = 0

		recipe_name.append(get_recipe_name_by_id(recipes[re_ind]))
		plans.append(recipes[re_ind])


	kw = {"recipes":recipe_name,"username":acc.username,"email":acc.email};
	pickled = cPickle.dumps(kw)
	r.hset("email",str(acc.pk),pickled)
	logging.info("menu added to email queue %s"%uid)
	pref = new_plan(uid,plans)
	acc.current_plan = pref
	acc.save()
	return pref;






