# import the necessary packages
import numpy as np
import shutil
import json
import os
from subprocess import check_output

PATH = '/projects/grail/6DOFnb/NYPL_new/'

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

def mean(imgs):
    x1_cons = []
    x2_cons = []
    y1_cons = []
    y2_cons = []
    width_cons = []
    height_cons = []
    for img in imgs:
        meta_file = PATH + "meta/meta_" + str(img) + ".json"
        meta = json.loads(open(meta_file).read())
        x1_cons.append(meta['x1'])
        x2_cons.append(meta['x2'])
        y1_cons.append(meta['y1'])
        y2_cons.append(meta['y2'])
        width_cons.append(meta['width'])
        height_cons.append(meta['height'])
    x1 = np.average(x1_cons)
    x2 = np.average(x2_cons)
    y1 = np.average(y1_cons)
    y2 = np.average(y2_cons)
    width = np.average(width_cons)
    height = np.average(height_cons)
    return x1, x2, y1, y2, width, height


def iou(img1, img2):
    meta_file1 = PATH + "meta/meta_" + str(img1) + ".json"
    meta1 = json.loads(open(meta_file1).read())
    imgL1 = [meta1['x1'], meta1['y1'], meta1['x1'] + meta1['width'], meta1['y1'] + meta1['height']]
    imgR1 = [meta1['x2'], meta1['y2'], meta1['x2'] + meta1['width'], meta1['y2'] + meta1['height']]
    meta_file2 = PATH + "meta/meta_" + str(img2) + ".json"
    meta2 = json.loads(open(meta_file2).read())
    imgL2 = [meta2['x1'], meta2['y1'], meta2['x1'] + meta2['width'], meta2['y1'] + meta2['height']]
    imgR2 = [meta2['x2'], meta2['y2'], meta2['x2'] + meta2['width'], meta2['y2'] + meta2['height']]
    iouL = intersection_over_union(imgL1, imgL2)
    iouR = intersection_over_union(imgR1, imgR2)
    return iouL + iouR


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print 'Error: Creating directory. ', +  directory


if __name__ == '__main__':
    id = 1000
    filename = PATH + '/url/urlmap_' + str(id) + '.json'
    json_data = open(filename).read()
    data = json.loads(json_data)
    for key in data.keys():
        imgs = data.get(key)
        if len(imgs) >= 2:
            consDir = PATH + 'cons/'
            createFolder(consDir)
            if len(imgs) == 2:
                x1, x2, y1, y2, width, height = mean(imgs)
                id = imgs[0]
            else:
                iou_score = {}
                for img1 in imgs:
                    score = 0
                    for img2 in imgs:
                        score += iou(img1, img2)
                    iou_score[score] = img1
                sorted_keys = sorted(iou_score, key=iou_score.get, reverse=True)
                img_1 = iou_score[sorted_keys[0]]
                img_2 = iou_score[sorted_keys[1]]
                x1, x2, y1, y2, width, height = mean(imgs)
                id = imgs[0]

            idDir = PATH + 'cons/' + str(id)
            createFolder(idDir)
            command = '/projects/grail/6DOF/dataset_NYPL/6DoF/server/consensus.rb'
            exist = 1

            try:
                url = check_output([command, str(id), str(x1), str(x2), str(y1), str(y2), str(width), str(height)])
            except:
                exist = 0

            if exist == 1:
                remove1 = PATH + str(id) + '.jpg'
                if os.path.exists(remove1):
                    os.remove(remove1)
                remove2 = PATH + str(id) + '_cropped.tif'
                if os.path.exists(remove2):
                    os.remove(remove2)
                remove3 = PATH + str(id) + '_gif.jpg'
                if os.path.exists(remove3):
                    os.remove(remove3)

                for img in imgs:
                    remove = PATH + 'cropped/' + str(img)
                    shutil.rmtree(remove)




    # filename = 'meta_21791.json'
    # json_data = open(filename).read()
    # data = json.loads(json_data)
    # print(data['x1'] )


    # define the list of example detections
    # imgL1 = [91, 51, 91+266, 51+282]
    # imgR1 = [403, 51, 403+266, 51+282]
    # imgL2 = [-17, 0, -17+300, 0+360]
    # imgR2 = [477,0, 477+300, 0+360]
    # imgL3 = [72, 40, 72+307, 40+304]
    # imgR3 = [381,40, 381+307, 40+304]
    # x1 = np.average([91,-17,72])
    # y1 = np.average([51, 0, 40])
    # x2 = np.average([403, 477, 381])
    # y2 = np.average([51, 0, 40])
    # width = np.average([266, 300, 307])
    # height = np.average([282, 360, 304])
    # print(x1, " ", x2, " ", y1, " ", y2, " ", width, " ", height)
    # iouL12 = intersection_over_union(imgL1, imgL2)
    # iouR12 = intersection_over_union(imgR1, imgR2)
    # print('12L: ', iouL12)
    # print('12R: ', iouR12)
    # iouL13 = intersection_over_union(imgL1, imgL3)
    # iouR13 = intersection_over_union(imgR1, imgR3)
    # print('13L: ', iouL13)
    # print('13R: ', iouR13)
    # iouL23 = intersection_over_union(imgL2, imgL3)
    # iouR23 = intersection_over_union(imgR2, imgR3)
    # print('23L: ', iouL23)
    # print('23R: ', iouR23)




