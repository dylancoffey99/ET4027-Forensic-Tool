from os import path
from sys import argv

from tool import Tool


def main():
    tool = Tool(image_path)
    tool.read_partitions()
    tool.print_partitions()


if __name__ == "__main__":
    print("ET4027 FORENSIC TOOL - PHASE 2\nNAME = Dylan Coffey\nID = 18251382\n")
    if len(argv) > 1:
        image_path = argv[1]
        main()
    else:
        while True:
            image_path = input("Please drop an image into the terminal or type its path:")
            image_path = image_path.replace('"', "")
            if not path.exists(image_path):
                print("\nError: image path does not exist!\n")
            else:
                main()
                input("\nPress <ENTER> to input another image:\n")
