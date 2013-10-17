import httplib
import re
import StringIO
import gzip

class RawWeb:
	def __init__(self,raw):
		try:
			raw = raw.decode('utf8')
		except Exception,e:
			raw = raw
		global headers,method,body,path
		headers = {}
		sp = raw.split('\n\n',1)
		if len(sp) > 1:
			head = sp[0]
			body = sp[1]
		else :
			head = sp[0]
			body = ""
		c1 = head.split('\n',head.count('\n'))
		method = c1[0].split(' ',2)[0]
		path = c1[0].split(' ',2)[1]
		for i in range(1, head.count('\n')+1):
			slice1 = c1[i].split(': ',1)
			if slice1[0] != "":
				headers[slice1[0]] = slice1[1]
	def rebuild(self,method,path,code,headers,body):
		raw_stream = method+" "+path+" "+code+"\n"
		# start adding header
		for key in headers:
			raw_stream += key + ": "+headers[key]+"\n"
		raw_stream += "\n"+body
		return raw_stream
	def addheaders(self,new_header):
		#add header
		for key in new_header:
			headers[key] = new_header[key]
		return self.rebuild(method,path,"HTTP/1.1",headers,body)
	def removeheaders(self,rem_headers):
		#remove headers
		for i in range(0,len(rem_headers)):
			if rem_headers[i] in headers:
				del headers[rem_headers[i]]
		return self.rebuild(method,path,"HTTP/1.1",headers,body)
	def addparameters(self,new_params):
		#add params
		new_body = body[:-1]
		for key in new_params:
                        new_body += "&" + key + "=" + new_params[key]
		return self.rebuild(method,path,"HTTP/1.1",headers,new_body)
	def removeparameter(self,del_param):
		rx = '(^|&)' + del_param + '=[^&]*'
		new_body = re.sub(rx, '', body)
		global body
		body = new_body
		return self.rebuild(method,path,"HTTP/1.1",headers,new_body)
	def changemethod(self):
		#url = ""
		url = path
		if method == "POST":
			#method = "GET"
			if "Content-Type" in headers:
				del headers['Content-Type']
			if "=" in url:
				url += "&"
			else:
				url += "?"
			url += body[:-1]
			global path,method,body
			body = ""
			method = "GET"
			path = url
			return self.rebuild("GET",url,"HTTP/1.1",headers,body)
		else:
			headers ['Content-Type'] = 'application/x-www-form-urlencoded'
			a = url.split('?',1)
			url = a[0]
			global path,method,body
			method = "POST"
			path = url
			body = a[1]
			return self.rebuild("POST",url,"HTTP/1.1",headers,body)
	def craft_res(self,res_head,res_body):
		'''
		if response data is gzip encoded this function detectes that and decode that compressed data
		'''
		for i in range(0,len(res_head)):
			e1 =  res_head[i]
			if e1[1] == "gzip":
				res_body = self.decode_gzip(res_body)
		return res_body	# Return the respionse body
	def decode_gzip(self,compresseddata):
		'''
		Accepts gzip compressde data and returns clear text data.
		'''
		compressedstream = StringIO.StringIO(compresseddata)
		gzipper = gzip.GzipFile(fileobj = compressedstream)
		return gzipper.read()
	def fire(self,ssl):
		if len(path) > 70:
			print '[+]',method,path[:100]+"..."
		else:
			print '[+]',method,path
		if ssl == "on":
			con = httplib.HTTPSConnection(headers['Host'])
		else:
			con = httplib.HTTPConnection(headers['Host'])
		try:
			con.request(method,path,body,headers)
			res = con.getresponse()
		except Exception,e:
			return 'Error','Error',{},'Error'
			print '[+] Connectivity Issue '
		#make response dict
		res_headers = {}
		for i in range(0,len(res.getheaders())):
			res_headers[res.getheaders()[i][0]] = res.getheaders()[i][1]
		return res.status,res.reason,res_headers,self.craft_res(res.getheaders(),res.read())
