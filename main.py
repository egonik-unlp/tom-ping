import getter , notification
import pandas as pd

data=getter.main()



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
		if offers.shape[0]==0:
			pass
		else:
			candidates.append(offers)
	if len(candidates) > 0:
		return pd.concat(candidates, axis=0)
	else:
		return False
	
def main():
	params=[
			{
			'token':'USDT',
			'target':40000,
			'finish_rate':80,
			'order_count':20
			}
		]
		
	notification.test()
	data=getter.main()
	candidates=filter(data, params)
	if candidates:
		notification.main(candidates)
	print('iteration->{}'.format(candidates))



