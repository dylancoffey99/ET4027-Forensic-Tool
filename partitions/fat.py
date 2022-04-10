from partitions.partition import Partition


class FAT16(Partition):
    def __init__(self, image_path, start_sector, partition_size):
        super().__init__(0x06, start_sector, partition_size)
        self.image_path = image_path
        self.sectors_per_cluster = None
        self.fat_area_size = None
        self.root_dir_size = None
        self.cluster_two_sector = None
        self.deleted_files = []

    def get_fat_info(self):
        pass

    def print_fat_info(self):
        pass
