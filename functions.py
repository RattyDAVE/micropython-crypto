def config_save(config, config_file):
    import ujson
    f = open(config_file, 'w')
    f.write(ujson.dumps(config))
    f.close()
    return

def config_load(config_file):
    import ujson
    try:
        f = open(config_file, 'r')
        config = ujson.loads(f.read())
        f.close()
    except OSError:
        config={'currency': 'GBP','headers': {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}}
        config['quantity']={'bitcoin': 0.0,'nexo': 0,'pluton': 0,'quickswap': 0}
        
        config['coinlist']=""
        for i in config['quantity']:
            config['coinlist']+=","+i if config['coinlist'] else ","+i
        
        config['geckourl'] = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=" + config['currency'] + "&ids=" + config['coinlist']

        config_save(config,config_file)
    return config

def getgecko(config):
    from urequests import get
    geckojson = get(config['geckourl'], headers=config['headers']).json()
    return geckojson

#Date and Time
def datetime():
    import umachine
    timestamp=umachine.RTC().datetime()
    return "%04d-%02d-%02d %02d:%02d:%02d"%(timestamp[0:3]+timestamp[4:7])

def date():
    import umachine
    timestamp=umachine.RTC().datetime()
    return "%04d-%02d-%02d"%(timestamp[0:3])

def time():
    import umachine
    timestamp=umachine.RTC().datetime()
    return "%02d:%02d:%02d"%(timestamp[4:7])

def settime():
    import ntptime
    try:
        ntptime.settime()
        return True
    except OSError:
        print("NTP Error")
        return False
    return

#File
def file_search(filename, search_term):
    import ure
    for line in open(filename, 'r').readlines():
        if ure.match(search_term, line):
            return line
    return None
    
def file_append(filename, ap_text):
    with open(filename, 'a') as myfile:
        myfile.write(ap_text)

def file_exist(filename):
    import uos
    try:
        uos.stat(filename)
        #print("DEBUG file_exist - File "+filename+" SUCCESS")
        return True
    except OSError:
        #print("DEBUG file_exist - File "+filename+" NOT FOUND")
        return False

#Graphics
def graphit(data,title,days):
    import framebuf

    height=200
    width=400
    bits=1

    maxvalue=max(data)
    minvalue=min(data)
    
    fbuf=framebuf.FrameBuffer(bytearray(height*width*bits),width,height, framebuf.MONO_HLSB)

    for x in range(len(data)):
        p_h=abs(int((height/(maxvalue-minvalue))*(data[x]-minvalue)))
        p_w=abs(int((width/len(data))*x))
        
        # (height / (maxvalue-minvalue)) * value
        #p_h=int((height/(maxvalue-minvalue))*(data[x]-minvalue))
        #p_h=abs(p_h-height)

        #p_w=int((width/len(data))*x)
        #p_w=abs(p_w)
    
        if not x==0: fbuf.line(p_wFrom,p_hFrom,p_w,p_h,1)
    
        p_hFrom=p_h
        p_wFrom=p_w
    
    #Decorations
    fbuf.hline(0,int((height/2)), width, 1) #Line Halfway
    fbuf.text(str(maxvalue), 0, 0, 1) # Max Value at top left
    fbuf.text(title, int((width/2)-((len(title)*8)/2)), 0, 1) #Title at the top centre
    fbuf.text(str(minvalue), 0, (height-8), 1) # Minvalue at bottom left

    #Day ticks
    for i in range(1,days):
          dayline=int((width/days)*i)
          fbuf.vline(dayline,int((height/2))-5, 10, 1)
    
    #Save as a PBM - P4
    with open(title+'.pbm', 'wb') as f:
        f.write("P4\n"+str(width)+" "+str(height)+"\n")
        f.write(fbuf)
        
    ## WARNING - SAVES ARE TOO LARGE 
    ##Save as a BMP 
    #import ustruct
    # Write the BMP header
    #bmp_file = open(title+'.bmp', 'wb')
    #bmp_file.write(b'BM')
    #bmp_file.write(ustruct.pack('<i', 62 + len(data)))
    #bmp_file.write(b'\x00\x00\x00\x00')
    #bmp_file.write(ustruct.pack('<i', 62))
    #bmp_file.write(ustruct.pack('<i', 40))
    #bmp_file.write(ustruct.pack('<i', height))
    #bmp_file.write(ustruct.pack('<i', width))
    #bmp_file.write(ustruct.pack('<H', 1))
    #bmp_file.write(ustruct.pack('<H', 1))
    #bmp_file.write(b'\x00\x00\x00\x00')
    #bmp_file.write(ustruct.pack('<i', height*width))
    #bmp_file.write(ustruct.pack('<i', 2835))
    #bmp_file.write(ustruct.pack('<i', 2835))
    #bmp_file.write(b'\x00\x00\x00\x00')
    #bmp_file.write(b'\x00\x00\x00\x00')
    #bmp_file.write(b'\x00\x00\x00\x00')
    #bmp_file.write(b'\x00\x00\x00\x00')
    #bmp_file.write(b'\x00\x00\x00\x00')
    #
    ## Write the image data in BMP format
    #for y in range(width):
    #    for x in range(height):
    #        pixel = fbuf.pixel(x, y)
    #        if pixel:
    #            bmp_file.write(b'\xff\xff\xff')
    #        else:
    #            bmp_file.write(b'\x00\x00\x00')
    #bmp_file.close()
    
    #Save as PNG - No zlib.compress or zlib.crc32
    #import uzlib
    #import ustruct
    
    #def write_chunk(f, type, data):
    #    f.write(ustruct.pack('!I', len(data)))
    #    f.write(type)
    #    f.write(data)
    #    crc = uzlib.crc32(type + data)
    #    f.write(ustruct.pack('!I', crc & 0xffffffff))
        
    #with open(title+'.png', 'wb') as f:
    #    f.write(b'\x89PNG\r\n\x1a\n')
    #    ihdr_data = ustruct.pack('!2I5B', width, height, 8, 0, 0, 0, 0)
    #    write_chunk(f, b'IHDR', ihdr_data)
    #    write_chunk(f, b'IDAT', uzlib.compress(data))
    #    write_chunk(f, b'IEND', b'')


    
    return


#Webserver
def startwww():
    from microWebSrv import MicroWebSrv
    global svr
    srv = MicroWebSrv(webPath='www/')
    #srv.Start() 
    srv.Start(threaded=True)
    #to stop srv.Stop()
    



#Database
def db_connect():
    import upymysql
    config=dict()
    config['db_host']="192.168.0.7"
    config['db_user']="root"
    config['db_password']="my-secret-pw"
    config['db_db']="testlog1"   
    
    connection = upymysql.connect(host=config['db_host'],
                                 user=config['db_user'],
                                 password=config['db_password'])
    return


