from colorama import init as coloarama_init
from colorama import Fore
class Speaker:
    name = ""
    def __init__(self):
        coloarama_init()
    def print_name(self):
        print(f"Hi my name is {Fore.GREEN}{self.name}!")
        