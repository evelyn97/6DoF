# import the necessary packages
from collections import namedtuple
import numpy as np
import cv2
import json
from pprint import pprint


# define the `Detection` object
Detection = namedtuple("Detection", ["image_path", "img1", "img2"])


def intersection_over_union(boxA, boxB):
    # determine the (x, y)-coordinates of the intersection rectangle
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    # compute the area of intersection rectangle
    interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)

    # compute the area of both the prediction and ground-truth
    # rectangles
    boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
    boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)

    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = interArea / float(boxAArea + boxBArea - interArea)

    # return the intersection over union value
    return iou


if __name__ == '__main__':
    # define the list of example detections
    imgL1 = [91, 51, 91+266, 51+282]
    imgR1 = [403, 51, 403+266, 51+282]
    imgL2 = [-17, 0, -17+300, 0+360]
    imgR2 = [477,0, 477+300, 0+360]
    imgL3 = [72, 40, 72+307, 40+304]
    imgR3 = [381,40, 381+307, 40+304]
    x1 = np.average([91,-17,72])
    y1 = np.average([51, 0, 40])
    x2 = np.average([403, 477, 381])
    y2 = np.average([51, 0, 40])
    width = np.average([266, 300, 307])
    height = np.average([282, 360, 304])
    print(x1, " ", x2, " ", y1, " ", y2, " ", width, " ", height)
    iouL12 = intersection_over_union(imgL1, imgL2)
    iouR12 = intersection_over_union(imgR1, imgR2)
    print('12L: ', iouL12)
    print('12R: ', iouR12)
    iouL13 = intersection_over_union(imgL1, imgL3)
    iouR13 = intersection_over_union(imgR1, imgR3)
    print('13L: ', iouL13)
    print('13R: ', iouR13)
    iouL23 = intersection_over_union(imgL2, imgL3)
    iouR23 = intersection_over_union(imgR2, imgR3)
    print('23L: ', iouL23)
    print('23R: ', iouR23)
    examples = [
        Detection("image_0002.jpg", [39, 63, 203, 112], [54, 66, 198, 114]),
        Detection("image_0016.jpg", [49, 75, 203, 125], [42, 78, 186, 126]),
        Detection("image_0075.jpg", [31, 69, 201, 125], [18, 63, 235, 135]),
        Detection("image_0090.jpg", [50, 72, 197, 121], [54, 72, 198, 120]),
        Detection("image_0120.jpg", [35, 51, 196, 110], [36, 60, 180, 108])]

