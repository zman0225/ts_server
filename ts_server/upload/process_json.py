

import json
import os.path

from adapter.usercontrol import new_recipe
from adapter.administration import connect_to_db
def process_recipe(recipe):
	name = recipe['name']
	category = recipe['category']
	instruction_list = list(recipe['instruction'])
	ingredients_dict = dict(recipe['ingredients'])
	for key in ingredients_dict.keys():
		new_key = key.replace('.','')
		new_key = new_key.replace('?','')
		ingredients_dict[new_key]=ingredients_dict[key]
		del ingredients_dict[key]
	time_dict = dict(recipe['time'])
	source = recipe['source'].encode('ascii', 'ignore')
	servings = recipe['servings']
	description = recipe['description'].encode('ascii', 'ignore')

	image_fs = 'upload/'+name+".jpg"
	image = None
	if os.path.isfile(image_fs):
		image = open(image_fs,'r')

	recipe = new_recipe(name=name, description=description, category=category, instructions = instruction_list, servings=servings, time_required=time_dict, ingredients=ingredients_dict,source=source,image=image)
	image.close()

def read_json(fs):
	json_data=open(fs,'r')
	# print json_data
	data = json.load(json_data)
	json_data.close()
	i = 0
	for recipe in data:
		process_recipe(recipe)

if __name__ == '__main__':
	connect_to_db("ts-server")
	read_json('upload/initial.json')