def do_connect():
    
    
    SSID="Gyros"
    SSID_Password="Toenails2Eyeballs!"
    
    #SSID="Gyros2"
    #SSID_Password="Toenails2Eyeballs"
    
    import time
    import network
    import ntptime
    
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, SSID_Password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        time.sleep(1)
    print(wlan.ifconfig())
    
    try:
        ntptime.timeout = 3
        ntptime.settime()
    except OSError:
        print("NTP Error")
        time.sleep(10)
        machine.reset()
        
do_connect()

#Clean up
#del(do_connect)
