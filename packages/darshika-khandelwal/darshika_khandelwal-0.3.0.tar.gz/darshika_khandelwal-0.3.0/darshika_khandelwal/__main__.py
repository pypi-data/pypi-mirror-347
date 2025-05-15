from .speakers import Darshika
from pathlib import Path

def main():
    Darshika().print_name()
    # with open("names.txt") as f:
    with (Path(__file__).parent / "names.txt").open() as f:
        print(f.read())

if __name__ == "__main__":
    main()