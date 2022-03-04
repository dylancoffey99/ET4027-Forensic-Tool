from os import path

from reader import Reader

if __name__ == "__main__":
    print("ET4027 FORENSIC TOOL - PHASE 1\nNAME = Dylan Coffey\nID = 18251382\n")
    while True:
        image_path = input("Please drop an image into the terminal or type its path:")
        if not path.exists(image_path):
            print("\nError: image path does not exist!\n")
        else:
            reader = Reader()
            reader.read_partitions(image_path)
            reader.print_partitions()
            input("\nPress <ENTER> to input another image:\n")
