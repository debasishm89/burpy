from rawweb import *
def main(raw_stream,ssl):
	title = [
		 "Possible Click Jacking",		#Test title for report when test is successfull
		"No XFO in Response Headers"		# Brief description of test how you are manipulating the request(Will help you to repoduce issues)
		]
	raw = RawWeb(raw_stream)
	final = raw.addheaders({'Fun':'Fun'})#okay
	result = raw.fire(ssl)
	#result[0] => 200	=> Integer
	#result[1] => OK	=> String
	#result[2] => Respheaders => dict
	#result[3] => body	=> string
	if 'x-frame-options' in result[2]:
		# If test result -ve return false
		return "FALSE"
		#return res.status,res.reason,res_headers,self.craft_res(res.getheaders(),res.read())
		#return title,final,result[0],result[1],result[2],result[3]
	else:
		# If false only send False
		#return "FALSE"
		return title,final,result[0],result[1],result[2],result[3]
