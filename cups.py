#!/usr/bin/python3

import nmap
import csv
import logging
class Printer():
    def __init__(self, name, ip, protocol):
        self.name = name
        self.ip = ip
        self.protocol = protocol

    def test_1_side_book():
        pass

    def test_2_side_book():
        pass
    
    def test_1_side_albom():
        pass

    def test_2_side_albom():
        pass

    def test_2_pages_book():
        pass

    def test_2_pages_albom():
        pass

    def test_color_book():
        pass

    def test_color_albom():
        pass

    def show():
        print(f"{self.ip} | {name} | {protocol}")


def AddPrinters(lport):
    printers = []
    for port in lport:
        if port == 631 and nmScan[host][proto][port]['state'] == 'open':
            printers.append = Printer(nmScan[host].hostname(), host, 'ipp' )
            # netcsv.write('\n%s, %s, ipp' % (host, nmScan[host].hostname()))
            return
        if port == 9100 and nmScan[host][proto][port]['state'] == 'open':
            # netcsv.write('\n%s, %s, raw' % (host, nmScan[host].hostname()))
            printers.append = Printer(nmScan[host].hostname(), host, 'raw' )
    return printers

def WritePrinterList(printers):
    # print("IP  | ")
    for printer in printers:
        printer.show()

nmScan = nmap.PortScanner()

f = open('ip_range.config')
netrange = f.read().splitlines()
print(netrange)
for net in netrange:
        nmScan.scan(net, '631, 9100', '-sS')
        csvname = net.replace('/', '-')
        # with open(f'{csvname}.csv', 'w') as testcsv:
        #     wr = csv.writer(testcsv, quoting=csv.QUOTE_ALL)
        #     testcsv.write('IP, HostName, ConnectionType')
        for host in nmScan.all_hosts():
                for proto in nmScan[host].all_protocols():
                    lport = nmScan[host][proto].keys()
                    AddPrinters(lport)

f.close()
