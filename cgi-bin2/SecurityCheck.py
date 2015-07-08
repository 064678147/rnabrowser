#!/usr/bin/python
import sys
import re

################################################################################
# This module does numerous security checks for CGI parameters. The checks are 
# very basic, but can be applied to any variable. Feel free to improve this 
# script.
#
# Usage:
# use lib qw(.); # If taint check in enabled
# use SecurityCheck; # This script (make sure it has 755 permissions!)
# check($cgiVariable); # Where $cgiVariable is the variable required, OR
# check($cgiVariable) if (defined($cgiVariable); # If problems, or 
# Use for loop with param() to get all parameter names
# 
# Author: Asher Pasha
# Date: August 2013
#
################################################################################

def end(arg):
    ''' This function exits the program '''
    print "Context-Type: text/html\n\n"
    print "There is an error in your input: %s. If your input is valid, please contact Dr. Provart ( nicholas.provart@utoronto.ca ). Thanks.\n" % (arg)
    sys.exit();

def checkXSS(arg):
    ''' Check for cross site scripting '''

    # Check if the variable is defined
    if arg == None:
        return

    match = re.search(r'<script|alert|javascript|</script', arg, re.M|re.I)
    if match:
        end(arg)

def check(arg):
    ''' Do all checks '''

    # Check if the variable is defined	
    if arg == None:
        return

    # check for cross site scripting
    match = re.search(r'<script|alert|javascript|</script', arg, re.M|re.I)
    if match:
        end(arg)

    # Check for SQL Injection exploits
    match = re.search(r'select |insert |drop |update |grant |from |where |having |mysql |users ', arg, re.M|re.I)
    if match:
        end(arg)

    # Check for Union exploits
    match = re.search(r' and | or | union | all | if ', arg, re.M|re.I)
    if match:
        end(arg)

    # Check for Boolean exploits
    match = re.search(r'make_set| substring| ascii| length', arg, re.M|re.I)
    if match:
        end(arg)

    # Check for Out of Band exploits
    match = re.search(r' http| request', arg, re.M|re.I)
    if match:
        end(arg)

    # Check for Time delay exploits
    match = re.search(r'%|sleep', arg, re.M|re.I)
    if match:
        end(arg)

    # Check for stored procedure injection
    match = re.search(r'create |procedure |declare |exec |set ', arg, re.M|re.I)
    if match:
        end(arg)

    # Command injections
    match = re.search(r'ping |cd |ls |cp |mv |rm |chmod |pico |clear |pwd |pine |mutt |mail ', arg, re.M|re.I)
    if match:
        end(arg)

    match = re.search(r'find |tar |kill |uname |wget |curl |ifconfig |sudo |shutdown ', arg, re.M|re.I)
    if match:
        end(arg)

    match = re.search(r'locate |gcc |grep |perl |python |sh |poweroff |echo |cat ', arg, re.M|re.I)
    if match:
        end(arg)


def checkCi(arg):
    ''' Check for command injections '''

    # Check if the variable is defined  
    if arg == None:
        return

    # Command injections
    match = re.search(r'ping |cd |ls |cp |mv |rm |chmod |pico |clear |pwd |pine |mutt |mail ', arg, re.M|re.I)
    if match:
        end(arg)

    match = re.search(r'find |tar |kill |uname |wget |curl |ifconfig |sudo |shutdown ', arg, re.M|re.I)
    if match:
        end(arg)

    match = re.search(r'locate |gcc |grep |perl |python |sh |poweroff |echo |cat ', arg, re.M|re.I)
    if match:
        end(arg)