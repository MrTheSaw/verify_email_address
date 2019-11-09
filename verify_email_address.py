#!/usr/bin/env python3

import re
import smtplib
import dns.resolver
import argparse
import sys

parser = argparse.ArgumentParser()

parser.add_argument('-f', '--from', dest='from_address', required=True,
					help='legit email address which will be sent to each server as part of verification process')
parser.add_argument('-l', '--list', type=argparse.FileType('r'), default=sys.stdin,
					help='List of addresses to check. Too many might get you in trouble')
parser.add_argument('address', type=str, nargs='?', default="",
					help='A single address can be checked on the command line')

args = parser.parse_args()

# Address used for SMTP MAIL FROM command
fromAddress = args.from_address


# Simple Regex for syntax checking
# Shorter regex is from emailregex.com
#regex = '^[_a-zA-Z0-9-]+(\.[_a-zA-Z0-9-]+)*@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*(\.[a-zA-Z]{2,})$'
regex= r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

if not re.match(regex, fromAddress):
	print(f"From address {fromAddress} is malformed")
	exit(-2)

addresses = []
if args.address != "":
	addresses.append(args.address)
else:
	addresses = args.list.readlines()

# SMTP lib setup (use debug level for full output)
server = smtplib.SMTP()
server.set_debuglevel(0)

for addressToVerify in addresses:
	addressToVerify = addressToVerify.rstrip("\r\n")

	username, domain = addressToVerify.split('@')

	print('User:', username, 'Domain:', domain, end=' ')

	# Syntax check
	match = re.match(regex, addressToVerify)
	if match == None:
		print(f" ### Address {addressToVerify} is malformed")
		continue

	# MX record lookup
	try:
		records = dns.resolver.query(domain, 'MX')
	except dns.resolver.NoAnswer:
		print("Bad DNS Response")
		continue
	except dns.resolver.NXDOMAIN:
		print("DNS Server says No such domain")
		continue

	mxRecord = records[0].exchange
	mxRecord = str(mxRecord)

	# SMTP Conversation
	try:
		server.connect(mxRecord)
	except TimeoutError:
		print(f"SMTP Server {mxRecord} TimeOut")
		continue

	except ConnectionRefusedError:
		print(f"SMTP Connection Refused by {mxRecord}")
		continue

	server.helo(server.local_hostname) ### server.local_hostname(Get local server hostname)
	server.mail(fromAddress)
	code, message = server.rcpt(str(addressToVerify))
	server.quit()

	#print(code)
	#print(message)

	# Assume SMTP response 250 is success
	if code == 250:
		print('Success')
	else:
		print('Bad')