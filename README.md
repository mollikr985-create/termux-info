# ðŸ›¡ï¸ NEXUS Advanced Utility Kit v2.0

A beautiful, multi-tool CLI application for **Termux** & **Linux** â€” like the original NEXUS, but with the 403 Temp Mail error **fixed**.

## ðŸ”¥ What's New (v2.0)

The original NEXUS had a 403 Forbidden error on Temp Mail because 1secmail's public API is unreliable. **This version fixes that** by:

- **Primary:** `mail.tm` API (modern, reliable, no key required)
- **Fallback:** `1secmail` API (with proper User-Agent headers)
- **Auto-install:** Dependencies install on first run
- **Persistent storage:** Generated emails saved to `~/.nexus/temp_mail.json`

## âœ¨ Features

| # | Feature | Description |
|---|---------|-------------|
| 1 | ðŸ“§ **Temp Mail** | Generate disposable email + check inbox (mail.tm primary) |
| 2 | ðŸŒ **IP Lookup** | Geolocation, ISP, ASN, lat/lon |
| 3 | ðŸ” **WHOIS** | Domain registration info (RDAP) |
| 4 | ðŸ“¡ **DNS** | A, AAAA, MX, NS, TXT, CNAME records |
| 5 | ðŸ”Œ **Port Scanner** | Check open/closed ports |
| 6 | ðŸ” **Hash** | MD5, SHA1, SHA256, SHA512 |
| 7 | ðŸ”‘ **Password** | Strong random password generator |
| 8 | ðŸ”— **URL Shortener** | TinyURL API |
| 9 | ðŸ“± **QR Code** | Generate QR as PNG |
| 10 | ðŸ™ **GitHub** | User profile lookup |
| 11 | ðŸŒ¤ï¸ **Weather** | Current weather (wttr.in) |
| 12 | ðŸ”§ **More** | Base64, UUID, HTTP headers, system info |

## ðŸš€ Quick Start (Termux)

```bash
# 1. Install dependencies (only first time)
pkg install python -y
pip install -r requirements.txt

# 2. Run
python nexus.py

# Or use the quick run script
chmod +x run.sh
./run.sh
```

That's it! Dependencies auto-install on first run anyway.

## ðŸ“¦ Project Structure

```
nexus_tool/
â”œâ”€â”€ nexus.py           # Main script
â”œâ”€â”€ requirements.txt   # Python deps
â”œâ”€â”€ run.sh            # Quick run script
â””â”€â”€ README.md         # This file
```

## ðŸ› 403 Error Fix Explained

The original NEXUS used:
```python
requests.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox")
```

This fails with 403 because 1secmail now blocks requests without a proper browser User-Agent. **Fix:**

```python
SESSION.headers.update({
    "User-Agent": "Mozilla/5.0 (Linux; Android 12; Termux) AppleWebKit/537.36..."
})
```

Plus, we use **mail.tm** as the primary service which is more reliable than 1secmail.

## ðŸŽ¨ Interface

Same NEXUS-style ASCII art + colored menu:

```
   _   _  ___   __  __  ___  __  __ __   __
  | \ | || \ | ||  \/  ||_ _||  \/  |\ \ / /
  | .\| ||  \| || |\/| | | | | |\/| | \ V / 
  | |\  || |\  || |  | | | | | |  | |  | |  
  |_| \_||_| \_||_|  |_||___||_|  |_|  |_|  
                                            
â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
      ðŸš€ NEXUS ADVANCED UTILITY KIT ðŸš€
â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
  Author  : Mavis
  Status  : Authorized Edition
â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
```

## ðŸ’¡ Tips

- Generated emails are saved in `~/.nexus/temp_mail.json`
- Press `Ctrl+C` to exit anytime
- All tools work offline-fetched (need internet though)
- No API keys required for any feature

## ðŸ“œ License

Free to use, modify, and distribute.

---

**Made with â¤ï¸ for Termux users**
