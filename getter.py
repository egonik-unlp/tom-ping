import requests as req
import pandas as pd
from notification import prep_data
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
		data_tokens[token]= pd.concat((pd.DataFrame(product),pd.DataFrame(seller)), axis=1)
	return data_tokens


def consulta():
    data=main()
    lista=[]
    for k,v in data.items():
	nodo= v[v.price==v.price.min()].copy()
	nodo["token"]=k
	lista.append(nodo)
    return pd.concat(lista, axis=0)
