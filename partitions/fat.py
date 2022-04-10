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
        with open(self.image_path, "rb") as image:
            start_address = self.start_sector * 512
            image.seek(start_address + 0x0B)
            bytes_per_sector = int.from_bytes(image.read(2), "little")
            self.sectors_per_cluster = int.from_bytes(image.read(1), "little")
            reserved_area_size = int.from_bytes(image.read(2), "little")
            fat_copies = int.from_bytes(image.read(1), "little")
            max_root_dir_entries = int.from_bytes(image.read(2), "little")
            image.seek(start_address + 0x16)
            fat_sector_size = int.from_bytes(image.read(2), "little")
            self.fat_area_size = fat_copies * fat_sector_size
            self.root_dir_size = int((max_root_dir_entries * 32) / bytes_per_sector)
            root_dir_sector = self.start_sector + reserved_area_size + self.fat_area_size
            self.cluster_two_sector = root_dir_sector + self.root_dir_size
            self.get_deleted_files(image, root_dir_sector, max_root_dir_entries, bytes_per_sector)

    def get_deleted_files(self, image, root_dir_sector, max_root_dir_entries, bytes_per_sector):
        root_dir_entry = root_dir_sector * bytes_per_sector
        for _ in range(max_root_dir_entries):
            image.seek(root_dir_entry)
            file_name = image.read(11)
            if file_name[0] == 0xE5:
                file_name = str(file_name, "ansi").replace(" ", "").replace("TXT", ".TXT")
                image.seek(root_dir_entry + 0x1A)
                start_cluster = int.from_bytes(image.read(2), "little")
                file_size = int.from_bytes(image.read(4), "little")
                cluster_sector = (self.cluster_two_sector + (start_cluster - 2) *
                                  self.sectors_per_cluster) * bytes_per_sector
                image.seek(cluster_sector)
                file_content = str(image.read(16), "ansi")
                deleted_file = {"name": file_name, "start_cluster": start_cluster,
                                "size": file_size, "content": file_content}
                self.deleted_files.append(deleted_file)
            root_dir_entry += 0x20

    def print_fat_info(self):
        print("\n[Volume Information]")
        print(f"Sectors per cluster = {self.sectors_per_cluster}")
        print(f"FAT Area Size (sectors) = {self.fat_area_size}")
        print(f"Root Directory Size (sectors) = {self.root_dir_size}")
        print(f"Cluster #2 Sector Address = {self.cluster_two_sector}")
        for i, file in enumerate(self.deleted_files):
            print(f"\n[Deleted File {i + 1}]")
            print(f"File Name = {file.get('name')}")
            print(f"Start Cluster = {file.get('start_cluster')}")
            print(f"File Size (bytes) = {file.get('size')}")
            print(f"File Content (first 16 characters):\n~~~~~~~~ Content Start ~~~~~~~~"
                  f"\n{file.get('content')}\n~~~~~~~~~ Content End ~~~~~~~~~")
