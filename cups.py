# !/usr/bin/python3
from Printer import Printer
import sys
import nmap
import logging
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
        if port == 443 and nmScan[host][proto][port]['state'] == 'open':
            logger.info(f"Найден IPP принтер {nmScan[host].hostname()}, ip: {host}")
            printers.append(Printer(nmScan[host].hostname(), host, 'ipp'))
            return
        if port == 5800 and nmScan[host][proto][port]['state'] == 'open':
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

def portrait_1_side(printer):
    pass
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



TESTPRINTER_PROMPT = "Выберите принтер для тестирования(укажите IP адрес принтера): "
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
    printer = Search(printers, input(TESTPRINTER_PROMPT))
    while (selection := input(TESTMENU_PROMPT)) != "9":
        try:
            TESTMENU_OPTIONS[selection](printer)
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
    nmScan.scan(net, '443, 5800', '-sS')
    logger.debug(f"Сканирую подсеть {net}")
    for host in nmScan.all_hosts():
        for proto in nmScan[host].all_protocols():
            lport = nmScan[host][proto].keys()
            AddPrinters(lport, printers)

WritePrinterList(printers)
TestMenu()

