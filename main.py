from os import path

from tool import Tool

if __name__ == "__main__":
    print("ET4027 FORENSIC TOOL - PHASE 2\nNAME = Dylan Coffey\nID = 18251382\n")
    while True:
        image_path = input("Please drop an image into the terminal or type its path:")
        image_path = image_path.replace('"', "")
        if not path.exists(image_path):
            print("\nError: image path does not exist!\n")
        else:
            tool = Tool(image_path)
            tool.read_partitions()
            tool.print_partitions()
            input("\nPress <ENTER> to input another image:\n")
