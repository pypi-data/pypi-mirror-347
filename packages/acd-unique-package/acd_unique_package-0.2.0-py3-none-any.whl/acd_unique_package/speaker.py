from colorama import init, Fore

class Speaker:
    name = "default"

    def __init__(self):
        init()

    def print_name(self):
        print(f"Hi, my name is {Fore.GREEN}{self.name}")