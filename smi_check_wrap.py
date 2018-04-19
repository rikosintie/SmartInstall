'''
References:
https://www.kaspersky.com/blog/cisco-apocalypse/21966/
https://github.com/Cisco-Talos/smi_check
https://embedi.com/blog/cisco-smart-install-remote-code-execution/

Script Function
Import a list of IP addresses, pass them to Cisco's smi_check.py

Change Log
April 14, 2018
Added code to remove duplicate IP addresses from iplist.txt
Added code to sort the IP addresses and save to iplist.txt
From a CAT core switch
sh cdp ne det | i IP_
Note the under score character. It means find IP plus a space. this
removes IPV6 addresses and firmware versions that include IPservices etc.
Save to iplist.txt

'''
import sys
import os
import struct
from socket import inet_aton
vernum = '1.2'


def version():

    """
    This function prints the version of this program.
    It doesn't allow any argument.
    """
    print("+----------------------------------------------------------------------+")
    print("| "+ sys.argv[0] + " Version "+ vernum +"                                               |")
    print("| This program is free software; you can redistribute it and/or modify |")
    print("| it in any way you want. If you improve it please send me a copy at   |")
    print("| the email address below.                                             |")
    print("|                                                                      |")
    print("| Author: Michael Hubbard, michael.hubbard999@gmail.com                |")
    print("|         mwhubbard.blogspot.com                                       |")
    print("|         @rikosintie                                                  |")
    print("+----------------------------------------------------------------------+")


version()


def Remove(duplicate):
    final_list = []
    for num in duplicate:
        if num not in final_list:
            final_list.append(num)
    return final_list


# create a blank list to accept each line in the file
data = []

mydatafile = 'iplist.txt'
try:
    f = open(mydatafile, 'r')
except FileNotFoundError:    
            print(mydatafile, ' does not exist')
else:

    '''
    format of file
    10.56.254.2
    10.56.254.3
    '''

    for line in f:
            line = line.strip('\n')
            line = line.strip(' ')
            line = line.strip("IP address: ")
            data.append(line)
    f.close

duplicate = data
data = Remove(duplicate)
data = sorted(data, key=lambda ip: struct.unpack("!L", inet_aton(ip))[0])

# write ip addresses to iplist.txt
with open(mydatafile, 'w') as myfile:
    myfile.write('\n'.join(data))

# run smi_check.py for each ip address
for ip in data:
    i = "-i " + ip
    vuln = "./smi_check.py " + i
    os.system(vuln)
