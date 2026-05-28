import cv2
import matplotlib.pyplot as plt
import cvlib as cv
from cvlib.object_detection import draw_bbox


im = cv2.imread('test/oo.jpg')
#im = cv2.imread('D:\\Bryce\\Dropbox\\pictures\\Trips and Events\\Outdoor activities\\Camping\\Kickapoo State Recreation Area, IL May 2015\\20150527_151657.jpg')


bbox, label, conf = cv.detect_common_objects(im)

print(bbox, label, conf)

output_image = draw_bbox(im, bbox, label, conf)

# OpenCV uses BGR but pyplot expects RGB so must convert image.
RGB_img = cv2.cvtColor(output_image, cv2.COLOR_BGR2RGB)
plt.imshow(RGB_img)
plt.show()
