from random import randint
import redis, nmap, time

import socket
socket.setdefaulttimeout(0.5) # 1 sekund

PORTS = [21,22,23,80,443,2222,6379,8080,8888,22222]

def check_private_ip(ip):
    # 10.0.0.0 - 10.255.255.255
    # 172.16.0.0 - 172.31.255.255
    # 192.168.0.0 - 192.168.255.255
    if ip[0] == '10':  # Private
        return True
    elif ip[0] == '127': # Localhost
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


def Scan(ip):
    nm = nmap.PortScanner()
    retur = []
    port = ','.join(map(str,PORTS))  # [1,2,3] -> '1,2,3'
    nm.scan(ip, port, '-sS -Pn')

    for i in PORTS:
        if('open' in nm[ip]['tcp'][i]['state']):
            retur.append(i)
    
    if retur:
        retur.append(nm[ip].hostname())

    return retur




def Main():
    R = redis.Redis('localhost')
    nr_entrys =  R.scard('random:ip')
    tid = time.time()

    print('Number of IPs in database: %i' % nr_entrys)
    print('')
    
    while 1:
        ip = make_ip()
#        ip = '24.67.93.211'

	if R.sadd('random:ip', ip):
            print('[*] Scanning: %s' % ip)
            ports = Scan(ip)

            if ports:
                R.sadd('random:ip:found', ip)  # List of IPs with open ports.
                tid = time.time() - tid
                nr_entrys = R.scard('random:ip') - nr_entrys
                print('[+] Searched %i IPs in %f seconds)' % (nr_entrys, tid))
                print('[+] ') + ip, ports 
                exit()
	else:
	   print('[-] Alredy checked: %s' % ip)


if __name__ == '__main__':
    Main()


#
#   (.|.)  <- Forslag pa logo!
#    ).(      Battre kommer tydligen inte?
#   ( v )
#    \|/
#
# Last line of code
