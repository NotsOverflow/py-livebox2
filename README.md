py-livebox2
===========

control your livebox 2 with scripts :)

edit login, password and ip of the livebox to meet your specs

  Example:
  
    box = Livebox(login,password,ip).connectAndRenew()
    
  Example2:
  
    while(True):
    	try:
    		Livebox(login,password,ip).testPhone()
    		time.sleep(1)
    	except:
    		time.sleep(3)
    


  you can use:
    checkIp <- to get your ip adress
    
    ipChanged <- to see if your ip has changed
    
    getWifiInfo <- i love this one ^^
    
    getInternetInfo <- to get info about how it is connected
    
    sendAction or sendActionPost <- to make it do things
    
    getPage <- to get a specific page
    
    reNewConnection <- it's in the name
    
    testPhone
    
    restartWifi
    
    restartBox
    
    connectAndRenew
    
