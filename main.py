from os import path

from reader import Reader

if __name__ == "__main__":
    while True:
        image_path = input("Please enter path of file system image:")
        if not path.exists(image_path):
            print("\nError: image path does not exist!\n")
        else:
            reader = Reader()
            reader.read_partitions(image_path)
            reader.print_partitions()
            break
