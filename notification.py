from numpy import load
from dotenv import load_dotenv
import requests as req
import pandas as pd
import os

load_dotenv()


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