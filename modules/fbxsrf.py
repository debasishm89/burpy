from rawweb import *
def main(raw_stream,ssl):
	'''
	This Burpy module is specially written to find CSRF vulnerability in Facebook Application.
	It has already found 1-2 major and few minor CSRF vulnerability in FB application.
	It simply checks whether CSRF token validation is present in server side or not by removing token from request and replaying it.
	Facebook application always shows a generic error message for CSRF error which is "Please try closing and re-opening your browser"
	If this error is not present in response after removing the token it returns +ve.
	'''
	title = [
		 "Possible XSRF",		#Please don't add <script>/ html tags here and report XSS :P
		"CSRF Token Removed from Request and Change Request Method"
		]
	csrf_error = "Please try closing and re-opening your browser"	# 
	raw = RawWeb(raw_stream)
	if "fb_dtsg" in raw_stream:		# Check if request contains any CSRF token or not
		raw.removeparameter("fb_dtsg")	# Use rawweb api to remove the parameter from request
		final = raw.changemethod()	# Chnage the request method from(if GET make it POST)
	else:
		return "FALSE"			#CSRF token not present in request
	result = raw.fire(ssl)
	#result[0] => 200
	#result[1] => OK
	#result[2] => Respheaders => dict
	#result[3] => body
	if csrf_error in result[3]:		# If the CSRF error presnt in response body, Everythng is fine, return false
		# validation there
		# If test positive return True,reponse header , response body
		#return res.status,res.reason,res_headers,self.craft_res(res.getheaders(),res.read())
		return "FALSE"
	else:
		# If false only send False
		return title,final,result[0],result[1],result[2],result[3]	# Else return the crafted request
