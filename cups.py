#!/usr/bin/python3

import nmap
import csv


def WritePrintersList(lport, netcsv):
    for port in lport:
        if port == 631 and nmScan[host][proto][port]['state'] == 'open':
            netcsv.write('\n%s, %s, ipp' % (host, nmScan[host].hostname()))
            return
        if port == 9100 and nmScan[host][proto][port]['state'] == 'open':
            netcsv.write('\n%s, %s, raw' % (host, nmScan[host].hostname()))

nmScan = nmap.PortScanner()
f = open('ip_range.config')
netrange = f.read().splitlines()
print(netrange)
for net in netrange:
        nmScan.scan(net, '631, 9100', '-sS')
        csvname = net.replace('/', '-')
        with open(f'{csvname}.csv', 'w') as testcsv:
            wr = csv.writer(testcsv, quoting=csv.QUOTE_ALL)
            testcsv.write('IP, HostName, ConnectionType')
            for host in nmScan.all_hosts():
                for proto in nmScan[host].all_protocols():
                    lport = nmScan[host][proto].keys()
                    WritePrintersList(lport, testcsv)

f.close()
