

import json



if __name__ == '__main__':
	json_data=open('initial.json','r')
	# print json_data
	data = json.load(json_data)
	json_data.close()
	
	