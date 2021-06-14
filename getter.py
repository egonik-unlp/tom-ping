from datetime import datetime
import requests as req
import pandas as pd
from database_management import db, Token, Offer



def main()->dict:
	url= "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"

	tokens=["USDT","BTC","BUSD","BNB","ETH","DAI"]
	data_tokens={}
	for token in tokens:
		data=[]
		for n in range(1,2):
			response = req.post(url=url, json={"page":n,"rows":10,"payTypes":[],"asset":token,"tradeType":"BUY","fiat":"ARS","publisherType":None,"merchantCheck":False,"transAmount":""})
			for node in response.json()["data"]:
				seller_params=node["advertiser"]
				token_params=node["adv"]
				methods=[]
				for transaction_method in token_params["tradeMethods"]:
					methods.append(transaction_method["identifier"])
				data.append({
					"user_name":seller_params["nickName"],
					"user_id":seller_params["userNo"],
					"finish_rate":seller_params["monthFinishRate"],
					"order_count":seller_params["monthOrderCount"],
					"methods": ", ".join(methods),
					"max_single_trans_amount":float(token_params["dynamicMaxSingleTransAmount"]),
					"min_single_trans_amount":float(token_params["minSingleTransAmount"]),
					"available":float(token_params["dynamicMaxSingleTransAmount"]),
					"price":float(token_params["price"]),
			
				})
		data_tokens[token]=data
	return data_tokens

def store_query_in_db():
	data=main()
	r,h=[],[]
	for keys, values in data.items():
		db_id=Token.query.filter_by(name=keys).with_entities(Token.token_id).first()[0]
		for value in values:
			if Offer.query.filter_by(**value).all():
				pass
			else:
				offer= Offer(**value,token_id= db_id)
				h.append(Offer.query.filter_by(**value).all())
				db.session.add(offer)
				print('wrote an offer, {}'.format(offer.user_name))
		db.session.commit()

def consulta():
  data=main()
  lista=[]
  for k,v in data.items():
    nodo = v[v.price==v.price.min()].copy()
    nodo["token"]=k
    lista.append(nodo)
  return pd.concat(lista, axis=0)



if __name__=="__main__":
	q=store_query_in_db()