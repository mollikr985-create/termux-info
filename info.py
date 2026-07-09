import os
import sys

def banner():
    os.system('clear')
    # ANSI Colors
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

    # ASCII Art Banner
    print(f"{CYAN}{BOLD}")
    print(" ____   ___  _   _ __   __")
    print("|  _ \ / _ \| \ | |\ \ / /")
    print("| |_) | | | |  \| | \ V / ")
    print("|  _ <| |_| | |\  |  | |  ")
    print("|_| \_\\\\___/|_| \_|  |_|  ")
    print(f"{RESET}")
    
    print(f"{RED}================================================={RESET}")
    print(f"{GREEN}{BOLD}      Information Display - Termux Tools       {RESET}")
    print(f"{RED}================================================={RESET}")
    
    # আপনার পার্সোনাল ইনফো
    print(f"{YELLOW}{BOLD}Author   :{RESET} Rony Mollik")
    print(f"{YELLOW}{BOLD}Role     :{RESET} Full-Stack Web & Bot Developer")
    print(f"{YELLOW}{BOLD}Location :{RESET} Magura, Bangladesh")
    print(f"{YELLOW}{BOLD}Github   :{RESET} https://github.com/mollikr985-create")
    print(f"{YELLOW}{BOLD}Skills   :{RESET} HTML, CSS, JS, Node.js, Python, Termux")
    print(f"{RED}================================================={RESET}")
    print(f"{GREEN}🎯 Status: Keep Coding & Stay Secure!{RESET}\n")

if __name__ == "__main__":
    banner()
  
