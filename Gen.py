import threading
import os
import pyfiglet
from colorama import Fore, Style
import json
from main import Botter
with open('config.json') as fp:
    config = json.load(fp)
def genToken(inv=None):
    while True:
            botter = Botter(inv, config["capKey"],config["kopeechkaKey"])
            botter.generateToken()
os.system('cls')
os.system('title Terminal Token Generator v1 | discord.gg/tokenz')
print(pyfiglet.figlet_format("Terminal Generator"))
print(f'{Style.BRIGHT}~Terminal#1337')
with open("proxies.txt") as fp:
    proxs = fp.read().splitlines()
if len(proxs) == 0:
    print(f'{Fore.RED}{Style.BRIGHT}Please input some proxies {Style.RESET_ALL}')
    input('Press enter to exit: ')
    exit()
threadCount = int(input(f"{Fore.BLUE}{Style.BRIGHT}[+] Enter The Number of Threads: {Style.RESET_ALL}"))
invite = str(input(f"{Fore.BLUE}{Style.BRIGHT}[+] Enter The Server Invite Code: {Style.RESET_ALL}"))
threads = []
for i in range(threadCount):
     t = threading.Thread(target=genToken, args=(invite, ))
     t.start()
     threads.append(t)
for i in range(threadCount):
    threads[i].join()
