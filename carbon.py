import asyncio
import os
import platform
from datetime import datetime
from threading import Thread
from time import sleep, time

import aiohttp
import msmcauth
import requests
from colored import fore

async def sendNCRequest(session, accNumber, headers):
    sends[accNumber].append(time())
    async with session.put(f"/minecraft/profile/name/{target}", headers=headers) as req:
        status[accNumber].append(req.status)
        recvs[accNumber].append(time())

async def sendGCRequest(session, accNumber, headers, data):
    sends[accNumber].append(time())
    async with session.post(f"/minecraft/profile", headers=headers, json=data) as req:
        status[accNumber].append(req.status)
        recvs[accNumber].append(time())

async def giftcardSniper(token, accNumber):
    tasks = []
    try:
        sleep(droptime - time() - 5 - (offset/1000))
    except:
        pass

    headers = {
        "Authorization": f"Bearer {token}",
        "Referer": "https://www.minecraft.net/",
        "Content-Type": "application/json",
        "Content-Length": f"{len(target)}"
    }

    data = {
        "profileName": str(target),
    }

    async with aiohttp.ClientSession("https://api.minecraftservices.com") as session:
        
        for x in range(6):
            tasks.append(asyncio.ensure_future(sendGCRequest(session, accNumber, headers, data)))
        await asyncio.gather(*tasks)
        await session.close()

async def namechangeSniper(token, accountAuthMethod, accNumber):
    tasks = []
    try:
        sleep(droptime - time() - 5 - (offset/1000))
    except:
        pass

    headers = {
        "Authorization": f"Bearer {token}",
        "Referer": "https://www.minecraft.net/",
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession("https://api.minecraftservices.com") as session:
        while True:
            if float(int(droptime) - (offset / 1000)) < time():
                break
        for x in range(2):
            task = asyncio.ensure_future(sendNCRequest(session, accNumber, headers))
            tasks.append(task)
        await asyncio.gather(*tasks)
        await session.close()

def cinput(text):

    var = input(f'{fore.WHITE}[{fore.LIGHT_RED}Carbon{fore.WHITE}] {text}\nroot{fore.LIGHT_RED}@{fore.WHITE}carbon-sniper:~# {fore.LIGHT_RED}')
    print(fore.WHITE)

    return var

def cprint(text, end='\n'):

    print(f'{fore.WHITE}[{fore.LIGHT_RED}Carbon{fore.WHITE}] {text}', end=end)

def sleepUI(droptime):
    while droptime - (offset / 1000) - 1 > time():
        timer = datetime.utcfromtimestamp(droptime - (offset / 1000) - time()).strftime('%H:%M:%S')
        sleep(0.1)
        cprint(f"Sniping {target} in {timer}         ", end='\r')
    cprint(f"Preparing to snipe {target}        ", end='\r')

def getDroptime(target):

    if target == 'test':
        return time() + 10

    headers = {
        'user-agent': 'Sniper'
    }

    try:
        try:
            req = requests.get(f'http://api.star.shopping/droptime/{target}', headers=headers)
            droptime = req.json()['unix']
        except:
            req = requests.get(f'https://droptime.site/api/v2/name/{target}')
            droptime = req.json()['droptime']
            if droptime == 0:
                raise Exception
    except:
        while True:
            try:
                dtTimestamp = cinput('Couldnt find droptime in droptime APIs. Paste in UNIX or NameMC timestamp (month/day/year format).')
                if len(dtTimestamp) == 14 or 10:
                    droptime = int(dtTimestamp)
                    break
                dtTimestamp = datetime.strptime(dtTimestamp, "%m/%d/%Y • %I:%M:%S %p")
                droptime = int(datetime.timestamp(dtTimestamp))
                break
            except:
                cprint('Invalid Format.')
    
    return droptime

def threadAsync(accountType, token, accNumber):
    if accountType == 1:
        asyncio.run(giftcardSniper(token, accNumber))
    else:
        if accountType == 2:
            accountAuthMethod = 'ms'
        elif accountType == 3:
            accountAuthMethod = 'mojang'
        asyncio.run(namechangeSniper(token, accountAuthMethod, accNumber))

def establishThreads():
    global threads

    accTypes = []
    accounts = open("accounts.txt", "r").read().splitlines()

    for i in range(len(accounts)):
        sends.append([])
        recvs.append([])
        status.append([])
        if accounts[i].split(':')[2] == 'gc':
            accTypes.append(1)
        elif accounts[i].split(':')[2] == 'ms':
            accTypes.append(2)
        else:
            accTypes.append(3)

    threads = []

    for i in range(len(accounts)):
        threads.append(Thread(target=threadAsync, args=(accTypes[i], accounts[i].split(':')[1], i)))
        threads[i].start()

def main():

    global target, offset, sends, recvs, status, droptime

    sends = []
    recvs = []
    status = []

    if platform.system() == 'Windows':
        os.system('cls')
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    else:
        os.system('clear')

    banner = f'''{fore.WHITE}
            ╔═════════════════════════════════╗
            ║ ╔═════════════════════════════╗ ║
            ║ ║ {fore.LIGHT_RED}6                     12.01{fore.WHITE} ║ ║
            ║ ║ {fore.LIGHT_RED}                           {fore.WHITE} ║ ║
            ║ ║ {fore.LIGHT_RED}         .ooooooo.         {fore.WHITE} ║ ║
            ║ ║ {fore.LIGHT_RED}        d8P'   `Y8b        {fore.WHITE} ║ ║
            ║ ║ {fore.LIGHT_RED}       888                 {fore.WHITE} ║ ║
            ║ ║ {fore.LIGHT_RED}       888                 {fore.WHITE} ║ ║
            ║ ║ {fore.LIGHT_RED}       888                 {fore.WHITE} ║ ║
            ║ ║ {fore.LIGHT_RED}       `88b     ooo        {fore.WHITE} ║ ║
            ║ ║ {fore.LIGHT_RED}        `Y8boood8P'        {fore.WHITE} ║ ║
            ║ ║ {fore.LIGHT_RED}                           {fore.WHITE} ║ ║
            ║ ║ {fore.LIGHT_RED}          Carbon           {fore.WHITE} ║ ║
            ║ ╚═════════════════════════════╝ ║
            ╚═════════════════════════════════╝
    '''

    creditString = f'Developed by {fore.LIGHT_RED}limbo#1112{fore.WHITE}'
    displayArray = []

    print(banner)

    for i in creditString:
        print(f'                 {"".join(displayArray)}{fore.WHITE}|', end='\r')
        displayArray.append(i)
        sleep(0.03)
    print(f'                 {"".join(displayArray)}              \n')

    target = str(cinput('Please enter the name you would like to snipe.'))
    droptime = int(getDroptime(target))
    offset = float(cinput('Please enter the offset you would like to use.'))

    cprint('Establishing sniper threads...', end='\r')

    establishThreads()
    Thread(target=sleepUI, args=(droptime,)).start()

    sleep(droptime - time() - 0.25)

    for i in threads:
        i.join()

    for i in range(len(sends)):
        cprint(f'Account {i+1}:                           ')
        for x in range(len(sends[i])):
            cprint(f'Sent @ {sends[i][x]} | {status[i][x]} @ {recvs[i][x]}')
            sleep(0.05)
        print()

main()