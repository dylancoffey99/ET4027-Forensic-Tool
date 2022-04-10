from partitions.partition import Partition


class NTFS(Partition):
    def __init__(self, image_path, start_sector, partition_size):
        super().__init__(0x07, start_sector, partition_size)
        self.image_path = image_path
        self.bytes_per_sector = None
        self.sectors_per_cluster = None
        self.mft_sector = None
        self.mft_attributes = []

    def get_ntfs_info(self):
        pass

    def print_ntfs_info(self):
        pass
