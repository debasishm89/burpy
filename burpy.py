import core

def initiate(dict_req_resp):
	'''
	Script initiate.Write the initial part of report
	'''
	print '[+] Found '+str(len(dict_req_resp))+" request from Porvided Burp Log..."
	raw_input('[+] Press Enter to start Test___')
	print '[+] Starting Test..'
	report_head = core.part1.replace('{number}',str(len(dict_req_resp))).replace('{target}',core.target_domain)
	report = open('Report.html','w')
	report.write(report_head)
	report.close()
	# Iterate through all req/response
	for item in dict_req_resp:
		if base.gerequestinfo(item,"Host") == core.target_domain:# Check whether request in in test scope
			for testcase in moduledict:#execute all modules test Case
				result = moduledict[testcase](item,core.ssl)
				#if +ve then
				#result[0] => Test Title
				#result[1] => Final Crafted Resposne
				#result[2] => reason
				#result[3] => response code
				#result[4] => dict of response headers
				#result[5] => Response body
				if len(result) > 5:
					# Test case true
					print '[+] Test Result Positive'
					base.write_report(result[0],result[2],result[3],item,result[1],result[4],result[5])
					#def write_report(self,title,res_reason,res_code,base_request,crafted_request,res_head_dict,latest_response):
				else:
					print '[+] Test Result Negative'
		else:
			print '[+] Skipping....Request not associated with ',core.target_domain
	print '[+] Test Completed...Report.html Generated'
	report = open('Report.html','a')# When test done, Close the report.
	report.write(core.part3)
	report.close()

if __name__ == '__main__':
	base = core.Core()
	base.banner()
	base.cmd_option()
	result = base.parse_log(core.burp_suite_log)
	global target
	target = core.target_domain
	moduledict = base.loadallmodules()
	initiate(result)
