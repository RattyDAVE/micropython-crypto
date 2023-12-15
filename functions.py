from urequests import get
import umachine
import ujson
import framebuf
import time

def config_save(config, config_file):
    with open(config_file, 'w') as f:
        f.write(ujson.dumps(config))

def config_load(config_file):
    try:
        with open(config_file, 'r') as f:
            config = ujson.loads(f.read())

    except OSError: #Create Defaults and Save Config File if not exist
        config={'currency': 'GBP','headers': {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}}
        config['quantity']={}
        config['quantity']['bitcoin']=1
        config['quantity']['nexo']=0
        config['quantity']['pluton']=0
        config['quantity']['matic-network']=0
        config['quantity']['the-sandbox']=0

        #config['coinlist']=""
        #for i in config['quantity']: config['coinlist']+=","+i if config['coinlist'] else ","+i
        
        #config['geckourl'] = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=" + config['currency'] + "&ids=" + config['coinlist']

        config_save(config,config_file)
    return config

def getgecko(config):
    
    for i in config['quantity']: coinlist+=i if coinlist else ","+i
    full_url="https://api.coingecko.com/api/v3/coins/markets?vs_currency=" + config['currency'] + "&ids=" +coinlist]

    #return get(config['geckourl'], headers=config['headers']).json()
    return get(full_url, headers=config['headers']).json()

def timestamp():
    return "%02d:%02d"%(umachine.RTC().datetime()[4:6])

def pc_diff(old_value, new_value):
    return ((new_value - old_value) / old_value) * 100

def file_append(filename, ap_text):
    with open(filename, 'a') as myfile:
        myfile.write(ap_text+'\n')


def graphwallet_file(filename,title,time_period,epd):
    #import framebuf
    
    epd.imageblack.fill(0xff)
    epd.imagered.fill(0xff)

    height, width=122, 250
 
    p_hFrom = 0
    p_wFrom = 0 

    #Set Max and Min for Scaling
    maxXvalue, maxYvalue = 0, 0
    minXvalue, minYvalue = 0, 0
    first_value = 0
    
    with open(filename,'r') as file:
        for line in file:
            values = line.strip().split(",")
            values[0] = int(values[0])
            values[1] = float(values[1])

            if values[0] > time.time()-time_period:
                if first_value == 0: first_value = values[1]
                if values[0] > maxXvalue: maxXvalue = values[0]
                if minXvalue == 0: minXvalue = values[0]
                if values[0] < minXvalue: maxXvalue = values[0]
                if values[1] > maxYvalue: maxYvalue = values[1]
                if minYvalue == 0: minYvalue = values[1]
                if values[1] < minYvalue: minYvalue = values[1]
    
    #Set Scale ratio
    if maxXvalue == minXvalue: scaleXval = 1
    else: scaleXval=width/(maxXvalue-minXvalue)
        
    if maxYvalue == minYvalue: scaleYval = 1
    else: scaleYval=height/(maxYvalue-minYvalue)

    with open(filename,'r') as file:
        for line in file:
            values = line.strip().split(",")
            values[0] = int(values[0])
            values[1] = float(values[1])
            
            if values[0] > time.time()-time_period:
                # (height / (maxvalue-minvalue)) * value
                p_h=abs(int(scaleYval*(float(values[1])-minYvalue)))
                p_w=abs(int(scaleXval*(float(values[0])-minXvalue)))

                p_h=int(height-p_h) #INVERT the graph!
                epd.imageblack.line(p_wFrom,p_hFrom,p_w,p_h,0x00) #Remember Graph is inverted! 0=top 
                
                p_hFrom=p_h
                p_wFrom=p_w
    
    epd.imageblack.line(p_wFrom,p_hFrom,p_w,p_h,0x00)
    
    #Decorations
    epd.imageblack.hline(0,int((height/2)), width, 0x00) #Line Halfway
    
    days=0
    day_tick = maxXvalue - (maxXvalue % 86400)
    while day_tick > minXvalue:
        day_tick_x =abs(int(scaleXval*(float(day_tick)-minXvalue)))
        epd.imagered.vline( day_tick_x ,int((height/2))-5, 10, 0x00) #Line Halfway
        day_tick -= 86400
        days += 1
    
    hour_tick = maxXvalue - (maxXvalue % 3600)
    while hour_tick > minXvalue:
        hour_tick_x =abs(int(scaleXval*(float(hour_tick)-minXvalue)))
        epd.imagered.vline(hour_tick_x ,int((height/2)), 5, 0x00) #Line Halfway
        hour_tick -= 3600
    
    epd.imageblack.hline(0,0, height, 0x00) #V Axis
    
    k_tick = maxYvalue - (maxYvalue % 1000)
    while k_tick > minYvalue:
        k_tick_y =abs(int(scaleYval*(float(k_tick)-minYvalue)))
        k_tick_y=int(height-k_tick_y) #Invert!
        epd.imagered.hline(0,k_tick_y, 10, 0x00) #Line Halfway
        k_tick -= 1000

    k_tick = maxYvalue - (maxYvalue % 500)
    while k_tick > minYvalue:
        k_tick_y=abs(int(scaleYval*(float(k_tick)-minYvalue)))
        k_tick_y=int(height-k_tick_y) #Invert!
        epd.imagered.hline(0,k_tick_y, 5, 0x00) #Line Halfway
        k_tick -= 500
  
    epd.imageblack.text(f"{maxYvalue:.0f}", 0, 0, 0x00) # Max Value at top left
    epd.imageblack.text(f"{minYvalue:.0f}", 0, (height-8), 0x00) # Minvalue at bottom left
    diff=str(f"{pc_diff(first_value, values[1]):.2f}")+"%"
    epd.imageblack.text(diff, width-(len(str(diff*8))), (height-8), 0x00) # %Diff at bottom right

    if days <= 1: title="1 Day"
    else: title=str(days)+" days"
    #epd.imageblack.text(title, int((width/2)-((len(title)*8)/2)), 0, 0x00) #Title at the top centre
    epd.imageblack.text(title, int((width/2)-((len(title)*8)/2)), 0, 0x00) #Title at the top centre

    time_string=str(timestamp())+"Z"
    epd.imageblack.text(time_string, width-(len(time_string)*8), 0, 0x00)

    epd.display()
    return

def graphwallet_dir(logdir,title,time_period,epd):
    #import framebuf
    
    epd.imageblack.fill(0xff)
    epd.imagered.fill(0xff)

    height, width=122, 250
 
    p_hFrom = 0
    p_wFrom = 0 

    #Set Max and Min for Scaling
    maxXvalue, maxYvalue = 0, 0
    minXvalue, minYvalue = 0, 0
    first_value = 0
    
    file filename = [f for f in os.listdir(logdir) if os.path.isfile(f)]

    for filename in files:
        with open(filename,'r') as file:
            for line in file:
                values = line.strip().split(",")
                values[0] = int(values[0])
                values[1] = float(values[1])

                if values[0] > time.time()-time_period:
                    if first_value == 0: first_value = values[1]
                    if values[0] > maxXvalue: maxXvalue = values[0]
                    if minXvalue == 0: minXvalue = values[0]
                    if values[0] < minXvalue: maxXvalue = values[0]
                    if values[1] > maxYvalue: maxYvalue = values[1]
                    if minYvalue == 0: minYvalue = values[1]
                    if values[1] < minYvalue: minYvalue = values[1]
    
    #Set Scale ratio
    if maxXvalue == minXvalue: scaleXval = 1
    else: scaleXval=width/(maxXvalue-minXvalue)
        
    if maxYvalue == minYvalue: scaleYval = 1
    else: scaleYval=height/(maxYvalue-minYvalue)

    for filename in files:
        with open(filename,'r') as file:
            for line in file:
                values = line.strip().split(",")
                values[0] = int(values[0])
                values[1] = float(values[1])
            
                if values[0] > time.time()-time_period:
                    # (height / (maxvalue-minvalue)) * value
                    p_h=abs(int(scaleYval*(float(values[1])-minYvalue)))
                    p_w=abs(int(scaleXval*(float(values[0])-minXvalue)))

                    p_h=int(height-p_h) #INVERT the graph!
                    epd.imageblack.line(p_wFrom,p_hFrom,p_w,p_h,0x00) #Remember Graph is inverted! 0=top 
                
                    p_hFrom=p_h
                    p_wFrom=p_w
    
    epd.imageblack.line(p_wFrom,p_hFrom,p_w,p_h,0x00)
    
    #Decorations
    epd.imageblack.hline(0,int((height/2)), width, 0x00) #Line Halfway
    
    days=0
    day_tick = maxXvalue - (maxXvalue % 86400)
    while day_tick > minXvalue:
        day_tick_x =abs(int(scaleXval*(float(day_tick)-minXvalue)))
        epd.imagered.vline( day_tick_x ,int((height/2))-5, 10, 0x00) #Line Halfway
        day_tick -= 86400
        days += 1
    
    hour_tick = maxXvalue - (maxXvalue % 3600)
    while hour_tick > minXvalue:
        hour_tick_x =abs(int(scaleXval*(float(hour_tick)-minXvalue)))
        epd.imagered.vline(hour_tick_x ,int((height/2)), 5, 0x00) #Line Halfway
        hour_tick -= 3600
    
    epd.imageblack.hline(0,0, height, 0x00) #V Axis
    
    k_tick = maxYvalue - (maxYvalue % 1000)
    while k_tick > minYvalue:
        k_tick_y =abs(int(scaleYval*(float(k_tick)-minYvalue)))
        k_tick_y=int(height-k_tick_y) #Invert!
        epd.imagered.hline(0,k_tick_y, 10, 0x00) #Line Halfway
        k_tick -= 1000

    k_tick = maxYvalue - (maxYvalue % 500)
    while k_tick > minYvalue:
        k_tick_y=abs(int(scaleYval*(float(k_tick)-minYvalue)))
        k_tick_y=int(height-k_tick_y) #Invert!
        epd.imagered.hline(0,k_tick_y, 5, 0x00) #Line Halfway
        k_tick -= 500
  
    epd.imageblack.text(f"{maxYvalue:.0f}", 0, 0, 0x00) # Max Value at top left
    epd.imageblack.text(f"{minYvalue:.0f}", 0, (height-8), 0x00) # Minvalue at bottom left
    diff=str(f"{pc_diff(first_value, values[1]):.2f}")+"%"
    epd.imageblack.text(diff, width-(len(str(diff*8))), (height-8), 0x00) # %Diff at bottom right

    if days <= 1: title="1 Day"
    else: title=str(days)+" days"
    #epd.imageblack.text(title, int((width/2)-((len(title)*8)/2)), 0, 0x00) #Title at the top centre
    epd.imageblack.text(title, int((width/2)-((len(title)*8)/2)), 0, 0x00) #Title at the top centre

    time_string=str(timestamp())+"Z"
    epd.imageblack.text(time_string, width-(len(time_string)*8), 0, 0x00)

    epd.display()
    return
