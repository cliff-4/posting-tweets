import json
import csv

def get_cred(cred):
	"""Argument has to be a string since its retreiving from a json file."""
	with open("credentials.json", "r") as j:
		kekw = json.load(j)
		try: 
			return kekw[cred]
		except KeyError: 
			print('"{}"'.format(cred))
			print("No such key exists in credentials.json. Maybe check the key or try get_id() instead.")
			return None

def get_id(identifier):
	"""Argument has to be a string since its retreiving from a json file."""
	with open("personal/tweet_ids.json", "r") as j:
		kekw = json.load(j)
		try: 
			return kekw[identifier]
		except KeyError: 
			print("No such key exists in tweet_ids.json. Maybe check the key or try get_cred() instead.")
			return None

def get_csv(file_name):
	"""Returns an array with the lines of the csv as different elements"""
	filename = file_name
	return_list = []
	with open(filename, 'r') as csvfile:
		csvreader = csv.reader(csvfile)
		next(csvreader) # to remove the field names
		for row in csvreader:
			return_list.append(row)
	return return_list

def get_json(filename):
	with open(filename, "r") as j:
		return json.load(j)

if __name__ == "__main__":
	print("This is a side script to get credentials and ids, since repetitive calling of with open bla bla bla was too much.")
	print("Just import this file and use the functions. Simple as that. Got it? No? Good.")
	print(get_cred("client_id"))
