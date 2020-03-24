import os
from PIL import Image
from datetime import datetime


def check_exif_info(filename):
    """
    Returns datetime object representing the date the image was taken as well
    as the time stamp (ms since some date).
    """

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

    dat = dat.split(' ')[0]
    dat = dat.replace('.', ':')
    vals = dat.split(':')
    if len(vals[0]) == 4:
        #std_fmt = '%Y:%m:%d %H:%M:%S'
        std_fmt = '%Y:%m:%d'
    else:
        std_fmt = '%m:%d:%Y'

    T = datetime.strptime(dat, std_fmt)  # year, month, month day, hour, min, sec, day of week, day of year, is dst
    T = T.replace(hour=0, minute=0, second=0, microsecond=0)

    return T, int(T.timestamp())


def check_file_data(filename):
    # st_mtime = modified time
    # st_ctime = created time (after it was copied to current position)
    # st_atime = access time (now since I just accessed it)
    info = os.stat(filename)

    stamp = int(info.st_mtime)
    T = datetime.fromtimestamp(stamp)
    if T.year == 1970:
        stamp = int(info.st_ctime)
        T = datetime.fromtimestamp(stamp)

    T = T.replace(hour=0, minute=0, second=0, microsecond=0)

    return T, int(T.timestamp())


def img_date(filename):
    #exif_time = check_exif_info(filename)

    #if exif_time is not None:
    #    return exif_time

    file_data_time = check_file_data(filename)
    return file_data_time


def stamp_to_date(stamp):
    return datetime.fromtimestamp(stamp)


if __name__ == '__main__':
    #filename = '..\\Test\\0703170811b.jpg'
    #filename = '..\\Test\\2019072795090646(1).jpg'
    filename = 'D:\\Bryce\\Dropbox\\pictures\\Mere&me\\Me pictures\\mass import 465.jpg'  # no modified time but has date created

    print(img_date(filename))
