from colorama import Fore
import sys

def quick_error(msg:str):
    print(Fore.RED + msg + Fore.RESET)
    sys.exit(1)