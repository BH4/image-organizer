import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def show_image(filename):
    img = mpimg.imread(filename)
    plt.imshow(img)
    plt.show()
