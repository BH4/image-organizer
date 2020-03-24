import numpy as np
from sklearn.neighbors.kde import KernelDensity
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt

from datetime import datetime

from bin.find_images import image_finder
from bin.find_date import img_date


def separators(data):
    """
    Find points to separate data into groups using kernal density estimation
    """
    data = np.array(data)

    kde = KernelDensity(kernel='gaussian', bandwidth=1).fit(data.reshape(-1, 1))
    x_axis = np.linspace(min(data), max(data), 1000)
    e = kde.score_samples(x_axis.reshape(-1, 1))

    plt.plot(x_axis, e)
    plt.show()

    mi = argrelextrema(e, np.less)[0]
    minima = x_axis[mi]

    return minima


def view_image(filename):
    4


if __name__ == '__main__':
    # path = '.'
    path = 'D:\\Bryce\\Dropbox\\pictures'
    filenames = image_finder(path)

    images = []
    for f in filenames:
        date, ms_date = img_date(f)
        images.append((ms_date, f))

    images.sort()

    time_data, filenames = zip(*images)
    sep = separators(time_data)

    print([datetime.fromtimestamp(stamp) for stamp in sep])
    #print(datetime.now())

    # Show images on each side of each separator date to see why they are separated.
    # also show their dates to see how far they are from the separator.

    # note that the number of points on the x axis as well as the 'bandwidth' affect the separators.
