import os
import bin.display as display
from bin.find_images import image_finder
from bin.hasher_classes import exact_hasher, approx_image_hasher


def duplicate_finder(start_folder, to_match=None, exact=True):
    """
    Finds all images in the starting folder and recursively searches lower
    folders.

    Returns dictionary of arrays of filenames. Duplicate images will have
    there filenames in the same array.

    Picture extensions included: .jpg, .png, .jpeg

    if a picture path is given in to_match its hash and number of matches will
    also be returned. Assuming the picture is within the folder being checked.
    """

    if exact:
        hasher = exact_hasher()
    else:
        hasher = approx_image_hasher()

    image_file_paths = image_finder(start_folder)

    percent_thresh = 1
    for ind, file_path in enumerate(image_file_paths):
        hasher.add(file_path)

        if 100*ind/len(image_file_paths) >= percent_thresh:
            print(f'{percent_thresh}% of images hashed.')
            percent_thresh += 1

    pics_dict = hasher.get_hash_dict()

    # Check for match if its needed
    to_match_key = None
    if to_match is not None:
        to_match_key = hasher.find(to_match)

    if to_match_key is not None:
        return pics_dict, (to_match_key, len(pics_dict[to_match_key]))
    return pics_dict


def matches_filters(filenames, filters):
    """
    Return True if any filename contains any string from the filters list.
    Otherwise False.
    """
    for f in filters:
        for fname in filenames:
            if f in fname:
                return True
    return False


def remove_with_check(filename):
    check = input(f'File {filename} will be removed. Enter anything to cancel:')
    if len(check) == 0:
        os.remove(filename)
        return True
    return False


if __name__ == '__main__':
    # path = '.\\Test\\approx_match_test'
    path = 'D:\\Bryce\\Dropbox\\pictures'
    filter_ignored_files = ['copies', 'Animals']

    pics = duplicate_finder(path, exact=False)
    print('Done hashing')

    dups = []
    for p_list in pics.values():
        if len(p_list) > 1 and not matches_filters(p_list, filter_ignored_files):
            dups.append(p_list)

    print(f"Number of picture groups: {len(dups)}")

    removed = []
    for p_list in dups:
        # print all paths for duplicates
        print(p_list)
        # Show images to prove they are the same/similar
        display.show_image_list(p_list)

        """
        # delete the duplicated pictures with input...
        remove = input('Enter indices from list to remove separated by spaces (-1 to keep all): ')
        if remove != '-1':
            remove = [int(x) for x in remove.split(' ')]
            for i, p in enumerate(p_list):
                if i in remove:
                    r = remove_with_check(p)
                    if r:
                        removed.append(p)
        """
        """
        # mass picture import delete
        exists_outside = False
        for p in p_list:
            if 'mass picture import' not in p.split('\\'):
                exists_outside = True

        #print(p_list)

        if exists_outside:
            for p in p_list:
                if 'mass picture import' in p.split('\\'):
                    os.remove(p)
                    removed.append(p)
        """

    print(removed)

