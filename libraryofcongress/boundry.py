import cv2
import numpy as np
from cv2.ximgproc import createFastLineDetector
# import utils.visualization as vis
import os
import matplotlib.pyplot as plt
from skimage.data import data_dir
from skimage.util import img_as_ubyte
from skimage import io
from skimage.morphology import closing
from skimage.morphology import disk
from sklearn.linear_model import LinearRegression
from numpy import linalg
from pdb import set_trace as st
import numpy as np

def check(image, x, y):

    l = x == 0 or image[y][x - 1] != image[y][x]
    r = x >= len(image[0]) - 1 or image[y][x + 1] != image[y][x]
    u = y == 0 or image[y - 1][x] != image[y][x]
    d = y >= len(image) - 1 or image[y + 1][x] != image[y][x]
    # print(image, x , y, l, r, u, d)

    if l and r and u and d:
        # print("returned", x , y)
        return
    else:
        if not l:
            # print(x , y,"l")
            # image[y][x] = [80,255,255]  # to green
            # print(image[y][x])
            left.append(image[y][x])
            check(image, x - 1, y)
        if not r:
            # print(x , y,"r")
            # image[y][x] = [10,255,255] # to red
            right.append(image[y][x])
            check(image, x + 1, y)

        if not u:
            # print(x , y,"u")
            # image[y][x] = [180,255,255] # to blue
            up.append(image[y][x])
            check(image, x, y - 1)
        if not d:
            # print(x , y,"d")
            # image[y][x] = [40, 255, 255]  # to yellow
            down.append(image[y][x])
            check(image, x, y + 1)


def checkLoop(image):
    h, w = image.shape
    for x in range(w):
        for y in range(h):
        #     for dx in [-1,1]:
        #         for dy in [-1,1]:
        #             xx, yy=x+dx,y+dy
        #             if xx <0 or xx>=w or yy < 0 or yy >= h:
        #                 continue

            if (x - 1 <= 0) or (x + 1 >= w) or (y - 1 <= 0) or (y + 1 >= h): continue
            if image[y][x - 1] != image[y][x]:
                left.append([x,y])
            if image[y][x + 1] != image[y][x]:
                right.append([x,y])
            if image[y - 1][x] != image[y][x]:
                up.append([x,y])
            if image[y + 1][x] != image[y][x]:
                down.append([x,y])


def Close(image_path, ipath, iname):
    orig_pic = img_as_ubyte(io.imread(os.path.join(data_dir, image_path),
                                          as_gray=True))
    # fig, ax = plt.subplots()
    # ax.imshow(orig_phantom, cmap=plt.cm.gray)
    selem = disk(6)
    closed = closing(orig_pic, selem)
    # cv2.imshow("closing", closed)
    cv2.imwrite(ipath + iname + '_closing.jpg', closed)
    print('done')
    return closed


def line_direction(line_seg):
    return line_seg[2:4] - line_seg[:2]


def angle(dir1, dir2):
    c = dir1.T.dot(dir2)/linalg.norm(dir1)/linalg.norm(dir2)
    a = np.rad2deg(np.arccos(c))
    if a > 90:
        a = 180-a
    return a


def select_lines(lines, direction, degree_threshold):
    lines = lines.squeeze().astype(float)
    result = []
    for l in lines:
        if angle(line_direction(l), direction) < degree_threshold:
            result.append(l)
    return result


def pad_ones(points):
    return np.concatenate((points,np.ones((points.shape[0],1))), axis=1)

def line_eq_from_a_line_seg(line_seg):
    points = pad_ones(np.array([line_seg[:2], line_seg[2:]]))
    return np.cross(points[0,:], points[1,:])

def line_eq_from_line_segs(line_seg):
    points = np.concatenate(([line_seg[:,:2], line_seg[:,2:]]), axis=0)
    return fit_line_eq(points)

# get line_eq from points (not homogeneous)
# fit s.t., <(w,b), (x,y, 1)>=1
# so line_eq = <(wx, wy, b-1), (x,y,1)> = 0
def fit_line_eq(points):
    # convert to homogeneous coordinates
    X = pad_ones(points)
    y = np.ones(X.shape[0])
    cls = LinearRegression(fit_intercept = True)
    model = cls.fit(X,y)
    print(model.coef_, model.intercept_)
    return np.array((model.coef_, model.intercept_-1))


def lineDetect(im, name, imtodraw):

    fld = createFastLineDetector(_length_threshold=100, _distance_threshold=5, _do_merge=True,
                                 _canny_th1=10, _canny_th2=10)
    lines = fld.detect(im)
    im_vis = fld.drawSegments(imtodraw, lines)
    cv2.imshow("lines", im_vis)
    cv2.imwrite(name + '_test.png', im_vis)
    cv2.imwrite(name + '_test2.png', im)

    v_lines = select_lines(lines, np.array((0, 1)), 5)
    h_lines = select_lines(lines, np.array((1, 0)), 5)
    im_vis = fld.drawSegments(imtodraw, np.array([v_lines]).astype(np.float32))
    # cv2.imshow([im_vis])
    cv2.imwrite(name + '_test3.png', im_vis)

    hlines = np.array(h_lines)

    for l in hlines:
        line_eq = line_eq_from_a_line_seg(l)
        print("eq: ", line_eq)

if __name__ == '__main__':
    # name = '1s00030v'
    # name = '1s00056v'
    # name = '1s00104v'
    # find union

    path = '/Users/ying/documents/uw/Junior-quarter4/lab/library of congress/output_jpeg/'
    error = []
    for i in range(41, 12008):
        try:
            num = str(i)
            while len(num) < 5:
                num = '0' + num
            print(num)
            im = '1s' + num + 'v.jpg'
            print(im)
            name = im.strip(".jpg")
            print(path + name + '.jpg')
            im_original = cv2.imread(path + name + '.jpg')
            img1 = cv2.imread(path + name + '.jpg' + name + '_blurflood_hsv_1.jpg', 0)
            img2 = cv2.imread(path + name + '.jpg' + name + '_blurflood_hsv_2.jpg', 0)
            img_bwo = cv2.bitwise_or(img1, img2)
            cv2.imwrite(path + name + '_union.jpg', img_bwo)
            img_bwo = cv2.medianBlur(img_bwo, 5)
            cv2.imwrite(path + name + '_union_blur.jpg', img_bwo)

            # closing on the unioned picture
            closed_img = Close(path + name + '_union_blur.jpg', path, name)
            print(closed_img[1,1])

        # lineDetect(closed_img, name + '_ori', im_original)


            h, w = closed_img.shape
            midline = []
            for x in range(w):
                for y in range(h):
                    if closed_img[y, x] == 0:
                        midline.append(x)
            mid_x = np.average(midline)
            print(mid_x)


            from PIL import Image



            # crop it
            (newX, newY) = (0, 0)
            (newW, newH) = (int(mid_x), h)
            box_crop = (newX, newY, newX + newW, newY + newH)

                        # open source
            i = Image.open(path + name + '_closing.jpg')
            i2 = i.crop(box=box_crop)

            # create the new image, and paste it in
            # note that we're making it 300x300  and have the background set to white (255x3)
            i3 = Image.new('RGB', (w, h), (255, 255, 255))
            # paste it at an offset. if you put no offset or a box, i3 must match i2s dimensions
            i3.paste(i2)
            # save it
            i3.save(path + name + '_closing_left.jpg')

            # # crop it
            # (newX, newY) = (w - mid_x, 0)
            # (newW, newH) = (mid_x, h)
            # box_crop = (newX, newY, newX + newW, newY + newH)
            # i4 = i.crop(box=box_crop)

            # save it , just for testing
            i4 = Image.open(path + name + '_closing.jpg')

            # create the new image, and paste it in
            # note that we're making it 300x300  and have the background set to white (255x3)
            i5 = Image.new('RGB', (int(mid_x), h), (255, 255, 255))
            # paste it at an offset. if you put no offset or a box, i3 must match i2s dimensions
            i4.paste(i5)
            # save it
            i4.save(path + name + '_closing_right.jpg')

        except:
            error.append[im]
            with open(path + 'error.txt', 'a') as f:
                f.write(error)
            continue

    # h, w = img_bwo.shape
    # print("h", + h)
    # print("w", + w)
    # print(len(img_bwo))
    # print(img_bwo[50][125])
    # print(img_bwo[2, 10])
    # up = []
    # down = []
    # right = []
    # left = []
    # im_original = cv2.imread(name + '.jpg', 0)
    # lineDetect(img_bwo, name + '_ori', im_original)





    # check(img_bwo, 1, 1)

    # checkLoop(median)
    # upY = []
    # for p in up:
    #     upY.append(p[1])
    # upY.sort()
    # print(upY)


