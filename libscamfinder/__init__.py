from colorama import Fore, Style
import sys

def check_key(KEY):
    if KEY == "" or len(KEY) != 39:
        print(f"{Style.BRIGHT}{Fore.RED}Invalid API Key!{Style.RESET_ALL}")
        sys.exit()
    else:
        print(f"{Style.BRIGHT}{Fore.GREEN}Using API Key: {Style.RESET_ALL}{KEY}")