import requests as req
import pandas as pd
from database_management import db, Token, Offer



def main()->dict:
	url= "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"

	tokens=["USDT","BTC","BUSD","BNB","ETH","DAI"]
	data_tokens={}
	for token in tokens:
		seller= []
		product=[]
		for n in range(1,2):
			response = req.post(url=url, json={"page":n,"rows":10,"payTypes":[],"asset":token,"tradeType":"BUY","fiat":"ARS","publisherType":None,"merchantCheck":False,"transAmount":""})
			for node in response.json()["data"]:
				seller_params=node["advertiser"]
				seller.append({
					"user_name":seller_params["nickName"],
					"user_id":seller_params["userNo"],
					"finish_rate":seller_params["monthFinishRate"],
					"order_count":seller_params["monthOrderCount"]
				})
				token_params=node["adv"]
				methods=[]
				for transaction_method in token_params["tradeMethods"]:
					methods.append(transaction_method["identifier"])
				product.append({
					"methods": ", ".join(methods),
					"max_single_trans_amount":float(token_params["dynamicMaxSingleTransAmount"]),
					"min_single_trans_amount":float(token_params["minSingleTransAmount"]),
					"available":float(token_params["dynamicMaxSingleTransAmount"]),
					"price":float(token_params["price"]),
			
				})
		# data_tokens[token]= pd.concat((pd.DataFrame(product),pd.DataFrame(seller)), axis=1)
		data_tokens[token]=product, seller
	return data_tokens
def store_query_in_db():
	data=main()
	for keys, values in data.items():
		db_id=Token.query.filter_by(name=keys).with_entities(Token.token_id).first()
		for value in values:
			offer= Offer(value["price"], db_id[0])
			db.session.add(offer)
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
	store_query_in_db()