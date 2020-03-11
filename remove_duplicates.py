import os
import hashlib
from collections import defaultdict

from PIL import Image

picture_extensions = set(['jpg', 'jpeg', '.png'])
BLOCKSIZE = 65536


def ext_finder(start_folder):
    """
    Finds all the extensions in the folder and recursively searches lower
    folders.
    """

    ext_list = set()
    num_checked = 0

    for root, dirs, files in os.walk(start_folder, topdown=False):
        for name in files:
            num_checked += 1
            ext = name.split('.')[-1].lower()
            ext_list.add(ext)

    print('{} files checked.'.format(num_checked))
    return ext_list


def duplicate_finder(start_folder):
    """
    Finds all images in the starting folder and recursively searches lower
    folders.

    Returns dictionary of arrays of filenames. Duplicate images will have
    there filenames in the same array.

    Picture extensions included: .jpg, .png, .jpeg
    """

    pics = defaultdict(list)
    num_checked = 0

    for root, dirs, files in os.walk(start_folder, topdown=False):
        for name in files:
            ext = name.split('.')[-1].lower()
            if ext in picture_extensions:
                num_checked += 1
                if num_checked % 100 == 0:
                    print(num_checked)

                file_path = os.path.join(root, name)

                hasher = hashlib.md5()

                with open(file_path, 'rb') as image_file:
                    buf = image_file.read(BLOCKSIZE)
                    while len(buf) > 0:
                        hasher.update(buf)
                        buf = image_file.read(BLOCKSIZE)

                    key = hasher.hexdigest()

                pics[key].append(file_path)

    print('{} pictures hashed.'.format(num_checked))
    return pics


if __name__ == '__main__':
    # print(ext_finder('D:\\Bryce\\Dropbox\\pictures'))

    # path = 'D:\\Bryce\\Dropbox\\pictures\\Animals\\Our pets\\Brownie'
    path = '.'
    pics = duplicate_finder(path)
    print('Done hashing')

    num_duplicated_pics = 0

    for p_list in pics.values():
        if len(p_list) > 1:
            num_duplicated_pics += 1

            # can show images to prove they are the same
            #for p in p_list:
            #    image = Image.open(p)
            #    image.show()

            print(p_list)
            keep = input('Enter indices to keep separated by spaces: ')
            if not keep == '-1':
                keep = [int(x) for x in keep.split(' ')]
                for i, p in enumerate(p_list):
                    if i not in keep:
                        os.remove(p)

    print(num_duplicated_pics)
