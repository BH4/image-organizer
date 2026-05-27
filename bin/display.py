from PIL import Image
import matplotlib
import matplotlib.pyplot as plt


def show_image(filename):
    image = Image.open(filename)
    image.show()


def text_wrap(text, width=20):
    new_text = ''
    for ind, c in enumerate(text):
        new_text += c
        if (ind+1) % width == 0:
            new_text += '\n'
    return new_text


def show_image_list(filenames, figsize_per_image=(4, 4)):
    n = len(filenames)
    if n > 8:
        print('Too many to display at once.')
        return

    num_rows = ((n-1) // 4) + 1
    num_cols = min(n, 4)

    font = {'size': 6}
    matplotlib.rc('font', **font)

    fig, axes = plt.subplots(
        num_rows,
        num_cols,
        figsize=(figsize_per_image[0] * num_cols, figsize_per_image[1] * num_rows),
    )

    if n == 1:
        axes = [axes]
    else:
        axes = axes.ravel()

    for ax, fname in zip(axes, filenames):
        img = Image.open(fname)
        ax.imshow(img)
        ax.set_title(text_wrap(fname, width=35))
        ax.axis("off")

    for ax in axes[n:]:
        ax.axis("off")

    plt.tight_layout()
    plt.show()
