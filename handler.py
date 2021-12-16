import sys
import os
import argparse
import hashlib


class DuplicateFiles:

    def __init__(self):
        self.root_directory = ""
        self.file_format = ""
        self.sort_by = 0
        self.same_size_files = {}
        self.sorted_keys = []
        self.same_hash_files = {}
        self.file_names_by_number = {}
        self.file_numbers = []

    def get_root(self):
        parser = argparse.ArgumentParser(description="List files in a directory")
        parser.add_argument("directory", nargs="?", default=False)
        args = parser.parse_args()

        if not args.directory:
            print("Directory is not specified")
            sys.exit(1)

        self.root_directory = args.directory

    def get_file_format(self):
        self.file_format = input("Enter file format:\n")

    def get_sort_by(self):
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

        self.sort_by = option

    def get_same_size_files(self):
        """ same_size_files = dictionary { file_size: [ file_path ] } """
        all_files = {}
        for root, dirs, files in os.walk(self.root_directory):
            for name in files:
                _, ext = os.path.splitext(name)
                if not self.file_format or self.file_format == ext[1:]:
                    path = os.path.join(root, name)
                    file_size = os.path.getsize(path)
                    if file_size not in all_files:
                        all_files[file_size] = []
                    all_files[file_size].append(path)

        for key in all_files:
            if len(all_files[key]) >= 2:
                self.same_size_files[key] = all_files[key]

    def sort_keys(self):
        if self.sort_by == 2:
            self.sorted_keys = sorted(self.same_size_files.keys())
        else:
            self.sorted_keys = sorted(self.same_size_files.keys(), reverse=True)

    def print_same_size_files(self):
        for key in self.sorted_keys:
            print()
            print(key, "bytes")
            for path in self.same_size_files[key]:
                print(path)

    def ask_search_for_duplicates(self):
        self.get_yes_no_answer("Check for duplicates?")

    def ask_delete_files(self):
        self.get_yes_no_answer("Delete files?", "Wrong option")

    @staticmethod
    def get_yes_no_answer(prompt: str, error: str = ""):
        ans = ""
        while ans not in ["yes", "no"]:
            print()
            print(prompt)
            ans = input()

            if ans == 'no':
                sys.exit(2)

            if ans != "yes" and error:
                print(error)

    def get_same_hash_files(self):
        """ same_hash_files = dictionary { file_size: { hash: [ file_name ] } } """

        for file_size in self.same_size_files.keys():
            file_names_by_hash = {}
            for file_name in self.same_size_files[file_size]:
                h = hashlib.md5()
                h.update(self.get_file_in_bytes(file_name))
                hex_hash = h.hexdigest()
                if hex_hash not in file_names_by_hash:
                    file_names_by_hash[hex_hash] = []
                file_names_by_hash[hex_hash].append(file_name)
            self.same_hash_files[file_size] = file_names_by_hash

    @staticmethod
    def get_file_in_bytes(file_name: str) -> bytes:
        file_bytes = bytes()
        with open(file_name, 'rb') as file_d:
            file_bytes = file_d.read()

        return file_bytes

    def print_same_hash_files(self):
        """ Build file_names_by_number: { file_number: { file_name: name, file_size: size } } """
        file_number = 1
        for file_size in self.sorted_keys:
            print()
            print(file_size, "bytes")
            for hex_hash in self.same_hash_files[file_size]:
                if len(self.same_hash_files[file_size][hex_hash]) >= 2:
                    print(f'Hash: {hex_hash}')
                    for file_name in self.same_hash_files[file_size][hex_hash]:
                        print(f'{file_number}. {file_name}')
                        elem = {"file_name": file_name, "file_size": file_size}
                        self.file_names_by_number[file_number] = elem
                        file_number += 1

    def get_file_numbers(self):
        format_is_bad = True
        while format_is_bad:
            print()
            print("Enter file numbers to delete:")
            ans = input()
            try:
                self.file_numbers = list(map(int, ans.split()))
                if any([num > len(self.file_names_by_number) for num in self.file_numbers]):
                    raise ValueError
                format_is_bad = False
            except ValueError:
                print("Wrong format")

    def delete_duplicate_files(self):
        total_freed_space = 0
        for file_number in self.file_numbers:
            os.remove(self.file_names_by_number[file_number]["file_name"])
            total_freed_space += self.file_names_by_number[file_number]["file_size"]

        print(f"\nTotal freed up space: {total_freed_space} bytes")

    def main(self):
        self.get_root()
        self.get_file_format()
        self.get_sort_by()
        self.get_same_size_files()
        self.sort_keys()
        self.print_same_size_files()
        self.ask_search_for_duplicates()
        self.get_same_hash_files()
        self.print_same_hash_files()
        self.ask_delete_files()
        self.get_file_numbers()
        self.delete_duplicate_files()


if __name__ == "__main__":
    DuplicateFiles().main()
