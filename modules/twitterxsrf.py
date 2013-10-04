from rawweb import *
def main(raw_stream,ssl):
	'''
	This Burpy module is specially written to find CSRF vulnerability in Twitter Application.
	It has already found few minor and one major CSRF vulnerability in Twitter.
	It simply checks whether CSRF token validation is present in Server Side or not by removing token from request and replaying it.
	Twitter application always shows a generic error message for CSRF error which is "Your account may not be allowed to perform this action."
	If this error is not present in response after removing the token it returns +ve.
	
	These Twitter Bugs were found using this Burpy Plugin:

	http://www.debasish.in/2013/09/hacking-twitter-for-fun.html
	http://www.debasish.in/2013/09/twitter-xsrf-vulnerability-thanks-to.html
	
	
	'''
	title = [
		 "Possible XSRF",		#Please don't add <script>/ html tags here and report XSS :P
		"CSRF Token Removed from Request"
		]
	csrf_error = "Your account may not be allowed to perform this action."	# 
	raw = RawWeb(raw_stream)
	if "authenticity_token" in raw_stream:		# Check if request contains any CSRF token or not
		raw.removeparameter("authenticity_token")	# Use rawweb api to remove the parameter from request
	else:
		return "FALSE"			#CSRF token not present in request
	result = raw.fire(ssl)
	if csrf_error in result[3]:		# If the CSRF error presnt in response body, Everythng is fine, return false
		# validation there
		return "FALSE"
	else:
		# If false only send False
		return title,final,result[0],result[1],result[2],result[3]	# Else return the crafted request
