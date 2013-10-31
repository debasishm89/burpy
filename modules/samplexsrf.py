from rawweb import *
def main(raw_stream,ssl):				# create a mail subroutine (mandatory)
	title = ["Possible XSRF",		  #Test title for reporting when test is successful
		      "Removed XSRF token from request"]# Brief description of test how you are manipulating the request(Will help you to reproduce issues)
	raw = RawWeb(raw_stream)			# Initiate rawweb library
	raw.addheaders({'Header1':'Value1'})  # Add new headers to that request
	raw.removeheaders(['Referrer'])			  # Remove Referrer header if exist in raw request
	final = raw.removeparameter("auth_token")	# final will hold the final request to be fired.(For reporting)
	result = raw.fire(ssl)				
	#result[0] => 200	=> Integer
	#result[1] => OK	=> String
	#result[2] => Response headers => dictionary
	#result[3] => body	=> string
	if 'csrf error' in result[3]:
		# Generic CSRF error is in response body. Hence return "FALSE"
		return "FALSE"
	else:
		# As the generic csrf error is not present in body, treat this as suspicious and +ve result.
		return title,final,result[0],result[1],result[2],result[3]
