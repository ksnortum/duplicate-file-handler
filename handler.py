import sys
import os
import argparse
import hashlib


class DuplicateFiles:

    @staticmethod
    def get_root() -> str:
        parser = argparse.ArgumentParser(description="List files in a directory")
        parser.add_argument("directory", nargs="?", default=False)
        args = parser.parse_args()

        if not args.directory:
            print("Directory is not specified")
            return ""

        return args.directory

    @staticmethod
    def get_sort_by() -> int:
        print("\nSize sorting options:")
        print("1. Descending")
        print("2. Ascending")

        option = 0
        there_is_more_to_do = True
        while there_is_more_to_do:
            print("\nEnter a sorting option:")
            option = int(input())

            if option == 1 or option == 2:
                there_is_more_to_do = False
            else:
                print("\nWrong option")

        return option

    @staticmethod
    def get_same_size_files(root_directory: str, file_format: str) -> dict:
        """ Returns a dictionary: { file_size: [ file_path ] } """
        all_files = {}

        for root, dirs, files in os.walk(root_directory):
            for name in files:
                _, ext = os.path.splitext(name)
                if not file_format or file_format == ext[1:]:
                    path = os.path.join(root, name)
                    file_size = os.path.getsize(path)
                    if file_size not in all_files:
                        all_files[file_size] = []
                    all_files[file_size].append(path)

        same_size_files = {}
        for key in all_files:
            if len(all_files[key]) >= 2:
                same_size_files[key] = all_files[key]

        return same_size_files

    @staticmethod
    def search_for_duplicates() -> bool:
        ans = ""
        while ans not in ["yes", "no"]:
            print("\nCheck for duplicates?")
            ans = input()

        return ans == 'yes'

    def get_same_hash_files(self, same_size_files: dict) -> dict:
        """
        In: dictionary { file_size: [ file_path ] }
        Returns a dictionary { file_size: { hash: [ file_name ] } }
        """
        same_hash_files = {}
        for file_size in same_size_files.keys():
            file_names_by_hash = {}
            for file_name in same_size_files[file_size]:
                h = hashlib.md5()
                h.update(self.get_file_in_bytes(file_name))
                hex_hash = h.hexdigest()
                if hex_hash not in file_names_by_hash:
                    file_names_by_hash[hex_hash] = []
                file_names_by_hash[hex_hash].append(file_name)
            same_hash_files[file_size] = file_names_by_hash

        return same_hash_files

    @staticmethod
    def get_file_in_bytes(file_name: str) -> bytes:
        file_bytes = bytes()
        with open(file_name, 'rb') as file_d:
            file_bytes = file_d.read()

        return file_bytes

    def main(self):
        root_directory = self.get_root()
        if not root_directory:
            sys.exit(1)

        file_format = input("Enter file format:\n")
        sort_by = self.get_sort_by()
        same_size_files = self.get_same_size_files(root_directory, file_format)

        if sort_by == 2:
            sorted_keys = sorted(same_size_files.keys())
        else:
            sorted_keys = sorted(same_size_files.keys(), reverse=True)

        for key in sorted_keys:
            print()
            print(key, "bytes")
            for path in same_size_files[key]:
                print(path)

        if not self.search_for_duplicates():
            sys.exit(2)

        same_hash_files = self.get_same_hash_files(same_size_files)
        file_number = 1

        for key in sorted_keys:
            print()
            print(key, "bytes")
            for hex_hash in same_hash_files[key]:
                if len(same_hash_files[key][hex_hash]) >= 2:
                    print(f'Hash: {hex_hash}')
                    for file_name in same_hash_files[key][hex_hash]:
                        print(f'{file_number}. {file_name}')
                        file_number += 1


if __name__ == "__main__":
    DuplicateFiles().main()
