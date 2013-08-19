import urllib
import urllib2
from BeautifulSoup import BeautifulSoup
import re
import hashlib
import time



class Livebox:
	def __init__(self, login, password, ip):
		self.login = login
		self.password = password
		self.url = "http://%s" % ip
		self.ip = False
		self.connected = False
		self.user = ""
		self.timeout = 30
		self.values = {}
		
	def checkIp(self):
		t = True
		c = 0
		while t==True:
			try:
				req = urllib2.Request('http://monip.org/')
				response = urllib2.urlopen(req)
				the_page = response.read()
				soup = BeautifulSoup(the_page)
				self.ip = str(soup.findAll('font',{'size':'8'})[0].contents[1])
				#print(self.ip)
				return self
			except:
				if c == self.timeout:
					print("fail to connect")
					return False
				c += 1
				time.sleep(1)
		
	def loadConnectInputs(self):
		#recuperation des valeur d'input sur la page d'acceil de la livebox
		req = urllib2.Request(self.url) #url
		response = urllib2.urlopen(req)
		the_page = response.read() #page de retour brut
		soup = BeautifulSoup(the_page) #on y met de l'ordre
		t = soup('input') #on trie
		self.values = {'page' : t[0]["value"],
				  'authaction' : t[1]["value"],
				  'sessionid' : t[2]["value"] ,
				  'authkey': t[3]["value"],
				  'authmd5passwd': '',
				  'authlogin': login,
				  'authpasswd': ''}
		#print(values['sessionid'])
		#cryptage du mot de passe
		md5Password = hashlib.md5(password).hexdigest()
		step = md5Password + self.values["authkey"]
		authmd5passwd = hashlib.md5(step).hexdigest()
		#mot de passe final
		self.values["authmd5passwd"] = authmd5passwd
		return self
		
	def connectProcess(self):
		url = '%s/index.cgi' % self.url
		user_agent = 'Mozilla/5.0 (compatible; MSIE 6.0; Windows NT)'
		headers = { 'User-Agent' : user_agent }
		data = urllib.urlencode(self.values) # les valeurs des inputs
		req = urllib2.Request(url, data, headers)
		response = urllib2.urlopen(req) #sumbmit
		the_page = response.read() #retour
		soup = BeautifulSoup(the_page)
		if soup.findAll('span', { "class" : "authusername" }): #login reussi
			t = soup.findAll('span', { "class" : "authusername" })[0].string
			self.connected = True
			self.user = t
			print("connected as : %s" % t)
			return self
		else:
			if soup.findAll('td', { "class" : "info_statusnok" }): # erreur de login
				t = soup.findAll('td', { "class" : "info_statusnok" })[0].string
				print(t)
				return False
			else: # erreur autre que loggin
				print("Error type unknow at connectProcess")
				print(soup.pretify())
				return False
				
	def connect(self):
		self.loadConnectInputs()
		self.connectProcess()
		return self
				
	def ipChanged(self):
		if self.ip==False:
			self.checkIp()
			print("ip wasn't checked before")
			print(self.ip)
			return self
		else:
			ip1 = self.ip
			ip2 = self.checkIp()
			if ip1 == ip2: #arf
				print(ip2)
				print("Same ip adress :'(")
				return False
			else: # super!
				print(ip2)
				print("New ip adress!")
				return self
						

	def sendAction(self,page,action):
		if self.connected == False:
			self.connect()
			
		redirect = "%s?page=%s&action=%s&sessionid=%s" % (self.url,page,action,self.values['sessionid'])
		#print(redirect)
		req = urllib2.Request(redirect)
		response = urllib2.urlopen(req)
		the_page = response.read()
		soup = BeautifulSoup(the_page)
		if soup.findAll('td', { "class" : "info_statusnok" }): #page d'erreur en retour 
			print("%s command error at sendAction : " % action)
			t = soup.findAll('td', { "class" : "info_statusnok" })[0].string
			print(t)
			return False
		else:
			if soup.findAll('span', { "class" : "authusername" }): #page normal avec login ( tout va bien aparament )
				t = soup.findAll('span', { "class" : "authusername" })[0].string
				print("%s command went well as %s" % (action,t))
				return self
			else: #page erreur autre que loggin et pas logguer
				print("%s command error type unknow at sendAction" % action)
				print(soup.pretify())
				return False
	def sendActionPost(self,values):
		action = values['action']
		if self.connected == False:
			self.connect()
			
		url = "%s" % (self.url)
		user_agent = 'Mozilla/5.0 (compatible; MSIE 6.0; Windows NT)'
		headers = { 'User-Agent' : user_agent }
		data = urllib.urlencode(values) # les valeurs des inputs
		req = urllib2.Request(url, data, headers)
		response = urllib2.urlopen(req) #sumbmit
		the_page = response.read() #retour
		soup = BeautifulSoup(the_page)

		if soup.findAll('td', { "class" : "info_statusnok" }): #page d'erreur en retour 
			print("%s command error at sendAction : " % action)
			t = soup.findAll('td', { "class" : "info_statusnok" })[0].string
			print(t)
			return False
		else:
			if soup.findAll('span', { "class" : "authusername" }): #page normal avec login ( tout va bien aparament )
				t = soup.findAll('span', { "class" : "authusername" })[0].string
				print("%s command went well as %s" % (action,t))
				return self
			else: #page erreur autre que loggin et pas logguer
				print("%s command error type unknow at sendAction" % action)
				print(soup.pretify())
				return False
		
	def getPage(self,page):
		if self.connected == False:
			self.connect()
			
		redirect = "%s?page=%s&sessionid=%s" % (self.url,page,self.values['sessionid'])
		#print(redirect)
		req = urllib2.Request(redirect)
		response = urllib2.urlopen(req)
		the_page = response.read()
		soup = BeautifulSoup(the_page)
		if soup.findAll('td', { "class" : "info_statusnok" }): #page d'erreur en retour 
			print("getting %s page error:" % page)
			t = soup.findAll('td', { "class" : "info_statusnok" })[0].string
			print(t)
			return False
		else:
			if soup.findAll('span', { "class" : "authusername" }): #page normal avec login ( tout va bien aparament )
				t = soup.findAll('span', { "class" : "authusername" })[0].string
				print("getting %s page went well as %s" % (page,t))
				return soup
			else: #page erreur autre que loggin et pas logguer
				print("getting %s page error type unknow" % page)
				print(soup.pretify())
				return False
				
	def getWifiInfo(self):
		soup = self.getPage(page = "wireless")
		t = soup("input")
		values = { "wifistatus" : t[6]['value'],
					"ssid" : t[7]['value'],
					"broadcast" : t[8]['value'],
					"key" : t[9]['value'],
					"easypairing" : t[10]['value'],
					"wpspairing" : t[11]['value'],
					"wpspincode" : t[12]['value'],
					"macfiltering" : t[13]['value']
					}
		return values
		
	def getInternetInfo(self):
		soup = self.getPage(page = "internet")
		t = soup("input")
		values = { "adsl" : t[5]['value'],
					"fibre" : t[6]['value'],
					"username" : t[7]['value'],
					"pass" : t[8]['value']
					}
		return values
	
	def reNewConnection(self):
		return self.sendAction(page = "internet",action ="reset")
		
	def testPhone(self):
		return self.sendAction(page = "voip",action ="test")
		
	def restartWifi(self):
		return self.sendAction(page = "reboot",action ="wifistart")
	
	def restartBox(self):
		if self.connected == False:
			self.connect()
		values = { 'page' : 'reboot',
					'action' : 'reboot',
					'sessionid': self.values['sessionid']
					}
		return self.sendActionPost(values = values)
		
	def connectAndRenew(self):
		self.checkIp().connect().reNewConnection().ipChanged()
		print(self.ip)
		return self

	
	
				
login = "admin"
password = "admin"
ip = "192.168.1.1"

box = Livebox(login,password,ip).connectAndRenew()
#box.connectAndRenew()
#.restartWifi()




'''
while(True):
	try:
		Livebox(login,password,ip).testPhone()
		time.sleep(1)
	except:
		time.sleep(3)
'''
