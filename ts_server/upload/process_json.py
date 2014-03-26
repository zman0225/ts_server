

import json
import os.path

from ts_server.adapter.usercontrol import new_recipe
from ts_server.adapter.administration import connect_to_db
from ts_server.models.recipe import *
def process_recipe(recipe):
	name = recipe['name']
	category = recipe['category']
	instruction_list = list(recipe['instruction'])
	ingredients_dict = dict(recipe['ingredients'])
	new_dict = {}
	for key in ingredients_dict.keys():
		new_key = key.replace('.','').encode('utf-8')
		new_key = new_key.replace('?','')
		new_dict[new_key]=ingredients_dict[key]
	print new_dict
	time_dict = dict(recipe['time'])
	source = recipe['source'].encode('ascii', 'ignore')
	servings = recipe['servings']
	description = recipe['description'].encode('ascii', 'ignore')

	image_fs = 'ts_server/upload/'+name+".jpg"
	image = None
	if os.path.isfile(image_fs):
		image = open(image_fs,'r')

	print image_fs
	try:
		recipe = new_recipe(name=name, description=description, category=category, instructions = instruction_list, servings=servings, time_required=time_dict, ingredients=new_dict,source=source,image=image)
		print "creating new"
	except:
		print 'ALREADY IN DATABASE!'
	image.close()

def redo_instructions(recipe):
	r = Recipe._by_name(recipe['name'])
	instruction_list = list(recipe['instruction'])
	r.update(set__instructions=instruction_list)
	print "recipe updated: %s"%r.name

def read_json(fs):
	json_data=open(fs,'r')
	# print json_data
	data = json.load(json_data)
	json_data.close()
	i = 0
	for recipe in data:
		redo_instructions(recipe)
		# process_recipe(recipe)

if __name__ == '__main__':
	connect_to_db("ts-server",'23.253.209.158',27017,'ts_server','a2e7rqej')
	read_json('ts_server/upload/initial.json')