import cv2
import numpy as np
import os


def blurflood1(img, imgpath):
    median = cv2.medianBlur(img, 5)

    # cv2.imwrite(path + name + '_blur2.jpg', median)
    h, w, chn = median.shape
    # h, w, chn = img.shape
    # seed = (20, 40)
    seed = (49,60)
    mask = np.zeros((h + 2, w + 2), np.uint8)

    floodflags = 4
    floodflags |= cv2.FLOODFILL_MASK_ONLY
    floodflags |= (255 << 8)

    median = cv2.cvtColor(median, cv2.COLOR_BGR2HSV)
    # cv2.imwrite(name + "_h.jpg", median[:, :, 0])
    # cv2.imwrite(name + "_s.jpg", median[:, :, 1])
    # cv2.imwrite(name + "_v.jpg", median[:, :, 2])
    # num, im, mask, rect = cv2.floodFill(median, mask, seed, (255, 0, 0), (5, 8, 10), (5, 8, 10), floodflags)
    num, im, mask, rect = cv2.floodFill(median, mask, seed, (255, 0, 0), (10,) * 3, (10,) * 3, floodflags)

    #11383
    # num, im, mask, rect = cv2.floodFill(median, mask, seed, (255, 0, 0), (3,5,10), (3,5,10), floodflags)
    # cv2.imwrite(imgpath + name + "_blurflood_hsv_1.jpg", mask)
    return mask

def blurflood1_other(img, imgpath):
    median = cv2.medianBlur(img, 5)

    # cv2.imwrite(path + name + '_blur2.jpg', median)
    h, w, chn = median.shape
    h, w, chn = img.shape
    print(h, w)
    # seed = (20, 40)
    # seed = (14,520)
    seed = (999,6)
    mask = np.zeros((h + 2, w + 2), np.uint8)

    floodflags = 4
    floodflags |= cv2.FLOODFILL_MASK_ONLY
    floodflags |= (255 << 8)

    median = cv2.cvtColor(median, cv2.COLOR_BGR2HSV)
    # cv2.imwrite(name + "_h.jpg", median[:, :, 0])
    # cv2.imwrite(name + "_s.jpg", median[:, :, 1])
    # cv2.imwrite(name + "_v.jpg", median[:, :, 2])
    # num, im, mask, rect = cv2.floodFill(median, mask, seed, (255, 0, 0), (5, 8, 10), (5, 8, 10), floodflags)
    num, im, mask, rect = cv2.floodFill(median, mask, seed, (255, 0, 0), (10,) * 3, (10,) * 3, floodflags)

    #11383
    # num, im, mask, rect = cv2.floodFill(median, mask, seed, (255, 0, 0), (3,5,10), (3,5,10), floodflags)
    # cv2.imwrite(imgpath + name + "_blurflood_hsv_1.jpg", mask)
    return mask

def blurflood2(img, imgpath):
    median = cv2.medianBlur(img, 5)

    # cv2.imwrite(name + '_blur2.jpg', median)
    h, w, chn = median.shape
    # seed = (7, 96)
    seed = (5, 5)
    mask = np.zeros((h + 2, w + 2), np.uint8)

    floodflags = 8
    floodflags |= cv2.FLOODFILL_MASK_ONLY
    floodflags |= (255 << 8)

    median = cv2.cvtColor(median, cv2.COLOR_BGR2HSV)
    # cv2.imwrite(path + name + "_h.jpg", median[:, :, 0])
    # cv2.imwrite(path + name + "_s.jpg", median[:, :, 1])
    # cv2.imwrite(path + name + "_v.jpg", median[:, :, 2])
    # general:
    # num, im, mask, rect = cv2.floodFill(median, mask, seed, (255, 0, 0), (200,60,10), (200,60,10), floodflags)

    num, im, mask, rect = cv2.floodFill(median, mask, seed, (255, 0, 0), (250,100,5), (250,100,5), floodflags)
    cv2.imwrite(imgpath + name + "_blurflood_hsv_2.jpg", mask)


if __name__ == '__main__':

    def imshow(img):
        cv2.imshow('img', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    path = '/Users/ying/documents/uw/Junior-quarter4/lab/library of congress/output_jpeg/'

    # for i in range(11256, 12008):
    i = 11383
    num = str(i)
    while len(num) < 5:
        num = '0' + num
    print(num)
    im = '1s' + num + 'v.jpg'

    name = im.strip(".jpg")
    image_path = path + im
    print(image_path)
    # try:
    img = cv2.imread(image_path)

    im1 = blurflood1(img, image_path)
    im2 = blurflood1_other(img, image_path)
    img_blur = cv2.bitwise_or(im1, im2)
    cv2.imwrite(image_path + name + "_blurflood_hsv_1.jpg", img_blur)
    blurflood2(img, image_path)
    # except:
    #     continue
