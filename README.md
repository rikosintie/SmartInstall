# SmartInstall
A wrapper for Cisco's smi_check.py file.

**Requirements**
1. Python 3.x
2. Python 2.7

The Cisco script is written in Python 2.7.

The guys at [embedi.com](embedi.com) released a remote code exploit for Cisco's Smart Install protocol at GeekPWN 2017 Hong Kong. The Smart install protocol is used for automatic switch deployment and is enabled by default on many models including the 3850, 2960x, and 4500x. 

This is a widespread vulnerability and it can lead to a DoS or a complete takeover of the switch. In this YouTube video Embedi [CVE-2018-0171 CISCO full control](https://www.youtube.com/watch?time_continue=6&v=CE7KNK6UJuk) demostrates gaining full control of the switch. In the reference section below I have a link to a Kapersky article on the vulnerability. They say that [Shodan.io](https://www.shodan.io/) lists 168,000 devices exposed on the public Internet. I have already been contacted by a customer that was notified they had one in the list. 

Keep in mind that being exposed to the Internet means you can be attacked from anywhere where in the world, but just because you don't have a switch in front of the firewall doesn't mean you shouldn't be concerned. Embedi released the PoC code that causes the switch to reload so if you aren't using ACLs on your management interfaecs any script kiddie can attack from the inside. 

I recommend using ACLs to limit access to the management interface to just your management network. This is a cisco best practice. Here is an example where the management stations are on 10.1.18.0 and 10.1.50.0 and the switch is 10.10.10.1.  
```
ip access-list extended Management
permit tcp host 10.10.10.1 host 10.1.18.0 0.0.0.255 eq 22
permit tcp host 10.10.10.1 host 10.1.50.0 0.0.0.255 eq 443
deny ip any any

line vty 0 15
access-class Management in
```
**Locating vulnerable switches**

Cisco released a python 2.7 script to check for the vulerability - [Smart Install Client Scanner](https://github.com/Cisco-Talos/smi_check). You run the script with an IP address and it tells you if smart install is running and accessable. It works great but isn't very scalable, so I wrote a wrapper that takes a text file of IP addresses and checks all of them. Much more efficient if you have a lot switches to check.

**Usage**

On a catalyst core switch run ```show cdp ne det | i IP_``` 
Be sure to include the underscore character. It tells the seach to look for IP and a space. This eliminates IPv6 addresses and the output from switches that have IPservices in their name.

You get an output something like this:
```
sh cdp ne det | i IP_
  IP address: 10.217.1.60
  IP address: 10.217.1.60
  IP address: 10.217.1.30
  IP address: 10.217.1.30
  IP address: 10.217.1.10
  IP address: 10.217.1.10
  IP address: 10.217.1.40
  IP address: 10.217.1.40
  IP address: 10.217.1.20
  IP address: 10.217.1.20
  IP address: 10.217.1.50
  IP address: 10.217.1.50
  IP address: 10.217.1.9
  IP address: 10.217.1.9
```  
Save it to a text file named iplist.txt and run the wrapper script ```python3 smi_check_wrap.py```. 

In this case I found that all the switches were vulnerable. 
```
+----------------------------------------------------------------------+
| smi_check_wrap.py Version 1.1                                               |
| This program is free software; you can redistribute it and/or modify |
| it in any way you want. If you improve it please send me a copy at   |
| the email address below.                                             |
|                                                                      |
| Author: Michael Hubbard, michael.hubbard999@gmail.com                |
|         mwhubbard.blogspot.com                                       |
|         @rikosintie                                                  |
+----------------------------------------------------------------------+
[INFO] Sending TCP probe to 10.217.1.9:4786
[INFO] Smart Install Client feature active on 10.217.1.9:4786
[INFO] 10.217.1.9 is affected
[INFO] Sending TCP probe to 10.217.1.10:4786
[INFO] Smart Install Client feature active on 10.217.1.10:4786
[INFO] 10.217.1.10 is affected
[INFO] Sending TCP probe to 10.217.1.20:4786
[INFO] Smart Install Client feature active on 10.217.1.20:4786
[INFO] 10.217.1.20 is affected
[INFO] Sending TCP probe to 10.217.1.30:4786
[INFO] Smart Install Client feature active on 10.217.1.30:4786
[INFO] 10.217.1.30 is affected
[INFO] Sending TCP probe to 10.217.1.40:4786
[INFO] Smart Install Client feature active on 10.217.1.40:4786
[INFO] 10.217.1.40 is affected
[INFO] Sending TCP probe to 10.217.1.50:4786
[INFO] Smart Install Client feature active on 10.217.1.50:4786
[INFO] 10.217.1.50 is affected
[INFO] Sending TCP probe to 10.217.1.60:4786
[INFO] Smart Install Client feature active on 10.217.1.60:4786
[INFO] 10.217.1.60 is affected
```
Run ```show vstack config``` to view the current status. Here is an example of a switch with smart install enabled.
```
sh vstack conf
 Role: Client (SmartInstall enabled)
 Vstack Director IP address: 0.0.0.0

 *** Following configurations will be effective only on director ***
 Vstack default management vlan: 1
 Vstack start-up management vlan: 1
 Vstack management Vlans: none
 Join Window Details:
	 Window: Open (default)
	 Operation Mode: auto (default)
 Vstack Backup Details:
	 Mode: On (default)
	 Repository: 
```
To disable smart install run ```no vstack``` from global configuration.

**Known Affected switches**
```
Catalyst 4500 Supervisor Engines
Catalyst 3850 Series
Catalyst 3750 Series
Catalyst 3650 Series
Catalyst 3560 Series
Catalyst 2960 Series
Catalyst 2975 Series
IE 2000
IE 3000
IE 3010
IE 4000
IE 4010
IE 5000
SM-ES2 SKUs
SM-ES3 SKUs
NME-16ES-1G-P
SM-X-ES3 SKUs
```

**References**

1. [Cisco Smart Install Remote Code Execution](https://embedi.com/blog/cisco-smart-install-remote-code-execution/)
2. [Cisco Smart Install Security](https://www.cisco.com/c/en/us/td/docs/switches/lan/smart_install/configuration/guide/smart_install/concepts.html#23355)
3. [What happened to the Internet: attack on Cisco switches](https://www.kaspersky.com/blog/cisco-apocalypse/21966/)
