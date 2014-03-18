#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: ziyuanliu
# @Date:   2014-03-14 16:46:10
# @Last Modified by:   ziyuanliu
# @Last Modified time: 2014-03-18 01:04:22
# will be used to update models/manage inconsistencies

# api = "http://api.walmartlabs.com/v1/search?apiKey=7cy4c9uth2a6w5w6natn9vpj&query=soy+sauce&format=json"
apiKey = "5810a3fa15"
import requests
import time


from ts_server.lib.redisrelations import *

from xml.etree import ElementTree
from ts_server.lib.languageprocess import *
from ts_server.models.ingredient import *
from ts_server.models.recipe import *
def searchAPI(item):
	a = item.replace(" ", "+").lower()
	# print a
	return "http://www.SupermarketAPI.com/api.asmx/SearchByProductName?APIKEY=%s&ItemName=%s"%(apiKey,a)

def add_ingredient(item):
	copy_item = str(item)
	item = item.strip().split(',')[0].split(' and ')[0].split(' or ')[0].strip()
	if ingredient_exist(copy_item) or ingredient_exist(item):
		return

	req = searchAPI(item)
	r = requests.get(req)
	if r.status_code==200:
		tree = ElementTree.fromstring(r.content)
		if len(tree)>0:
			print item
			cats = [child[2].text for child in tree]
			cats = list(set(cats))
			print '\t',cats
			ind = raw_input("index: (-1) for uncategorized")
			ind = int(ind)
			if ind>-1:
				add_ingredient_to_redis(copy_item,cats[ind])
				add_ingredient_to_redis(item,cats[ind])
			else:
				add_ingredient_to_redis(item,"uncategorized")
		else: 
			item = get_nouns(item)
			r = requests.get(searchAPI(item)) 
			if r.status_code==200:
				tree = ElementTree.fromstring(r.content)
				if len(tree)>0:
					print item
					cats = [child[2].text for child in tree]
					cats = list(set(cats))
					print '\t',cats
					ind = raw_input("index: (-1) for uncategorized")
					ind = int(ind)
					if ind>-1:
						add_ingredient_to_redis(copy_item,cats[ind])
						add_ingredient_to_redis(item,cats[ind])
				else:
					add_ingredient_to_redis(item,"uncategorized")
					print item, "uncategorized"

def add_ingredient_to_db(item):
	item = item.strip()
	item = item.replace(',','').replace('.','')

	# walmart rate limits
	time.sleep(0.05)
	req = searchAPI(item)
	print 'req is',req
	r = requests.get(req)
	if r.status_code==200:
		kw = r.json()
		if 'items' in kw:
			first_item = kw['items'][0]
			description = ''
			if 'shortDescription' in first_item:
				description = first_item['shortDescription']
			elif 'longDescription' in first_item:
				description = first_item['longDescription']
			thumbnail = first_item['thumbnailImage']
			category = first_item['categoryPath']
			category = category.split('/')
			category = category[len(category)-1]
			print item, description, thumbnail, 'cat', category
			print '\n'
			try:
				new_ingredient(name=item, thumbnail=thumbnail,description=description, category=category)
			except Exception:
				pass
		else:
			category = 'other'
			try:
				new_ingredient(name=item, thumbnail='',description='', category="")
			except Exception:
				pass
	else:
		print "status code error:",r.status_code

def add_all():
	# first step is to go through the all the ingredients
	f = open('ingredients.txt','w')
	master_list = []
	for re in Recipe.objects:
		master_list.extend(add_from_recipe(re))
	for a in set(master_list):
		f.write(a) # python will convert \n to os.linesep
	f.close() # you can omit in most cases as the destructor will call if

def add_from_recipe(recipe):
	# first step is to check if the ingredient already exists
	ingredients = recipe.ingredients
	lst = []
	for ingredient in ingredients:
		# add_ingredient(ingredient)
		
		lst.append(ingredient.encode("utf-8").strip()+'\n')
	return lst

def load_into_db():
	ing = []
	with open('ts_server/adapter/ingredients.txt') as fp:
	    for line in fp:
	        ing.append(line)
	key = ing[0]
	ing = ing[1:]
	key = [s.strip() for s in key.split(';')]
	for k in ing:
		v = k.split(":")
		name = v[0].decode("utf-8").strip()
		short_name = get_nouns(name)
		cat = key[int(v[1].strip())]
		try:
			new_ingredient(name=name, thumbnail='',description='', category=cat)
		except Exception:
			print name,"is already in here"

		try:
			new_ingredient(name=short_name, thumbnail='',description='', category=cat)
		except Exception:
			print short_name,"is already in here"

if __name__ == '__main__':
	from ts_server.adapter.administration import connect_to_db
	mongo_db = connect_to_db("ts-server",'23.253.209.158',27017,'ts_server','a2e7rqej')
	load_into_db()

