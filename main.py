from functions import *
import time
import umachine

from EPD_2in13_B_V4_Landscape import EPD_2in13_B_V4_Landscape
epd=EPD_2in13_B_V4_Landscape()

config_file="config.json"
config=dict()
config=config_load(config_file)
screen=1
filedir='logs'
filename=filedir+'/data.log'

screen_options = {
    1: {'time_period': 86400, 'title': 'Last 24h'},
    2: {'time_period': 86400 * 360, 'title': 'Max Days'}

}
valid_screens = [1, 2]

# Main Loop
while True: # Main Loop
    try:
        formatted_date = time.strftime('%Y%m%d', time.time())
        filename=filedir+'/'+ formatted_date +'.log'

        total = sum(config['quantity'][coin['id']] * coin['current_price'] for coin in getgecko(config)) #Get prices from CoinGecko in ONE API call and add up totals.
        file_append(filename, str(time.time())+','+str("%.2f" % total)) #Log the result
        
        time_period = screen_options[screen]['time_period']
        title = screen_options[screen]['title']
        
        graphwallet_file(filename,title,time_period,epd)
        
        if screen in valid_screens:
            screen = (screen % len(valid_screens)) + 1
        else:
            screen = 1
        
        time.sleep(300) #Sleep as not to overload the Coingeko API
        
    except: #Oh crap!
        time.sleep(30)
        machine.reset()
        