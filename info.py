import os
import sys
import time
import random
import string
from urllib.request import urlopen

# ANSI Color Codes
R = '\033[91m' # Red
G = '\033[92m' # Green
Y = '\033[93m' # Yellow
B = '\033[94m' # Blue
C = '\033[96m' # Cyan
W = '\033[97m' # White
BOLD = '\033[1m'
RESET = '\033[0m'

def clear():
    os.system('clear')

def banner():
    clear()
    print(f"{C}{BOLD}")
    print(" __  __ _   _ _  _____ ___ _____ ___   ___  _     ")
    print("|  \/  | | | | ||_   _|_ _|_   _/ _ \ / _ \| |    ")
    print("| |\/| | | | | |  | |  | |  | || | | | | | | |    ")
    print("| |  | | |_| | |__| |  | |  | || |_| | |_| | |___ ")
    print("|_|  |_|\___/|____|_| |___| |_| \___/ \___/|_____|")
    print(f"{RESET}")
    print(f"{R}================================================={RESET}")
    print(f"{G}{BOLD}        💥 NEXUS MULTI-TOOL KIT v1.0 💥          {RESET}")
    print(f"{R}================================================={RESET}")
    print(f"{Y}Author   :{W} Rony Mollik")
    print(f"{Y}Github   :{W} https://github.com/mollikr985-create")
    print(f"{Y}Status   :{G} Online & Ready")
    print(f"{R}================================================={RESET}\n")

def system_info():
    banner()
    print(f"{C}[+] Fetching System & Network Info...{RESET}\n")
    print(f"{G}1. OS Platform   :{W} {sys.platform}")
    print(f"{G}2. Python Ver    :{W} {sys.version.split()[0]}")
    
    try:
        print(f"{G}3. Checking IP   :{Y} Requesting API...")
        ip = urlopen('https://api.ipify.org', timeout=5).read().decode('utf-8')
        print(f"{G}4. Your Public IP:{W} {ip}")
    except:
        print(f"{R}[✗] Public IP    : Offline / Connection Error")
    
    input(f"\n{Y}Press Enter to go back to Menu...{RESET}")

def web_checker():
    banner()
    print(f"{C}[+] Website Status Checker{RESET}\n")
    url = input(f"{Y}Enter URL (e.g., google.com): {W}").strip()
    if not url.startswith('http'):
        url = 'https://' + url
    try:
        print(f"{C}[*] Connecting to {url}...{RESET}")
        status = urlopen(url, timeout=6).getcode()
        if status == 200:
            print(f"\n{G}[✓] Website is LIVE & RUNNING! (Status: 200){RESET}")
        else:
            print(f"\n{Y}[!] Response received with Status Code: {status}{RESET}")
    except Exception as e:
        print(f"\n{R}[✗] Connection Failed! Website might be DOWN or URL is wrong.{RESET}")
    
    input(f"\n{Y}Press Enter to go back to Menu...{RESET}")

def pass_gen():
    banner()
    print(f"{C}[+] Secure Password Generator{RESET}\n")
    try:
        length = int(input(f"{Y}Enter password length (e.g., 14): {W}"))
        chars = string.ascii_letters + string.digits + "!@#$%^&*()"
        password = "".join(random.choice(chars) for _ in range(length))
        print(f"\n{G}[✓] Generated Password: {W}{password}{RESET}")
    except ValueError:
        print(f"\n{R}[✗] Invalid input! Please enter a number.{RESET}")
    
    input(f"\n{Y}Press Enter to go back to Menu...{RESET}")

def tg_tester():
    banner()
    print(f"{C}[+] Telegram Notification Tester{RESET}\n")
    token = input(f"{Y}Enter Bot Token: {W}").strip()
    chat_id = input(f"{Y}Enter Chat ID: {W}").strip()
    msg = "🚀 Hello from your Termux Multi-Tool Kit!"
    
    if token and chat_id:
        try:
            print(f"{C}[*] Sending notification via Telegram API...{RESET}")
            url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={msg}"
            urlopen(url, timeout=5)
            print(f"\n{G}[✓] Alert sent successfully! Check your Telegram.{RESET}")
        except Exception as e:
            print(f"\n{R}[✗] Failed to send. Check Token/Chat ID or Internet connection.{RESET}")
    else:
        print(f"\n{R}[✗] Token or Chat ID cannot be empty!{RESET}")
        
    input(f"\n{Y}Press Enter to go back to Menu...{RESET}")

def main():
    while True:
        banner()
        print(f"{W}[01] Check System & Public IP")
        print(f"{W}[02] Website Status Checker")
        print(f"{W}[03] Secure Password Generator")
        print(f"{W}[04] Telegram Alert Tester")
        print(f"{R}[00] Exit Tool{RESET}\n")
        
        choice = input(f"{C}Select an option >> {W}").strip()
        
        if choice in ['1', '01']:
            system_info()
        elif choice in ['2', '02']:
            web_checker()
        elif choice in ['3', '03']:
            pass_gen()
        elif choice in ['4', '04']:
            tg_tester()
        elif choice in ['0', '00']:
            print(f"\n{G}Thanks for using Nexus Kit! Happy Coding.{RESET}\n")
            break
        else:
            print(f"\n{R}[!] Invalid Option! Try again.{RESET}")
            time.sleep(1)

if __name__ == "__main__":
    main()
    
