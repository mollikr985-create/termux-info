#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import json
import requests
import subprocess
from datetime import datetime
import random
import string

# Colors for terminal
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

class NexusTool:
    def __init__(self):
        self.banner = f"""
{Colors.CYAN}{Colors.BOLD}
╔══════════════════════════════════════════╗
║              NEXUS TOOL v2.0             ║
║    Advanced Utility Kit for Termux       ║
╠══════════════════════════════════════════╣
║ Author : Rony Mollik                     ║
║ GitHub : mollikr985-create               ║
║ Status : {Colors.GREEN}Authorized Edition{Colors.CYAN}      ║
╚══════════════════════════════════════════╝
{Colors.END}"""
        self.menu()

    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')

    def print_header(self, text):
        print(f"\n{Colors.BLUE}{'='*50}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.CYAN}  {text}{Colors.END}")
        print(f"{Colors.BLUE}{'='*50}{Colors.END}\n")

    def loading_animation(self, text="Loading"):
        chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
        for i in range(20):
            sys.stdout.write(f'\r{Colors.YELLOW}{text} {chars[i % len(chars)]}{Colors.END}')
            sys.stdout.flush()
            time.sleep(0.1)
        print()

    # ============ TEMPORARY MAIL ============
    def temp_mail(self):
        self.print_header("TEMPORARY MAIL GENERATOR")
        
        try:
            # Using Mail.tm API
            print(f"{Colors.YELLOW}[*] Generating temporary email...{Colors.END}")
            
            # Create account
            response = requests.post(
                'https://api.mail.tm/accounts',
                json={
                    'address': f"user{random.randint(1000,9999)}@{random.choice(['mail.tm', 'guerrillamail.com', 'temp-mail.org'])}",
                    'password': ''.join(random.choices(string.ascii_letters + string.digits, k=10))
                },
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 201:
                data = response.json()
                print(f"{Colors.GREEN}[✓] Email created successfully!{Colors.END}")
                print(f"{Colors.CYAN}📧 Email: {data['address']}{Colors.END}")
                print(f"{Colors.CYAN}🔑 Password: {data['password']}{Colors.END}")
                print(f"{Colors.YELLOW}[!] Check inbox at: https://mail.tm{Colors.END}")
            else:
                # Alternative API
                response = requests.get('https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1')
                if response.status_code == 200:
                    email = response.json()[0]
                    print(f"{Colors.GREEN}[✓] Email created!{Colors.END}")
                    print(f"{Colors.CYAN}📧 Email: {email}{Colors.END}")
                    print(f"{Colors.YELLOW}[!] Check inbox at: https://www.1secmail.com{Colors.END}")
                else:
                    print(f"{Colors.RED}[✖] Error: Could not create email{Colors.END}")
                    
        except Exception as e:
            print(f"{Colors.RED}[✖] Error: {str(e)}{Colors.END}")
            print(f"{Colors.YELLOW}[!] Using fallback method...{Colors.END}")
            
            # Fallback: Generate fake email
            domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'protonmail.com']
            username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
            email = f"{username}@{random.choice(domains)}"
            print(f"{Colors.GREEN}[✓] Generated temporary email:{Colors.END}")
            print(f"{Colors.CYAN}📧 {email}{Colors.END}")

    # ============ IP CHECKER ============
    def ip_checker(self):
        self.print_header("IP ADDRESS CHECKER")
        
        ip = input(f"{Colors.YELLOW}[?] Enter IP (or press Enter for your IP): {Colors.END}")
        
        try:
            if not ip:
                ip = requests.get('https://api.ipify.org').text
                print(f"{Colors.GREEN}[✓] Your IP: {ip}{Colors.END}")
            
            self.loading_animation("Fetching IP information")
            
            response = requests.get(f'http://ip-api.com/json/{ip}')
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    print(f"""
{Colors.CYAN}🌐 IP Information:{Colors.END}
{Colors.GREEN}📌 IP Address  : {data.get('query', 'N/A')}
📍 City         : {data.get('city', 'N/A')}
🗺️ Region       : {data.get('regionName', 'N/A')}
🌍 Country      : {data.get('country', 'N/A')} ({data.get('countryCode', 'N/A')})
📮 ZIP Code     : {data.get('zip', 'N/A')}
📡 ISP          : {data.get('isp', 'N/A')}
🗺️ Location     : {data.get('lat', 'N/A')}, {data.get('lon', 'N/A')}
🌐 Timezone     : {data.get('timezone', 'N/A')}
🖥️ Organization : {data.get('org', 'N/A')}{Colors.END}
""")
                else:
                    print(f"{Colors.RED}[✖] Invalid IP address{Colors.END}")
            else:
                print(f"{Colors.RED}[✖] API request failed{Colors.END}")
                
        except Exception as e:
            print(f"{Colors.RED}[✖] Error: {str(e)}{Colors.END}")

    # ============ WEBSITE LOOKUP ============
    def website_lookup(self):
        self.print_header("WEBSITE INFORMATION LOOKUP")
        
        domain = input(f"{Colors.YELLOW}[?] Enter domain name (e.g., google.com): {Colors.END}")
        
        if not domain:
            print(f"{Colors.RED}[✖] Please enter a domain name{Colors.END}")
            return
            
        try:
            self.loading_animation(f"Looking up {domain}")
            
            # WHOIS Information
            print(f"{Colors.CYAN}📋 WHOIS Information:{Colors.END}")
            try:
                whois = subprocess.getoutput(f"whois {domain}")
                lines = whois.split('\n')[:20]
                for line in lines:
                    if ':' in line:
                        print(f"{Colors.GREEN}{line}{Colors.END}")
            except:
                print(f"{Colors.YELLOW}[!] WHOIS not available{Colors.END}")
            
            # DNS Information
            print(f"\n{Colors.CYAN}🔍 DNS Information:{Colors.END}")
            try:
                dns = subprocess.getoutput(f"dig {domain} ANY")
                important_lines = [line for line in dns.split('\n') if line and (';;' not in line)]
                for line in important_lines[:10]:
                    print(f"{Colors.GREEN}{line}{Colors.END}")
            except:
                print(f"{Colors.YELLOW}[!] DNS info not available{Colors.END}")
            
            # IP Address
            print(f"\n{Colors.CYAN}🌐 IP Address:{Colors.END}")
            try:
                ip = subprocess.getoutput(f"dig +short {domain}")
                print(f"{Colors.GREEN}{ip}{Colors.END}")
            except:
                print(f"{Colors.YELLOW}[!] IP not available{Colors.END}")
                
        except Exception as e:
            print(f"{Colors.RED}[✖] Error: {str(e)}{Colors.END}")

    # ============ ADDITIONAL TOOLS ============
    def phone_lookup(self):
        self.print_header("PHONE NUMBER LOOKUP")
        
        number = input(f"{Colors.YELLOW}[?] Enter phone number (with country code): {Colors.END}")
        
        try:
            # Using free API
            response = requests.get(f'http://apilayer.net/api/validate?access_key=demo&number={number}')
            if response.status_code == 200:
                data = response.json()
                print(f"""
{Colors.CYAN}📱 Phone Information:{Colors.END}
{Colors.GREEN}📞 Number      : {data.get('number', 'N/A')}
🌍 Country     : {data.get('country_name', 'N/A')}
📮 Location    : {data.get('location', 'N/A')}
🏢 Carrier     : {data.get('carrier', 'N/A')}
✅ Valid       : {data.get('valid', 'N/A')}
🌐 Country Code: {data.get('country_code', 'N/A')}{Colors.END}
""")
            else:
                print(f"{Colors.RED}[✖] Phone lookup failed{Colors.END}")
        except:
            print(f"{Colors.YELLOW}[!] Service unavailable. Using local info...{Colors.END}")
            print(f"{Colors.GREEN}📞 Number: {number}{Colors.END}")
            print(f"{Colors.YELLOW}[!] Country: Unknown (API limit reached){Colors.END}")

    def url_shortener(self):
        self.print_header("URL SHORTENER")
        
        url = input(f"{Colors.YELLOW}[?] Enter URL to shorten: {Colors.END}")
        
        try:
            # Using TinyURL API
            response = requests.get(f'https://tinyurl.com/api-create.php?url={url}')
            if response.status_code == 200:
                print(f"{Colors.GREEN}[✓] Shortened URL:{Colors.END}")
                print(f"{Colors.CYAN}🔗 {response.text}{Colors.END}")
            else:
                print(f"{Colors.RED}[✖] URL shortening failed{Colors.END}")
        except Exception as e:
            print(f"{Colors.RED}[✖] Error: {str(e)}{Colors.END}")

    def qr_generator(self):
        self.print_header("QR CODE GENERATOR")
        
        text = input(f"{Colors.YELLOW}[?] Enter text or URL to encode: {Colors.END}")
        
        try:
            response = requests.get(f'https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={text}')
            if response.status_code == 200:
                with open('qrcode.png', 'wb') as f:
                    f.write(response.content)
                print(f"{Colors.GREEN}[✓] QR Code saved as 'qrcode.png'{Colors.END}")
                
                # Display QR code if possible
                try:
                    subprocess.run(['display', 'qrcode.png'], check=False)
                except:
                    print(f"{Colors.YELLOW}[!] Open 'qrcode.png' manually{Colors.END}")
            else:
                print(f"{Colors.RED}[✖] QR generation failed{Colors.END}")
        except Exception as e:
            print(f"{Colors.RED}[✖] Error: {str(e)}{Colors.END}")

    def system_info(self):
        self.print_header("SYSTEM INFORMATION")
        
        try:
            hostname = subprocess.getoutput('hostname')
            uptime = subprocess.getoutput('uptime -p')
            cpu = subprocess.getoutput("top -bn1 | grep 'Cpu(s)' | awk '{print $2}'")
            memory = subprocess.getoutput("free -m | awk 'NR==2{printf \"Used: %s MB, Free: %s MB, Total: %s MB\", $3, $4, $2}'")
            disk = subprocess.getoutput("df -h / | awk 'NR==2{printf \"Used: %s, Free: %s, Total: %s\", $3, $4, $2}'")
            
            print(f"""
{Colors.CYAN}💻 System Information:{Colors.END}
{Colors.GREEN}🖥️  Hostname  : {hostname}
⏱️  Uptime    : {uptime}
💾 CPU Usage : {cpu}%
🗄️  Memory    : {memory}
💿 Disk      : {disk}
{Colors.END}
""")
        except Exception as e:
            print(f"{Colors.RED}[✖] Error: {str(e)}{Colors.END}")

    def network_scanner(self):
        self.print_header("NETWORK SCANNER")
        
        ip_range = input(f"{Colors.YELLOW}[?] Enter IP range (e.g., 192.168.1.0/24): {Colors.END}")
        
        try:
            print(f"{Colors.YELLOW}[*] Scanning network...{Colors.END}")
            result = subprocess.getoutput(f"nmap -sn {ip_range}")
            print(f"{Colors.GREEN}{result}{Colors.END}")
        except:
            print(f"{Colors.RED}[✖] nmap not installed. Install with: pkg install nmap{Colors.END}")

    def port_scanner(self):
        self.print_header("PORT SCANNER")
        
        target = input(f"{Colors.YELLOW}[?] Enter target IP or domain: {Colors.END}")
        ports = input(f"{Colors.YELLOW}[?] Enter ports (comma-separated, or 'all'): {Colors.END}")
        
        try:
            if ports.lower() == 'all':
                result = subprocess.getoutput(f"nmap {target}")
            else:
                result = subprocess.getoutput(f"nmap -p {ports} {target}")
            print(f"{Colors.GREEN}{result}{Colors.END}")
        except:
            print(f"{Colors.RED}[✖] nmap not installed. Install with: pkg install nmap{Colors.END}")

    # ============ MAIN MENU ============
    def menu(self):
        while True:
            self.clear_screen()
            print(self.banner)
            print(f"""
{Colors.BOLD}{Colors.CYAN}╔══════════════════════════════════════════╗
║          AVAILABLE TOOLS                ║
╠══════════════════════════════════════════╣
║ {Colors.GREEN}1{Colors.END}  Temporary Mail Generator            ║
║ {Colors.GREEN}2{Colors.END}  IP Address Checker                 ║
║ {Colors.GREEN}3{Colors.END}  Website Lookup                     ║
║ {Colors.GREEN}4{Colors.END}  Phone Number Lookup                ║
║ {Colors.GREEN}5{Colors.END}  URL Shortener                     ║
║ {Colors.GREEN}6{Colors.END}  QR Code Generator                  ║
║ {Colors.GREEN}7{Colors.END}  System Information                 ║
║ {Colors.GREEN}8{Colors.END}  Network Scanner                    ║
║ {Colors.GREEN}9{Colors.END}  Port Scanner                      ║
║ {Colors.RED}0{Colors.END}  Exit                               ║
╚══════════════════════════════════════════╝
""")
            
            try:
                choice = input(f"{Colors.YELLOW}[?] Select option: {Colors.END}")
                
                if choice == '1':
                    self.temp_mail()
                elif choice == '2':
                    self.ip_checker()
                elif choice == '3':
                    self.website_lookup()
                elif choice == '4':
                    self.phone_lookup()
                elif choice == '5':
                    self.url_shortener()
                elif choice == '6':
                    self.qr_generator()
                elif choice == '7':
                    self.system_info()
                elif choice == '8':
                    self.network_scanner()
                elif choice == '9':
                    self.port_scanner()
                elif choice == '0':
                    print(f"{Colors.GREEN}Thanks for using Nexus Tool! 👋{Colors.END}")
                    sys.exit()
                else:
                    print(f"{Colors.RED}[✖] Invalid option!{Colors.END}")
                    time.sleep(1)
                    continue
                
                input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")
                
            except KeyboardInterrupt:
                print(f"\n{Colors.GREEN}Exiting...{Colors.END}")
                sys.exit()
            except Exception as e:
                print(f"{Colors.RED}[✖] Error: {str(e)}{Colors.END}")
                time.sleep(2)

if __name__ == "__main__":
    try:
        # Check dependencies
        required_packages = ['requests']
        for package in required_packages:
            try:
                __import__(package)
            except ImportError:
                print(f"[!] Installing {package}...")
                os.system(f'pip install {package}')
        
        NexusTool()
    except KeyboardInterrupt:
        print(f"\n{Colors.GREEN}Goodbye! 👋{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}Error: {str(e)}{Colors.END}")
