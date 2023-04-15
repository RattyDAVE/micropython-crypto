from functions import *
from urequests import get
#import math


config_file="config.json"
config=dict()
config=config_load(config_file)

coin="bitcoin"
days=2


def getchart(config, coin, days):
    chart_url="https://api.coingecko.com/api/v3/coins/"+coin+"/market_chart?vs_currency="+config['currency']+"&days="+str(days)
    rawlivecoin = get(chart_url, headers=config['headers']).json()
    price_list=[]
    for i in rawlivecoin['prices']: price_list.append(i[1])
    return(price_list)

price_list=getchart(config, coin, days)

print("Length = "+str(len(price_list)))
print("Min Value = "+str(min(price_list)))
print("Max Value = "+str(max(price_list)))


graphit(price_list,coin,days)
