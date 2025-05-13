from acd_unique_package.speakers import Acd
from pathlib import Path

def main():
    Acd().print_name()

    #with open("names.txt", "r") as f:
    with open(Path(__file__).parent / "names.txt", "r") as f:
        print(f.read())

if __name__ == "__main__":
    main()