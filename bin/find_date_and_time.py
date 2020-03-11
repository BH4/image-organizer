import os
from PIL import Image
from datetime import datetime


def check_exif_info(filename):
    """
    Returns datetime object representing the date the image was taken as well
    as the time stamp (ms since some date).
    """

    std_fmt = '%Y:%m:%d %H:%M:%S'
    tags = [36867,  # DateTimeOriginal
            36868,  # DateTimeDigitized
            306]    # DateTime
    exif = Image.open(filename)._getexif()

    if exif is None:
        return None

    for t in tags:
        dat = exif.get(t)

        if dat is not None:
            break

    if dat is None:
        return None

    T = datetime.strptime(dat, std_fmt)  # year, month, month day, hour, min, sec, day of week, day of year, is dst

    return T, int(T.timestamp())


def check_file_data(filename):
    # st_mtime = modified time
    # st_ctime = created time (after it was copied to current position)
    # st_atime = access time (now since I just accessed it)
    info = os.stat(filename)

    stamp = int(info.st_mtime)
    T = datetime.fromtimestamp(stamp)

    return T, stamp


def img_date(filename):
    exif_time = check_exif_info(filename)

    if exif_time is not None:
        return exif_time

    file_data_time = check_file_data(filename)
    return file_data_time


if __name__ == '__main__':
    #filename = '..\\Test\\0703170811b.jpg'
    filename = '..\\Test\\2019072795090646(1).jpg'

    print(img_date(filename))
