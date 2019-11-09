# verify_email_address
A python script for seeing if an email address might work

This is derived from https://github.com/scottbrady91/Python-Email-Verification-Script
and the same warnings apply:

This tests email by trying to send an email and quitting after the server responds to the address given it. This could annoy some servers.
It tries on port 25, not on the submission port, maybe that'll change in the future.

I was using this from a relatively well setup mail server. Using it from, say, a home machine on cable internet might fail for a lot of reasons having to do with looking like a potential spammer.

# The new features:
- Can take a list of email addresses, either from a file, with -l, or from the standard input
- Tries to keep going in the face of strange server responses. I doubt I got them all.
- You specify the "from" address on the commandline with -f. Use a real one, please, unless you enjoy getting blacklisted. You can add a default by editting the file.

# Future ideas
- Catch more server responses
- add a hook for when you get a bad address

# Example uses

`grep whitelist_from .spamassassin/user_prefs | grep -v '*@' | cut -f 2 -d' ' | ./verify_email_address.py > verified_addresses`

Broken down, this says:

1. Find each instance of "whitelist_from" in my spamassassin user_prefs
1. Get rid of the lines about entire servers
1. Get the second field of output (the address, in this case)
1. Hand that to the script
1. Pipe the output to the file "verified_addresses"

Please note that *verified_addresses* is an ideal, not a reality. It possible the server just doesn't want to talk to the script.

----

`./verify_email_address.py -f myrealemail@example.com someaddress@example.com`

Please check *someaddress@example.com* using the from address *myrealemail@example.com*

# The official Usage documentation

```
usage: verify_email_address.py [-h] [-f FROM_ADDRESS] [-l LIST] [address]

positional arguments:
 address               A single address can be checked on the command line

optional arguments:
 -h, --help            show this help message and exit
 -f FROM_ADDRESS, --from FROM_ADDRESS
                       legit email address which will be sent to each server
                       as part of verification process
 -l LIST, --list LIST  List of addresses to check. Too many might get you in
                       trouble
```