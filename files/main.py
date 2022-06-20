__winc_id__ = "ae539110d03e49ea8738fd413ac44ba8"
__human_name__ = "files"


from os.path import join
from os.path import exists
import os
import zipfile
"""
Student : Xitlalli Mayahuel van der Kroft Martínez
Datum : 20/06/2022
Note:
In gobal variables, files is added to cwd as
the terminal is worked from the assignments folder.
"""


def main():
    cachelist = cached_files()
    zip_path = join(path, 'files', 'data.zip')

    clean_cache()
    cache_zip(zip_path, full_path)
    print(find_password(cachelist))
    clean_cache()


# Global variables
path = os.getcwd()
new_dir = 'cache'
a = join(path, new_dir)
b = join(path, 'files', new_dir)
full_path = a if path.endswith('files') else b


# 1 -clean_cache: no arguments, creates an empty cache folder.
# If it already exists, it deletes everything in the cache folder.
def clean_cache():
    if exists(full_path) is False:
        os.mkdir(full_path)
    else:
        for file in os.listdir(full_path):
            file_path = join(full_path, file)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    os.rmdir(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))


# 2. cache_zip: takes a zip file path (str) and a cache dir path (str)
# The function then unpacks the indicated zip file into a clean cache folder.
def cache_zip(zip_path, cache_path):
    with zipfile.ZipFile(zip_path, 'r') as zipObj:
        zipObj.extractall(path=cache_path)


# 3. cached_files: no arguments, returns list of all the files in the cache.
def cached_files():
    list = []
    if exists(full_path):
        for file in os.listdir(full_path):
            file_path = join(full_path, file)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                list.append(os.path.abspath(file_path))
            elif os.path.isdir(file_path):
                continue
        return list
    if exists(full_path) is False:
        return ('no cache files')


# 4. find_password: takes the list of file paths from cached_files
# It reads the text in each one to see if the password is in there.
# Once found, find_password should return this password string.
def find_password(list):
    for item in list:
        file = open(file=item, mode='r')
        for line in file.readlines():
            if (('password' or 'pw' or 'Password' or 'PW')
               in line):
                password = line[line.find(' '):].strip()
                return password


if __name__ == "__main__":
    main()
