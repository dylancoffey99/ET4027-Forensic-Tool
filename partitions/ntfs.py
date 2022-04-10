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
        with open(self.image_path, "rb") as image:
            start_address = self.start_sector * 512
            image.seek(start_address + 0x0B)
            self.bytes_per_sector = int.from_bytes(image.read(2), "little")
            self.sectors_per_cluster = int.from_bytes(image.read(1), "little")
            image.seek(start_address + 0x30)
            logical_cluster = int.from_bytes(image.read(8), "little")
            self.mft_sector = self.start_sector + (logical_cluster * self.sectors_per_cluster)
            self.get_mft_attributes(image)

    def get_mft_attributes(self, image):
        mft_address = self.mft_sector * self.bytes_per_sector
        image.seek(mft_address + 0x14)
        first_offset = int.from_bytes(image.read(2), "little")
        first_attribute = self.get_mft_attribute(image, mft_address + first_offset)
        second_offset = first_offset + first_attribute.get("length")
        second_attribute = self.get_mft_attribute(image, mft_address + second_offset)
        self.mft_attributes = [first_attribute, second_attribute]

    def get_mft_attribute(self, image, offset):
        image.seek(offset)
        attribute_type = self.get_attribute_type(int.from_bytes(image.read(4), "little"))
        attribute_length = int.from_bytes(image.read(4), "little")
        return {"type": attribute_type, "length": attribute_length}

    @staticmethod
    def get_attribute_type(attribute_type):
        if attribute_type == 16:
            return "$STANDARD_INFORMATION"
        elif attribute_type == 32:
            return "$ATTRIBUTE_LIST"
        elif attribute_type == 48:
            return "$FILE_NAME"
        elif attribute_type == 64:
            return "$OBJECT_ID"
        elif attribute_type == 80:
            return "$SECURITY_DESCRIPTOR"
        elif attribute_type == 96:
            return "$VOLUME_NAME"
        elif attribute_type == 122:
            return "$VOLUME_INFORMATION"
        elif attribute_type == 128:
            return "$DATA"
        elif attribute_type == 144:
            return "$INDEX_ROOT"
        elif attribute_type == 160:
            return "$INDEX_ALLOCATION"
        elif attribute_type == 176:
            return "$BITMAP"
        elif attribute_type == 192:
            return "$REPARSE_POINT"
        elif attribute_type == 256:
            return "$LOGGED_UTILITY_STREAM"
        else:
            return "NOT-DEFINED"

    def print_ntfs_info(self):
        print("\n[Volume Information]")
        print(f"Bytes per sector = {self.bytes_per_sector}")
        print(f"Sectors per cluster = {self.sectors_per_cluster}")
        print(f"MFT Sector Address = {self.mft_sector}")
        for i, attribute in enumerate(self.mft_attributes):
            print(f"\n[Attribute {i + 1}]")
            print(f"Type = {attribute.get('type')}")
            print(f"Length (bytes) = {attribute.get('length')}")
