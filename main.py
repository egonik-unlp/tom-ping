import getter , notification
import pandas as pd
import requests as req
# data=getter.main()



def filter(data, params):
	candidates=[]
	for param in params:
		offers=data[param['token']]
		offers= offers[
			(offers['max_single_trans_amount'] > param['target']) &
			(offers['min_single_trans_amount'] < param['target']) &
			(offers['finish_rate'] >= param['finish_rate'])&
			(offers['order_count'] >= param['order_count'])
		]
		print(offers)
		if offers.shape[0]==0:
			pass
		else:
			candidates.append(offers)
	if len(candidates) > 0:
		return pd.concat(candidates, axis=0), True
	else:
		return 'Void', False
	
def main():
	params=[
			{
				'token':'USDT',
				'target':40000,
				'finish_rate':.80,
				'order_count':20
			},
			{
				'token':'BTC',
				'target':5000,
				'finish_rate':.20,
				'order_count':1
			}
		]
		
	# notification.test()
	data=getter.main()
	candidates=filter(data, params)
	if candidates[1]:
		r=notification.main(candidates[0])
		log=candidates[0].to_html()
	else:
		log=data['BTC'].to_html()
	print('iteration->{}'.format(candidates))
	
	with open('falopa.html' , 'w') as file:
		file.write(log)
	
