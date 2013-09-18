burpy
=====


This portable python tool performs parse Burp Suite (http://portswigger.net) log and performs series of tests and generate HTML report.

This tool also includes on raw http request manipulation library (rawweb.py). Using this library you can easily manupulate (Add remove headers , parameter , methods)
raw http requests.

Writing Modules for Bury is pretty easy. One example is given below which tries to validate whether server side check of CSRF token is perfect or not.

In many application we see that if we remove CSRF token from request, the servr throws a generic error message.

Suppose you have already verified that when you remove CSRF token from any request, the generic message server thouws is "Not Allowed".

This below module will simply take requst one by one from Burp log, remove CSRF token from it and fire the request.And in response chek whether CSRF error message is present or not.


from rawweb import *
def main(raw_stream,ssl):			#main() subroutine must be present in any module you write. It accepts raw http stream and whether SSL to used or not
	title = [
		 "Possible XSRF",			#Vulnerability title in Report when result +ve
		"CSRF Token Removed from Request and Change Request Method"	#Description Eg. Removed token from request.it you to reproduce this issue from final report
		]
	csrf_error = "Not Allowed"			#Generic CSRF error message.
	raw = RawWeb(raw_stream)			#Raw HTTP request object
	if "xsrf-token" in raw_stream:			# Check if request contains any CSRF token or not
		raw.removeparameter("xsrf-token")	# if yes then wse rawweb api to remove the parameter from request
	else:
		return "FALSE"			#CSRF token not present in request
	result = raw.fire(ssl)			# Fire the request using rawweb API.
	#result[0] => Response Code
	#result[1] => Response Reason
	#result[2] => A dictionary of Respheaders
	#result[3] => Response Body
	if csrf_error in result[3]:		# If the CSRF error text presnt in response body, Everythng is fine, it return false
		return "FALSE"
	else:
		# If CSRF error is not present in response body a possiblity of CSRF token validation is not present @ server side so write this to report
		return title,final,result[0],result[1],result[2],result[3]	# Else return the crafted request

Now add save this file xsrf.py and drop in in module folder. And its ready to go. So when next time you launch burpy it will load this and perform test cases.
