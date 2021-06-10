from numpy import load
from dotenv import load_dotenv
import requests as req
import os

load_dotenv()

def prep_data():
	lista=[]
	for k,v in data_tokens.items():
		nodo= v[v.price==v.price.min()].copy()
		nodo["token"]=k
		lista.append(nodo)
	return pd.concat(lista)

def test(text="Estoy andando pedazo de tontolin"):
	token = os.getenv("API_KEY")
	urlp = f"https://api.telegram.org/bot{token}"
	params = {"chat_id": os.getenv("CHAT_ID"), 
          "text":text}
	r = req.get(urlp + "/sendMessage", params=params)
	return r.json()






def main(data):
	tablita=prep_data(data)
	token = os.getenv("API_KEY")
	urlp = f"https://api.telegram.org/bot{token}"
	params = {"chat_id": os.getenv("CHAT_ID"), 
          "text":"\n\n".join(["\n".join([f"{x} = {str(z)}" for x,z in v.iteritems()]) for k,v in tablita.iterrows()])}
	r = req.get(urlp + "/sendMessage", params=params)