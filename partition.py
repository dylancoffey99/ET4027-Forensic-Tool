class Partition:
    def __init__(self, partition_type, start_sector, partition_size):
        self.partition_type = partition_type
        self.start_sector = start_sector
        self.partition_size = partition_size

    def get_partition_type(self):
        if self.partition_type == 0x00:
            return "NOT-VALID"
        elif self.partition_type == 0x01:
            return "12-BIT FAT"
        elif self.partition_type == 0x04:
            return "16-BIT FAT"
        elif self.partition_type == 0x05:
            return "EXTENDED MS-DOS PARTITION"
        elif self.partition_type == 0x06:
            return "FAT-16"
        elif self.partition_type == 0x07:
            return "NTFS"
        elif self.partition_type == 0x0B:
            return "FAT-32 (CHS)"
        elif self.partition_type == 0x0C:
            return "FAT-32 (LBA)"
        elif self.partition_type == 0x0E:
            return "FAT-16 (LBA)"
        else:
            return "NOT-DECODED"

    def get_start_sector(self):
        return self.start_sector

    def get_partition_size(self):
        return self.partition_size
