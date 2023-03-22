#!/usr/bin/python3
from printer import Printer
import os
import nmap
import logging
import csv
def init_logger(name):
    logger = logging.getLogger(name)
    FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
    logger.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter(FORMAT))
    sh.setLevel(logging.DEBUG)
    fh = logging.FileHandler('test.log')
    fh.setFormatter(logging.Formatter(FORMAT))
    fh.setLevel(logging.DEBUG)
    logger.addHandler(sh)
    logger.addHandler(fh)
    logger.debug("logger was initialized")

def AddPrinters(lport, printers):
    for port in lport:
        if port == 631 and nmScan[host][proto][port]['state'] == 'open':
            logger.info(f"Найден IPP принтер {nmScan[host].hostname()}, ip: {host}")
            printers.append(Printer(nmScan[host].hostname(), host, 'ipp'))
            return
        if port == 9100 and nmScan[host][proto][port]['state'] == 'open':
            logger.info(f"Найден RAW принтер {nmScan[host].hostname()}, ip: {host}")
            printers.append(Printer(nmScan[host].hostname(), host, 'raw'))

def WritePrinterList(printers):
    print("Список найденных принтеров: ")
    for printer in printers:
        printer.show()


def Search(printers, ip):
    for printer in printers:
        if printer.ip == ip:
            return printer
    raise ValueError("Принтер не найден")
#def mount_printer(printer):
#    command = f"lpadmin -p ipp_{printer} -E -v ipp://{printer}/ipp/print -m everywhere"

def WritePrintResult(printer):
    print_result = input("Укажите правильно ли напечатан результат('+' - да, '-' - нет')") 
    if print_result == "-":
        comments = input("Оставьте комментарий что напечаталось неправильно: ")
    elif print_result == "+":
        comments = ' '
    else:
        return WritePrintResult
    with open(f'Print_Result.csv', 'w') as resultcsv:
        wr = csv.writer(resultcsv, quoting=csv.QUOTE_ALL)
        resultcsv.write('IP, HostName, ConnectionType, Result, Comments')
        # resultcsv.write('\n%s, %s, ipp' % (host, nmScan[host].hostname()))
        resultcsv.write(f"{printer.ip}, {printer.name}, {printer.protocol}, {print_result}, {comments}")




def portrait_1_side(printer, filename):
    command = f"lp -o media=A4,portrait -d {printer.name} {filename}"
    os.system(command)
    WritePrintResult(printer)
        
def portrait_2_side(printer):
    pass
def landscape_1_side(printer):
    pass
def landscape_2_side(printer):
    pass
def portrait_2_pages(printer):
    pass
def landscape_2_pages(printer):
    pass
def portrait_color(printer):
    pass
def landscape_color(printer):
    pass



TESTPRINTER_PROMPT = "Выберите принтер для тестирования(укажите IP адрес принтера) или введите 'exit' для выхода: "
TESTMENU_PROMPT = """ Меню тестирования принтера 
1) 1-сторонняя печать(книжная)
2) 2-сторонняя печать(книжная)
3) 1-сторонняя печать(альбомная)
4) 2-сторонняя печать(альбомная)
5) Печать 2-х страниц(книжная)
6) Печать 2-х страниц(альбомная)
7) Цветная печать(книжная)
8) Цветная печать(альбомная)
9) Выход(переход к другому принтеру)

Выберите пункт меню: """

TESTMENU_OPTIONS = {
    "1": portrait_1_side,
    "2": portrait_2_side,
    "3": landscape_1_side,
    "4": landscape_2_side,
    "5": portrait_2_pages,
    "6": landscape_2_pages,
    "7": portrait_color,
    "8": landscape_color
}
def TestMenu():
    while True:
        printer_ip = input(TESTPRINTER_PROMPT)
        if printer_ip == "exit":
            break
        else:
            try:        
                printer = Search(printers, printer_ip)
            except Exception:
                logger.error("Принтер не найден, введите правильный IP адрес")
            else:
                printer.mount()
                while True:
                    selection = input(TESTMENU_PROMPT)
                    if selection == "9":
                        break
                    #((selection := input(TESTMENU_PROMPT) != "9"):
                    else:
                        try:
                            TESTMENU_OPTIONS[selection](printer.name,'testprint.txt')
                        except KeyError:
                            logger.error("Введен неправильный номер, попробуйте еще раз")




init_logger("cups")
logger = logging.getLogger("cups.main")

nmScan = nmap.PortScanner()

f = open('ip_range.config')
netrange = f.read().splitlines()

logger.debug(f"Получен список подсетей: {netrange}")
f.close()
printers = []
for net in netrange:
    nmScan.scan(net, '631, 9100', '-sS')
    logger.debug(f"Сканирую подсеть {net}")
    for host in nmScan.all_hosts():
        for proto in nmScan[host].all_protocols():
            lport = nmScan[host][proto].keys()
            AddPrinters(lport, printers)

WritePrinterList(printers)
TestMenu()

