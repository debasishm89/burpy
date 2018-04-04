Burpy v0.1
===========

This portable python tool,parses Burp Suite (http://portswigger.net) log and performs 
series of tests and finally generate HTML report.


		debasish@debasish:~/burpy$ python burpy.py 

                         ____                                             ___  __ 
                        |  _ \                                           / _ \/_ |
                        | |_) |_   _ _ __ _ __  _   _   ______  __   __ | | | || |
                        |  _ <| | | | '__| '_ \| | | | |______| \ \ / / | | | || |
                        | |_) | |_| | |  | |_) | |_| |           \ V /  | |_| || |
                        |____/ \__,_|_|  | .__/ \__, |            \_/    \___(_)_|
                                         | |     __/ |                            
                                         |_|    |___/      

                  Burpy v0.1 Portable and Flexible Web Application Security Scanner
                        Author : Debasish Mandal (http://www.debasish.in)
		[+] Error!! You have missed a mandatory option

		Usage: burpy.py [options]
		
		Options:
    		-h, --help         show this help message and exit
    		-t TARGET_DOMAIN   Target/Scan Scope domain - Its mandatory option
    		-l BURP_SUITE_LOG  Full path to burp suite log - Its mandatory option
    		-s SSL             Use of SSL on or off - Its mandatory option
		debasish@debasish:~/burpy$ 



I have included one raw http request manipulation library (rawweb.py) here.
Using this library you can easily manipulate (Add remove headers , parameter ,change methods) raw 
http requests on the fly.

You can easily write your own module specific to any web application. 

One example is given below.

Below mentioned burpy module adds a new header to any request, remove Referrer header and csrf token from 
request and fire the request.If generic CSRF error is returned, it means token validation is present in 
server side. If server respond is a different manner it log this crafted request in html report.

https://github.com/debasishm89/burpy/blob/master/modules/samplexsrf.py


And this is how the final report looks.

		http://onlyhtmlfiles.appspot.com/static/Sample_Burpy_Report.html

I've used twitter Bootstrap library to design this final report.

Following Bugs were found using Burpy:

                         http://www.debasish.in/2013/09/hacking-twitter-for-fun.html
                         http://www.debasish.in/2013/09/twitter-xsrf-vulnerability-thanks-to.html
                         http://www.debasish.in/2013/10/fuzzing-facebook-for-using-burpy.html

Mail me any feature request , Bug @ debasishm89 [@] gmail.com


**Update**
I've been receiving many issues / errors with this prototype of burpy. Right now I'm unable to maintain this project due to other priorities and limited bandwidth. Sorry about that :(
