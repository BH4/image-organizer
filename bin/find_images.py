import os


picture_extensions = set(['jpg', 'jpeg', '.png'])
BLOCKSIZE = 65536


def image_finder(start_folder):
    """
    Finds all images in the starting folder and recursively searches lower
    folders.

    Returns dictionary of arrays of filenames. Duplicate images will have
    there filenames in the same array.

    Picture extensions included: .jpg, .png, .jpeg
    """

    pics = []
    num_checked = 0

    for root, dirs, files in os.walk(start_folder, topdown=False):
        for name in files:
            ext = name.split('.')[-1].lower()
            if ext in picture_extensions:
                num_checked += 1
                if num_checked % 100 == 0:
                    print(num_checked)

                file_path = os.path.join(root, name)

                pics.append(file_path)

    print('{} pictures found.'.format(num_checked))
    return pics
