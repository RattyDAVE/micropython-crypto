from functions import *
import time
import machine
import os

from EPD_2in13_B_V4_Landscape import EPD_2in13_B_V4_Landscape
epd=EPD_2in13_B_V4_Landscape()

config_file="config.json"
config=dict()
config=config_load(config_file)
screen=1
filedir='logs'

#Create dir if not exist
if not filedir in os.listdir(): os.mkdir(filedir)

screen_options = {
    1: {'time_period': 86400, 'title': 'Last 24h'},
    2: {'time_period': 86400 * 7, 'title': 'Last 7 Days'},
    3: {'time_period': 86400 * 360, 'title': 'Max Days'}
}

valid_screens = [1, 2, 3]

# Main Loop
while True: # Main Loop
    try:
        now=time.localtime()
        formatted_date = str(now[0])+str(now[1])+str(now[2])
        filename=filedir+'/'+ formatted_date +'.log'
        total = sum(config['quantity'][coin['id']] * coin['current_price'] for coin in getgecko(config)) #Get prices from CoinGecko in ONE API call and add up totals.
        print(filename,total)
        
        file_append(filename, str(time.time())+','+str("%.2f" % total)) #Log the result
        
        time_period = screen_options[screen]['time_period']
        title = screen_options[screen]['title']
        
        #graphwallet_file(filename,title,time_period,epd)
        graphwallet_dir(filedir,title,time_period,epd)
        
        if screen in valid_screens:
            screen = (screen % len(valid_screens)) + 1
        else:
            screen = 1
        
        time.sleep(60 * 2) #Sleep as not to overload the Coingeko API
        
    except: #Oh crap!
        print("Crash!")
        time.sleep(10)
        machine.reset()
        