def wget(url, filename):
    from urequests import get
    with open(filename, 'wb') as f:
        f.write(get(url).content)
    
    
wget("https://raw.githubusercontent.com/jczic/MicroWebSrv/master/microWebTemplate.py", "microWebTemplate.py")
#wget("https://raw.githubusercontent.com/jczic/MicroWebSrv/master/microWebSrv2.png", "microWebSrv2.png")
wget("https://raw.githubusercontent.com/jczic/MicroWebSrv/master/microWebSrv.py", "microWebSrv.py")
wget("https://raw.githubusercontent.com/jczic/MicroWebSrv/master/microWebSocket.py", "microWebSocket.py")
wget("https://raw.githubusercontent.com/jczic/MicroWebSrv/master/main.py", "main.py")

wget("https://raw.githubusercontent.com/jczic/MicroWebSrv/master/www/favicon.ico","www/favicon.ico")
wget("https://raw.githubusercontent.com/jczic/MicroWebSrv/master/www/index.html","www/index.html")
wget("https://raw.githubusercontent.com/jczic/MicroWebSrv/master/www/pdf.png","www/pdf.png")
wget("https://raw.githubusercontent.com/jczic/MicroWebSrv/master/www/style.css","www/style.css")
#wget("https://raw.githubusercontent.com/jczic/MicroWebSrv/master/www/test.pdf","www/test.pdf")
wget("https://raw.githubusercontent.com/jczic/MicroWebSrv/master/www/test.pyhtml","www/test.pyhtml")
wget("https://raw.githubusercontent.com/jczic/MicroWebSrv/master/www/wstest.html","www/wstest.html")
