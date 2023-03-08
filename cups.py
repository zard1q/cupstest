#!/usr/bin/python3

import nmap
import csv


def WritePrintersList(lport):
    for port in lport:
        # print('port : %s\tstate : %s' % (port, nmScan[host][proto][port]['state']))
        if port == 631 and nmScan[host][proto][port]['state'] == 'open':
            testcsv.write('\n%s, %s, ipp' % (host, nmScan[host].hostname()))
            return
        if port == 80 and nmScan[host][proto][port]['state'] == 'open':
            testcsv.write('\n%s, %s, raw' % (host, nmScan[host].hostname()))


# initialize the port scanner
nmScan = nmap.PortScanner()

netrange1 = open('ip_range.config').readlines()

# with open('ip_range.config', 'r') as netrange:
for net in netrange1:
        nmScan.scan(net, '631, 9100', '-sS')
        print(net)
        with open('test.csv', 'w') as testcsv:
            wr = csv.writer(testcsv, quoting=csv.QUOTE_ALL)
            testcsv.write('IP, HostName, ConnectionType')
            for host in nmScan.all_hosts():
                # print('Host : %s (%s)' % (host, nmScan[host].hostname()))
                # print('State : %s' % nmScan[host].state())
                for proto in nmScan[host].all_protocols():
                    # print('----------')
                    # print('Protocol : %s' % proto)

                    lport = nmScan[host][proto].keys()
                    # lport.sort()
                    WritePrintersList(lport)

netrange1.close()

