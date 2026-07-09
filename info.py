import os
import sys
import time
import json
import socket
from urllib.request import urlopen, Request

# ANSI Colors
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
    print(" _   _ _______  ___   _ ____  ")
    print("| \ | | ____\ \/ / | | / ___| ")
    print("|  \| |  _|  \  /| | | \___ \ ")
    print("| |\  | |___ /  \| |_| |___) |")
    print("|_| \_|_____/_/\_\\\\___/|____/ ")
    print(f"{RESET}")
    print(f"{R}================================================={RESET}")
    print(f"{G}{BOLD}        🚀 NEXUS ADVANCED UTILITY KIT 🚀        {RESET}")
    print(f"{R}================================================={RESET}")
    print(f"{Y}Author   :{W} Rony Mollik")
    print(f"{Y}Github   :{W} https://github.com/mollikr985-create")
    print(f"{Y}Status   :{G} Authorized Edition")
    print(f"{R}================================================={RESET}\n")

# --- FEATURE 1: TEMP MAIL ---
def temp_mail():
    banner()
    print(f"{C}[+] Temporary Mail Generator{RESET}\n")
    try:
        print(f"{Y}[*] Generating temporary email...{RESET}")
        req = Request("https://www.1secmail.com/api/v1/?action=genEmailAddresses&count=1", headers={'User-Agent': 'Mozilla'})
        email = json.loads(urlopen(req, timeout=7).read().decode('utf-8'))[0]
        name, domain = email.split('@')
        
        while True:
            banner()
            print(f"{C}[+] Temporary Mail Generator{RESET}\n")
            print(f"{G}Your Temp Email:{W} {email}\n")
            print(f"{Y}[1] Check Inbox (Refresh)")
            print(f"{R}[0] Back to Main Menu")
            
            opt = input(f"\n{C}Select Option >> {W}").strip()
            if opt == '1':
                print(f"\n{C}[*] Checking mailbox...{RESET}")
                chk_url = f"https://www.1secmail.com/api/v1/?action=getMessages&login={name}&domain={domain}"
                req_mail = Request(chk_url, headers={'User-Agent': 'Mozilla'})
                mails = json.loads(urlopen(req_mail, timeout=7).read().decode('utf-8'))
                
                if not mails:
                    print(f"{R}[!] Mailbox is empty. No messages received yet.{RESET}")
                else:
                    print(f"\n{G}[✓] New Messages Found:{RESET}")
                    for m in mails:
                        print(f"\n{G}ID: {W}{m['id']}")
                        print(f"{G}From: {W}{m['from']}")
                        print(f"{G}Subject: {W}{m['subject']}")
                        print(f"{G}Date: {W}{m['date']}")
                        print(f"{B}-----------------------------------------{RESET}")
                input(f"\n{Y}Press Enter to continue...{RESET}")
            elif opt == '0':
                break
    except Exception as e:
        print(f"{R}[✗] Error connecting to Temp Mail API.{RESET}")
        print(f"{Y}Error Details: {e}{RESET}")
        input(f"\n{Y}Press Enter to go back...{RESET}")

# --- FEATURE 2: IP CHECKER ---
def ip_checker():
    banner()
    print(f"{C}[+] IP Address Lookup Tool{RESET}\n")
    target_ip = input(f"{Y}Enter IP Address (Leave blank for your own IP): {W}").strip()
    try:
        url = f"http://ip-api.com/json/{target_ip}"
        data = json.loads(urlopen(url, timeout=7).read().decode('utf-8'))
        
        if data['status'] == 'success':
            print(f"\n{G}[✓] IP Details Found:{RESET}")
            print(f"{C}Target IP   :{W} {data.get('query')}")
            print(f"{C}Country     :{W} {data.get('country')} ({data.get('countryCode')})")
            print(f"{C}Region/State:{W} {data.get('regionName')}")
            print(f"{C}City        :{W} {data.get('city')}")
            print(f"{C}ZIP Code    :{W} {data.get('zip')}")
            print(f"{C}ISP         :{W} {data.get('isp')}")
            print(f"{C}ASN         :{W} {data.get('as')}")
        else:
            print(f"\n{R}[✗] Invalid IP address or data not found.{RESET}")
    except Exception as e:
        print(f"\n{R}[✗] Connection Error! Could not fetch IP details.{RESET}")
        
    input(f"\n{Y}Press Enter to go back to Menu...{RESET}")

# --- FEATURE 3: WEBSITE LOOKUP ---
def web_lookup():
    banner()
    print(f"{C}[+] Website Domain Lookup{RESET}\n")
    domain = input(f"{Y}Enter Website Domain (e.g., google.com): {W}").strip()
    if "://" in domain:
        domain = domain.split("://")[1]
    if "/" in domain:
        domain = domain.split("/")[0]
        
    try:
        print(f"\n{C}[*] Fetching DNS info for {domain}...{RESET}")
        ip_addr = socket.gethostbyname(domain)
        print(f"{G}[✓] Target Domain:{W} {domain}")
        print(f"{G}[✓] IP Address   :{W} {ip_addr}")
    except socket.gaierror:
        print(f"\n{R}[✗] Could not resolve domain. Make sure the URL is correct.{RESET}")
    except Exception as e:
        print(f"\n{R}[✗] An error occurred.{RESET}")
        
    input(f"\n{Y}Press Enter to go back to Menu...{RESET}")

# --- FEATURE 4: MANUAL TELEGRAM MESSENGER ---
def tg_messenger():
    banner()
    print(f"{C}[+] Manual Telegram Bot Messenger{RESET}\n")
    token = "7262426918:AAETLOfhl8Y3zouo0z-nJ2XAijn4gGOsUa4"
    chat_id = "6459093455"
    
    print(f"{G}Default Bot Configured Status: {Y}Ready{RESET}")
    text = input(f"{Y}Enter the message you want to send: {W}").strip()
    
    if text:
        try:
            import urllib.parse
            safe_text = urllib.parse.quote(text)
            url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={safe_text}"
            req = Request(url, headers={'User-Agent': 'Mozilla'})
            urlopen(req, timeout=7)
            print(f"\n{G}[✓] Message successfully sent to your Telegram Bot!{RESET}")
        except Exception as e:
            print(f"\n{R}[✗] Failed to send message. Please check network or bot status.{RESET}")
    else:
        print(f"\n{R}[✗] Message context cannot be empty!{RESET}")
        
    input(f"\n{Y}Press Enter to go back to Menu...{RESET}")

def main():
    while True:
        banner()
        print(f"{W}[01] Temp Mail Generator")
        print(f"{W}[02] IP Address Checker")
        print(f"{W}[03] Website Domain Lookup")
        print(f"{W}[04] Send Telegram Message (Manual)")
        print(f"{R}[00] Exit Tool{RESET}\n")
        
        choice = input(f"{C}Select an option >> {W}").strip()
        
        if choice in ['1', '01']:
            temp_mail()
        elif choice in ['2', '02']:
            ip_checker()
        elif choice in ['3', '03']:
            web_lookup()
        elif choice in ['4', '04']:
            tg_messenger()
        elif choice in ['0', '00']:
            print(f"\n{G}Thank you for using Nexus Kit! Stay safe.{RESET}\n")
            break
        else:
            print(f"\n{R}[!] Invalid Option! Try again.{RESET}")
            time.sleep(1)

if __name__ == "__main__":
    main()
            
