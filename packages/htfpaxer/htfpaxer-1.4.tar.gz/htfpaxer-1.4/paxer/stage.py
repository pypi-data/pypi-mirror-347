from colorama import Fore
import sys
import keyboard as kb

def quick_error(msg:str):
    print(Fore.RED + msg + Fore.RESET)
    sys.exit(1)


def get_key() -> str:
    key = kb.read_key()
    while kb.is_pressed(key): ...
    return key