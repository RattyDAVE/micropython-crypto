from functions import *
import time
import umachine

config_file="config.json"
config=dict()
config=config_load(config_file)

#print(config)

## START

#Debug
#rawlivecoin = getgecko(config)
#print(allcoins(rawlivecoin,config))


# Main Loop
while True:
    #Get prices from coingeko in ONE api call
    rawlivecoin = getgecko(config)

    #Add up the totals
    total=0
    for i in rawlivecoin: total+=config['quantity'][i['id']]*i['current_price']

    #Log the result    
    #ap_text='"'+datetime()+'"'+','+str("%.2f" % total)
    ap_text=str(time.time())+','+str("%.2f" % total)
    
    filename='logs/'+date()+'.log'
    
    if not file_exist(filename):
        #print("DEBUG - File "+filename+" NOT FOUND")
        #settime()
        file_append('logs/daily.log', ap_text)
        
    print(filename,ap_text)
    file_append(filename, ap_text)
    
    #Sleep as not to overload the Coingeko API
    time.sleep(300)
    

