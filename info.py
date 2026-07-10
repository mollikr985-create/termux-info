#!/usr/bin/env python3
"""
â•”â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•—
â•‘   ðŸ›¡ï¸  NEXUS - Advanced Utility Kit                            â•‘
â•‘   Multi-Tool CLI for Termux & Linux                           â•‘
â•‘   Fixed: 1secmail 403 â†’ mail.tm primary + fallback system    â•‘
â•šâ•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
"""

import os
import sys
import json
import time
import random
import string
import hashlib
import base64
import uuid
import socket
import re
import secrets
import subprocess
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

# Auto-install dependencies on first run
def install_deps():
    needed = {
        'requests': 'requests',
        'colorama': 'colorama',
        'pyfiglet': 'pyfiglet'
    }
    for mod, pkg in needed.items():
        try:
            __import__(mod)
        except ImportError:
            print(f"[*] Installing {pkg}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"])

install_deps()

import requests
from colorama import init, Fore, Style
init(autoreset=True)
import pyfiglet

# ============== Color Setup ==============
class C:
    R  = Fore.RED
    G  = Fore.GREEN
    Y  = Fore.YELLOW
    B  = Fore.BLUE
    M  = Fore.MAGENTA
    CY = Fore.CYAN
    W  = Fore.WHITE
    BR = Style.BRIGHT
    X  = Style.RESET_ALL

# ============== Data Storage ==============
DATA_DIR = Path.home() / ".nexus"
DATA_DIR.mkdir(exist_ok=True)
TM_FILE = DATA_DIR / "temp_mail.json"

# ============== HTTP Session ==============
SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": "Mozilla/5.0 (Linux; Android 12; Termux) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
})

# ============== UI Helpers ==============
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    clear()
    art = pyfiglet.figlet_format("NEXUS", font="slant")
    print(f"{C.CY}{art}{C.X}")
    print(f"{C.R}{'â•'*60}{C.X}")
    print(f"{C.Y}{C.BR}       ðŸš€ NEXUS ADVANCED UTILITY KIT ðŸš€{C.X}")
    print(f"{C.R}{'â•'*60}{C.X}")
    print(f"{C.G}  Author  : {C.W}Mavis")
    print(f"{C.G}  Github  : {C.W}https://github.com/nexus-tool")
    print(f"{C.G}  Status  : {C.W}Authorized Edition")
    print(f"{C.G}  Version : {C.W}2.0 (Fixed){C.X}")
    print(f"{C.R}{'â•'*60}{C.X}")

def err(msg):  print(f"{C.R}[x] {msg}{C.X}")
def ok(msg):   print(f"{C.G}[âœ“] {msg}{C.X}")
def info(msg): print(f"{C.CY}[*] {msg}{C.X}")
def warn(msg): print(f"{C.Y}[!] {msg}{C.X}")
def head(t):
    print(f"\n{C.R}{'â”€'*60}")
    print(f"{C.Y}  {t}")
    print(f"{C.R}{'â”€'*60}{C.X}\n")

def back():
    input(f"\n{C.Y}Press Enter to go back...{C.X}")

def hr():
    print(f"{C.R}{'â”€'*60}{C.X}")

def pause(t=1):
    time.sleep(t)

# ============== Temp Mail â€” mail.tm (PRIMARY) ==============
def tm_get_domain():
    try:
        r = SESSION.get("https://api.mail.tm/domains", timeout=10)
        if r.status_code == 200:
            for d in r.json().get("hydra:member", []):
                if d.get("isActive") and not d.get("isPrivate"):
                    return d["domain"]
    except Exception as e:
        info(f"mail.tm domain fetch error: {e}")
    return None

def tm_create_account():
    domain = tm_get_domain()
    if not domain:
        return None
    
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
    address = f"{username}@{domain}"
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
    
    try:
        r = SESSION.post("https://api.mail.tm/accounts", 
                        json={"address": address, "password": password}, 
                        timeout=15)
        if r.status_code in (200, 201):
            tr = SESSION.post("https://api.mail.tm/token",
                            json={"address": address, "password": password},
                            timeout=15)
            if tr.status_code == 200:
                return {
                    "service": "mail.tm",
                    "address": address,
                    "password": password,
                    "token": tr.json().get("token"),
                    "id": r.json().get("id")
                }
    except Exception as e:
        info(f"mail.tm account error: {e}")
    return None

def tm_inbox(token):
    try:
        r = SESSION.get("https://api.mail.tm/messages",
                       headers={"Authorization": f"Bearer {token}"},
                       timeout=10)
        if r.status_code == 200:
            return r.json().get("hydra:member", [])
    except:
        pass
    return []

def tm_read(token, msg_id):
    try:
        r = SESSION.get(f"https://api.mail.tm/messages/{msg_id}",
                       headers={"Authorization": f"Bearer {token}"},
                       timeout=10)
        if r.status_code == 200:
            return r.json()
    except:
        pass
    return None

# ============== Temp Mail â€” GuerrillaMail (3rd FALLBACK) ==============
def gma_get_email():
    """Get GuerrillaMail email"""
    try:
        r = SESSION.get("https://api.guerrillamail.com/ajax.php?f=get_email_address", timeout=10)
        if r.status_code == 200:
            d = r.json()
            return {
                "service": "guerrillamail",
                "address": d.get("email_addr"),
                "sid": d.get("sid_token")
            }
    except:
        pass
    return None

def gma_inbox(sid):
    """Get GuerrillaMail inbox"""
    try:
        r = SESSION.get(f"https://api.guerrillamail.com/ajax.php?f=get_email_list&offset=0&sid_token={sid}", timeout=10)
        if r.status_code == 200:
            return r.json().get("mail_list", [])
    except:
        pass
    return []

def gma_read(sid, msg_id):
    """Read GuerrillaMail message"""
    try:
        r = SESSION.get(f"https://api.guerrillamail.com/ajax.php?f=fetch_email&email_id={msg_id}&sid_token={sid}", timeout=10)
        if r.status_code == 200:
            return r.json()
    except:
        pass
    return None

# ============== Temp Mail â€” 1secmail (2nd FALLBACK) ==============
def osm_generate():
    try:
        r = SESSION.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1", timeout=10)
        if r.status_code == 200 and r.json():
            return r.json()[0]
    except:
        pass
    return None

def osm_inbox(login, domain):
    try:
        r = SESSION.get(f"https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}", timeout=10)
        if r.status_code == 200:
            return r.json()
    except:
        pass
    return []

def osm_read(login, domain, msg_id):
    try:
        r = SESSION.get(f"https://www.1secmail.com/api/v1/?action=readMessage&login={login}&domain={domain}&id={msg_id}", timeout=10)
        if r.status_code == 200:
            return r.json()
    except:
        pass
    return None

# ============== Network Tools ==============
def ip_lookup(ip=None):
    head("ðŸŒ IP ADDRESS LOOKUP")
    if not ip:
        ip = input(f"  {C.Y}Enter IP (blank for your IP): {C.X}").strip()
    
    if not ip:
        try:
            ip = SESSION.get("https://api.ipify.org", timeout=10).text
        except:
            err("Could not detect your IP")
            back()
            return
    
    info(f"Looking up {ip}...")
    try:
        r = SESSION.get(f"http://ip-api.com/json/{ip}", timeout=10)
        d = r.json()
        if d.get("status") == "fail":
            err(f"Lookup failed: {d.get('message')}")
        else:
            print(f"  {C.G}IP: {C.W}{d.get('query', ip)}")
            print(f"  {C.G}Country: {C.W}{d.get('country', 'N/A')} ({d.get('countryCode', '')})")
            print(f"  {C.G}Region: {C.W}{d.get('regionName', 'N/A')}")
            print(f"  {C.G}City: {C.W}{d.get('city', 'N/A')}")
            print(f"  {C.G}ZIP: {C.W}{d.get('zip', 'N/A')}")
            print(f"  {C.G}Lat/Lon: {C.W}{d.get('lat', 'N/A')}, {d.get('lon', 'N/A')}")
            print(f"  {C.G}Timezone: {C.W}{d.get('timezone', 'N/A')}")
            print(f"  {C.G}ISP: {C.W}{d.get('isp', 'N/A')}")
            print(f"  {C.G}Org: {C.W}{d.get('org', 'N/A')}")
            print(f"  {C.G}AS: {C.W}{d.get('as', 'N/A')}")
    except Exception as e:
        err(f"Error: {e}")
    back()

def whois_lookup():
    head("ðŸ” WEBSITE WHOIS LOOKUP")
    domain = input(f"  {C.Y}Enter domain (e.g. google.com): {C.X}").strip().lower()
    if not domain:
        err("Domain required")
        back()
        return
    
    domain = domain.replace("http://", "").replace("https://", "").split("/")[0]
    info(f"Looking up {domain}...")
    
    # Try RDAP first
    try:
        r = SESSION.get(f"https://rdap.org/domain/{domain}",
                       headers={"Accept": "application/json"}, timeout=10)
        if r.status_code == 200:
            d = r.json()
            events = {e.get("eventName"): e.get("eventDate", "N/A") for e in d.get("events", [])}
            registrar = "N/A"
            for ent in d.get("entities", []):
                if "registrar" in ent.get("roles", []):
                    vcard = ent.get("vcardArray", [])
                    if vcard and len(vcard) > 1:
                        for item in vcard[1]:
                            if item[0] == "fn":
                                registrar = item[3]
                                break
                    break
            ns = ", ".join(n.get("ldhName", "") for n in d.get("nameservers", [])[:3]) or "N/A"
            print(f"  {C.G}Domain: {C.W}{d.get('ldhName', domain)}")
            print(f"  {C.G}Registrar: {C.W}{registrar}")
            print(f"  {C.G}Created: {C.W}{events.get('registration', 'N/A')}")
            print(f"  {C.G}Expires: {C.W}{events.get('expiration', 'N/A')}")
            print(f"  {C.G}Updated: {C.W}{events.get('last changed', 'N/A')}")
            print(f"  {C.G}Status: {C.W}{', '.join(d.get('status', [])) or 'N/A'}")
            print(f"  {C.G}Nameservers: {C.W}{ns}")
            back()
            return
    except:
        pass
    
    # Fallback to who-dat
    try:
        r = SESSION.get(f"https://who-dat.as93.net/{domain}", timeout=10)
        d = r.json()
        if d.get("result") == "success":
            reg = d.get("registrar", {})
            print(f"  {C.G}Domain: {C.W}{d.get('domain_name', domain)}")
            print(f"  {C.G}Registrar: {C.W}{reg.get('name', 'N/A')}")
            print(f"  {C.G}Created: {C.W}{d.get('creation_date', 'N/A')}")
            print(f"  {C.G}Expires: {C.W}{d.get('expiration_date', 'N/A')}")
            print(f"  {C.G}Status: {C.W}{d.get('status', 'N/A')}")
            print(f"  {C.G}NS: {C.W}{', '.join(d.get('name_servers', [])) or 'N/A'}")
        else:
            err("Lookup failed")
    except Exception as e:
        err(f"Error: {e}")
    back()

def dns_lookup():
    head("ðŸ“¡ DNS RECORDS LOOKUP")
    domain = input(f"  {C.Y}Enter domain: {C.X}").strip().lower()
    if not domain:
        back()
        return
    domain = domain.replace("http://", "").replace("https://", "").split("/")[0]
    info(f"Resolving DNS for {domain}...")
    
    types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME']
    found = False
    for t in types:
        try:
            r = SESSION.get(f"https://dns.google/resolve?name={domain}&type={t}", timeout=10)
            d = r.json()
            if d.get("Answer"):
                found = True
                print(f"\n  {C.Y}[{t} Records]{C.X}")
                for ans in d["Answer"][:5]:
                    print(f"    {C.W}â†’ {ans.get('data', 'N/A')}{C.X}")
        except:
            continue
    
    if not found:
        err("No DNS records found")
    back()

def port_check():
    head("ðŸ”Œ PORT CHECKER")
    host = input(f"  {C.Y}Enter host (e.g. google.com): {C.X}").strip()
    port_str = input(f"  {C.Y}Enter port (e.g. 443): {C.X}").strip()
    if not host or not port_str:
        back()
        return
    try:
        port = int(port_str)
    except:
        err("Invalid port")
        back()
        return
    
    info(f"Checking {host}:{port}...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        r = sock.connect_ex((host, port))
        sock.close()
        if r == 0:
            ok(f"Port {port} is OPEN on {host}")
        else:
            err(f"Port {port} is CLOSED on {host}")
    except Exception as e:
        err(f"Error: {e}")
    back()

# ============== Crypto Tools ==============
def hash_gen():
    head("ðŸ” HASH GENERATOR")
    text = input(f"  {C.Y}Enter text: {C.X}")
    if not text:
        back()
        return
    print()
    print(f"  {C.G}MD5:    {C.W}{hashlib.md5(text.encode()).hexdigest()}")
    print(f"  {C.G}SHA1:   {C.W}{hashlib.sha1(text.encode()).hexdigest()}")
    print(f"  {C.G}SHA256: {C.W}{hashlib.sha256(text.encode()).hexdigest()}")
    print(f"  {C.G}SHA512: {C.W}{hashlib.sha512(text.encode()).hexdigest()}")
    back()

def b64_tool():
    head("ðŸ” BASE64 ENCODE/DECODE")
    print(f"  {C.G}[1]{C.W} Encode")
    print(f"  {C.G}[2]{C.W} Decode")
    mode = input(f"\n  {C.Y}Choose: {C.X}").strip()
    text = input(f"  {C.Y}Enter text: {C.X}")
    try:
        if mode == "1":
            result = base64.b64encode(text.encode()).decode()
            ok(f"Encoded: {result}")
        elif mode == "2":
            result = base64.b64decode(text).decode()
            ok(f"Decoded: {result}")
        else:
            err("Invalid choice")
    except Exception as e:
        err(f"Error: {e}")
    back()

# ============== Generators ==============
def uuid_gen():
    head("ðŸŽ² UUID GENERATOR")
    count = input(f"  {C.Y}How many? (1-20, default 5): {C.X}").strip()
    try:
        n = int(count) if count else 5
        n = max(1, min(20, n))
    except:
        n = 5
    for _ in range(n):
        print(f"  {C.CY}â†’ {C.W}{uuid.uuid4()}")
    back()

def password_gen():
    head("ðŸ”‘ PASSWORD GENERATOR")
    length = input(f"  {C.Y}Length (8-64, default 16): {C.X}").strip()
    try:
        l = int(length) if length else 16
        l = max(8, min(64, l))
    except:
        l = 16
    chars = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{}|;:,.<>?"
    pwd = ''.join(secrets.choice(chars) for _ in range(l))
    print(f"\n  {C.G}Password ({l} chars): {C.W}{pwd}")
    warn("Save it now. It won't be shown again.")
    back()

def qr_gen():
    head("ðŸ“± QR CODE GENERATOR")
    text = input(f"  {C.Y}Enter text/URL: {C.X}").strip()
    if not text:
        back()
        return
    url = f"https://api.qrserver.com/v1/create-qr-code/?size=500x500&data={text}"
    qr_file = DATA_DIR / "qrcode.png"
    try:
        r = SESSION.get(url, timeout=15)
        if r.status_code == 200:
            qr_file.write_bytes(r.content)
            ok(f"QR saved to: {qr_file}")
            print(f"  {C.CY}Open the image to view QR code{C.X}")
        else:
            err("QR generation failed")
    except Exception as e:
        err(f"Error: {e}")
    back()

# ============== Web Tools ==============
def url_shorten():
    head("ðŸ”— URL SHORTENER")
    url = input(f"  {C.Y}Enter URL: {C.X}").strip()
    if not url.startswith("http"):
        url = "https://" + url
    try:
        r = SESSION.get(f"https://tinyurl.com/api-create.php?url={url}", timeout=10)
        if "tinyurl" in r.text:
            ok(f"Short URL: {r.text}")
        else:
            err("Shortening failed")
    except Exception as e:
        err(f"Error: {e}")
    back()

def github_lookup():
    head("ðŸ™ GITHUB USER LOOKUP")
    user = input(f"  {C.Y}Enter GitHub username: {C.X}").strip()
    if not user:
        back()
        return
    info(f"Fetching {user}...")
    try:
        u = SESSION.get(f"https://api.github.com/users/{user}", timeout=10).json()
        if "message" in u:
            err(f"User not found")
        else:
            print(f"  {C.G}Name: {C.W}{u.get('name', 'N/A')}")
            print(f"  {C.G}Bio: {C.W}{u.get('bio', 'N/A')}")
            print(f"  {C.G}Location: {C.W}{u.get('location', 'N/A')}")
            print(f"  {C.G}Public Repos: {C.W}{u.get('public_repos', 0)}")
            print(f"  {C.G}Followers: {C.W}{u.get('followers', 0)}")
            print(f"  {C.G}Following: {C.W}{u.get('following', 0)}")
            print(f"  {C.G}Profile: {C.W}{u.get('html_url', 'N/A')}")
            print(f"  {C.G}Created: {C.W}{u.get('created_at', 'N/A')[:10]}")
    except Exception as e:
        err(f"Error: {e}")
    back()

def weather_lookup():
    head("ðŸŒ¤ï¸ WEATHER LOOKUP")
    city = input(f"  {C.Y}Enter city: {C.X}").strip()
    if not city:
        back()
        return
    try:
        r = SESSION.get(f"https://wttr.in/{city}?format=j1", timeout=15)
        d = r.json()
        if "current_condition" not in d:
            err("Could not fetch weather")
        else:
            cur = d["current_condition"][0]
            area = d.get("nearest_area", [{}])[0]
            name = area.get("areaName", [{}])[0].get("value", city)
            country = area.get("country", [{}])[0].get("value", "")
            print(f"  {C.G}Location: {C.W}{name}, {country}")
            print(f"  {C.G}Temp: {C.W}{cur.get('temp_C')}Â°C / {cur.get('temp_F')}Â°F")
            print(f"  {C.G}Feels Like: {C.W}{cur.get('FeelsLikeC')}Â°C")
            print(f"  {C.G}Condition: {C.W}{cur.get('weatherDesc', [{}])[0].get('value', 'N/A')}")
            print(f"  {C.G}Humidity: {C.W}{cur.get('humidity')}%")
            print(f"  {C.G}Wind: {C.W}{cur.get('windspeedKmph')} km/h")
    except Exception as e:
        err(f"Error: {e}")
    back()

# ============== More Tools ==============
def more_tools():
    while True:
        clear()
        banner()
        print(f"{C.CY}  â•”â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•—")
        print(f"{C.CY}  â•‘  {C.Y}MORE TOOLS{C.CY}                              â•‘")
        print(f"{C.CY}  â• â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•£")
        print(f"{C.CY}  â•‘  {C.G}[1]{C.W} ðŸ” Base64                            {C.CY}â•‘")
        print(f"{C.CY}  â•‘  {C.G}[2]{C.W} ðŸ†” UUID Generator                    {C.CY}â•‘")
        print(f"{C.CY}  â•‘  {C.G}[3]{C.W} ðŸŒ HTTP Headers                      {C.CY}â•‘")
        print(f"{C.CY}  â•‘  {C.G}[4]{C.W} ðŸŽ¨ Color Picker                      {C.CY}â•‘")
        print(f"{C.CY}  â•‘  {C.G}[5]{C.W} ðŸ“Š System Info                       {C.CY}â•‘")
        print(f"{C.CY}  â•‘  {C.G}[6]{C.W} ðŸ”™ Back to Main Menu                 {C.CY}â•‘")
        print(f"{C.CY}  â•šâ•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•")
        ch = input(f"\n  {C.Y}nexus > {C.X}").strip()
        if ch == "1": b64_tool()
        elif ch == "2": uuid_gen()
        elif ch == "3": http_headers()
        elif ch == "4": color_picker()
        elif ch == "5": sys_info()
        elif ch == "6": return
        else: err("Invalid option"); pause()

def http_headers():
    head("ðŸŒ HTTP HEADERS LOOKUP")
    url = input(f"  {C.Y}Enter URL: {C.X}").strip()
    if not url.startswith("http"):
        url = "https://" + url
    try:
        r = SESSION.get(url, timeout=10, allow_redirects=True)
        print(f"\n  {C.G}Status: {C.W}{r.status_code} {r.reason}")
        for k, v in r.headers.items():
    
