from random import randint
import urllib2

import socket
socket.setdefaulttimeout(0.5) # 1 sekund

def check_private_ip(ip):
    # 10.0.0.0 - 10.255.255.255
    # 172.16.0.0 - 172.31.255.255
    # 192.168.0.0 - 192.168.255.255
    if ip[0] == '10':  # Private
        return True
    elif ip[0] == '172' and (int(ip[1]) >= 16 and int(ip[1]) <=31):  # Private
        return True
    elif ip[0] == '192' and ip[1] == '168':  # Private
        return True
    elif ip[0] == '169' and ip[1] == '254':  # Microsoft no DHCP
        return True
    elif int(ip[0]) >= 224 and int(ip[0] <= 239):   # Multicast
        return True
    elif ip[0] == '255' and ip[1] == '255' and ip[2] == '255' and ip[3] == '255':  # Broadcast
        return True

    return False

def make_ip():
    while 1:
        ip = []
        for x in range(0,4):
            ip.append(str(randint(1,255)))
        
        if not check_private_ip(ip):
            return(".".join(ip))


def get_webserver(ip):
    print '[*] Looking for HTTP server: '+ip
    try:
        response = urllib2.urlopen('http://'+ip)
        print "This gets the code: ", response.code
        print "The Server is: ", response.info()['server']
        return True
    except urllib2.URLError, e:
        return False
    

def Main():
    while 1:
        ip = make_ip()
#        ip = '24.67.93.211'
        if get_webserver(ip):
            exit()



if __name__ == '__main__':
    Main()


#  
#
#
#

