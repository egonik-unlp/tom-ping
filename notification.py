from numpy import load
from dotenv import load_dotenv
import requests as req
import pandas as pd
import os

load_dotenv()

def prep_data(data):
	lista=[]
	print(data)
	
	# for v in data.values:
	# 	lista.append(v)
	# return_val=pd.concat(lista, axis=0)
	# print('se viene se viene')
	# print(return_val)
	return return_val

def test(text="Estoy andando pedazo de tontolin"):
	token = os.getenv("API_KEY")
	urlp = f"https://api.telegram.org/bot{token}"
	params = {"chat_id": os.getenv("CHAT_ID"), 
          "text":text}
	r = req.get(urlp + "/sendMessage", params=params)
	return r.json()






def main(data):
	tablita=data
	print(tablita)
	token = os.getenv("API_KEY")
	urlp = f"https://api.telegram.org/bot{token}"
	try:
		package="\n\n".join(["\n".join([f"{x} = {str(z)}" for x,z in v.iteritems()]) for k,v in tablita.iterrows()])
	except AttributeError:
		package="\n".join([f"{x} = {str(z)}" for x,z in tablita.iteritems()])
	params = {"chat_id": os.getenv("CHAT_ID"), 
          "text":package}

	r = req.get(urlp + "/sendMessage", params=params)
	return r