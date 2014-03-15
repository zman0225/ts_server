#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: ziyuanliu
# @Date:   2014-03-14 16:46:10
# @Last Modified by:   ziyuanliu
# @Last Modified time: 2014-03-14 22:13:38
# will be used to update models/manage inconsistencies

# api = "http://api.walmartlabs.com/v1/search?apiKey=7cy4c9uth2a6w5w6natn9vpj&query=soy+sauce&format=json"
apiKey = "7cy4c9uth2a6w5w6natn9vpj"
import requests
import time

from ts_server.models.ingredient import *
from ts_server.models.recipe import *
def searchAPI(item):
	a = item.replace(" ", "+").lower()
	print a
	return "http://api.walmartlabs.com/v1/search?apiKey=%s&query=%s&format=json&categoryId=976759"%(apiKey,a)

def add_ingredient_to_db(item):
	item = item.strip().lower()
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
	for re in Recipe.objects:
		add_from_recipe(re)

def add_from_recipe(recipe):
	# first step is to check if the ingredient already exists
	ingredients = recipe.ingredients
	for ingredient in ingredients:
		ingredient = ingredient.strip().lower()
		try:
			ingre = Ingredient._by_name(ingredient)
			print ingredient,"already exists"
		except Exception:
			# add it 
			
			add_ingredient_to_db(ingredient)


if __name__ == '__main__':
	from ts_server.adapter.administration import connect_to_db
	mongo_db = connect_to_db("ts-server",'23.253.209.158',27017,'ts_server','a2e7rqej')
	add_all()

