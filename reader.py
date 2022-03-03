from partition import Partition


class Reader:
    def __init__(self):
        self.buffer = bytes(64)
        self.valid_partitions = 0

    def read_partitions(self, image_path):
        with open(image_path, "rb") as image:
            image.seek(0x1BE)
            self.buffer = image.read(64)

    def get_partitions(self):
        partitions = []
        for i in range(0, 4):
            partition_entry = i * 16
            partition_type = self.get_bytes(1, partition_entry + 0x04)
            start_sector = self.get_bytes(4, partition_entry + 0x08)
            partition_size = self.get_bytes(4, partition_entry + 0x0C)
            partition = Partition(partition_type, start_sector, partition_size)
            partitions.append(partition)
            if partition_type != 0x00:
                self.valid_partitions += 1
        return partitions

    def get_bytes(self, size, offset):
        byte_array = bytearray()
        for _ in range(size):
            byte = self.buffer[offset]
            byte_array.append(byte)
            offset += 0x01
        return int.from_bytes(byte_array, "little")

    def print_partitions(self):
        partitions = self.get_partitions()
        for i, partition in enumerate(partitions):
            print(f"\n============== Partition {i + 1} ==============")
            print(f"Partition Type = {partition.get_partition_type()}")
            print(f"Start Sector = {partition.get_start_sector()}")
            print(f"Partition Size = {partition.get_partition_size()}")
        print(f"\nTotal number of valid partitions = {self.valid_partitions}")
