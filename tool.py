from partitions.fat import FAT16
from partitions.ntfs import NTFS
from partitions.partition import Partition


class Tool:
    def __init__(self, image_path):
        self.image_path = image_path
        self.buffer = bytes(64)
        self.valid_partitions = 0

    def read_partitions(self):
        with open(self.image_path, "rb") as image:
            image.seek(0x1BE)
            self.buffer = image.read(64)

    def get_partitions(self):
        partitions = []
        for i in range(0, 4):
            partition_entry = i * 16
            partition_type = self.get_bytes(1, partition_entry + 0x04)
            start_sector = self.get_bytes(4, partition_entry + 0x08)
            partition_size = self.get_bytes(4, partition_entry + 0x0C)
            partition = self.get_partition(partition_type, start_sector, partition_size)
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

    def get_partition(self, partition_type, start_sector, partition_size):
        if partition_type == 0x06:
            fat_16 = FAT16(self.image_path, start_sector, partition_size)
            fat_16.get_fat_info()
            return fat_16
        if partition_type == 0x07:
            ntfs = NTFS(self.image_path, start_sector, partition_size)
            ntfs.get_ntfs_info()
            return ntfs
        return Partition(partition_type, start_sector, partition_size)

    def print_partitions(self):
        partitions = self.get_partitions()
        for i, partition in enumerate(partitions):
            print(f"\n============== Partition {i + 1} ==============")
            print(f"Partition Type = {partition.get_partition_type()}")
            print(f"Start Sector = {partition.get_start_sector()}")
            print(f"Partition Size (sectors) = {partition.get_partition_size()}")
            if isinstance(partition, FAT16):
                partition.print_fat_info()
            elif isinstance(partition, NTFS):
                partition.print_ntfs_info()
        print(f"\nTotal number of valid partitions = {self.valid_partitions}")
