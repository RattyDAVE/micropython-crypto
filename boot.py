def do_connect():
    import network
    import ntptime

    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        ('connecting to network...')
    sta_if.active(True)
    sta_if.connect('SSID', 'password')
    while not sta_if.isconnected():
        pass
    
    print('network config:', sta_if.ifconfig())
    
    #try:
    #    ntptime.settime()
    #except OSError:
    #    print("NTP Error")
        
do_connect()

#Clean up
#del(do_connect)
