def wget(url, filename):
    from urequests import get
    r = get(url)
    print(r.content)
    with open(filename, 'wb') as f:
        f.write(r.content)
 
import os


# Install Webserver
if not 'www' in os.listdir(): os.mkdir("/www")
wget("https://raw.githubusercontent.com/jczic/MicroWebSrv/master/microWebTemplate.py", "microWebTemplate.py")
wget("https://raw.githubusercontent.com/jczic/MicroWebSrv/master/microWebSrv.py", "microWebSrv.py")
wget("https://raw.githubusercontent.com/jczic/MicroWebSrv/master/www/index.html","www/index.html")
wget("https://raw.githubusercontent.com/jczic/MicroWebSrv/master/www/test.pyhtml","www/test.pyhtml")

