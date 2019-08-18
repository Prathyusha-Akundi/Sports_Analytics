import cv2
import numpy as np
import time
from scipy import stats
from copy import deepcopy
from imageOperatives import *
from ground_color import *
from DLdata import *
from lines import *


'''
  Req: This code requires sklearn to run.
  The code accepts image containing bw data of white lines extracted from parent image.
  Initially, the code scans the image sequentially using a window, and if the data in window seems likely to be a line,
  regression is applied on the window. If the reg score is high enough, the line segment is considered.
  Using this part of line, find_right_end_point and find_left_end_point are called which return the right and the left end points of the complete line.
  Once the end points are retrieved, the sequential search continues till the end of image is reached.
  coords contains two points on the line in the form [[y1,x1],[y2,x2]]
 '''

def find_right_end_point(image, sx, sy, edge, m, isVerticalLine):
    temp_img = np.array(image)
    window = image[int(sx-0.5*edge): int(sx+0.5*edge), int(sy-0.5*edge): int(sy+0.5*edge)]  # to get the inital mask of line
    init_area = np.sum(window)
    mask = deepcopy(window)
    mask[mask!=0] = 1
    mask = cv2.dilate(mask, (np.ones((10,10), np.uint8)))     # mask is dilated because the line we aim to find is generally slightly curved, if not dilated we lose the line eventually
    break_encountered = 0       # storing if a break in the line is encountered.

    while True:
        if(int(sx-0.5*edge) < 0 or int(sx+0.5*edge) > 1080+edge or int(sy-0.5*edge) < 0 or int(sy+0.5*edge) > 1920):
            break

        completeWindow = image[int(sx-0.5*edge): int(sx+0.5*edge), int(sy-0.5*edge): int(sy+0.5*edge)][:60,:60] #to ensure (edge*edge) shape, int() rounds to edge+1 sometimes
        mask = mask[:completeWindow.shape[0], :]
        window = np.multiply(completeWindow, mask)
        area = np.sum(window)
        # print(area)
        # cv2.namedWindow('hmm', cv2.WINDOW_NORMAL)
        # cv2.resizeWindow('hmm', 1280,720)
        # cv2.rectangle(temp_img, (int(sy-0.5*edge), int(sx-0.5*edge)), (int(sy+0.5*edge), int(sx+0.5*edge)), 255, 2)
        # cv2.imshow('hmm', temp_img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()


        if area < init_area/7:
            if(break_encountered == 0):
                # y is the horizontal coordinate in the image and x is the vertical
                if(m<1):
                    sy += edge
                    sx += int(edge*m)
                else:
                    sy += int(edge/m)
                    sx += edge
                break_encountered = 1
                continue
            else:
                break
        break_encountered = 0

        last_box = window
        x_coord = int(sx - 0.5*edge)
        y_coord = int(sy - 0.5*edge)

        if(m<1):
            sy += edge
            sx += int(edge*m)
        else:
            sy += int(edge/m)
            sx += edge

    if isVerticalLine == 0:
        divs = 3
        r_value_min = 0
        final_box = last_box
        for i in range(divs):
            last_box_copy = last_box[:, :last_box.shape[1]*(i+1)//divs]
            points = np.array(np.argwhere([last_box_copy != 0]))[:,1:3]
            if len(points) != 0:
                x = points[:,0]
                y = points[:,1]
                _, _, r_value, _, _ = stats.linregress(y, x)
                if abs(r_value) > r_value_min:
                    final_box = last_box_copy
                    r_value_min = abs(r_value)
    else:
        final_box = last_box
        # print(np.nonzero(final_box))
        return x_coord+np.nonzero(final_box)[0][-1], y_coord+int(np.average(np.nonzero(final_box[np.nonzero(final_box)[0][-1], :])[0]))

    #finding end point of the line in the box.
    final_box = np.fliplr(final_box)
    nonzero = np.nonzero(final_box.T)

    return x_coord+nonzero[1][0], y_coord+final_box.shape[1]-nonzero[0][0]


# similar to find_right_end_point
def find_left_end_point(image, sx, sy, edge, m, isVerticalLine):
    window = image[int(sx-0.5*edge): int(sx+0.5*edge), int(sy-0.5*edge): int(sy+0.5*edge)]
    init_area = np.sum(window)
    mask = deepcopy(window)
    mask[mask!=0] = 1
    mask = cv2.dilate(mask, (np.ones((10,10), np.uint8)))
    break_encountered = 0

    while True:
        if(int(sx-0.5*edge) < 0 or int(sx+0.5*edge) > 1080+edge or int(sy-0.5*edge) < 0 or int(sy+0.5*edge) > 1920):
            break

        completeWindow = image[int(sx-0.5*edge): int(sx+0.5*edge), int(sy-0.5*edge): int(sy+0.5*edge)][:60,:60]
        mask = mask[:completeWindow.shape[0], :]
        window = np.multiply(completeWindow, mask)
        area = np.sum(window)

        if area < init_area/7:
            if(break_encountered == 0):
                if(m<1):
                    sy -= edge
                    sx -= int(edge*m)
                else:
                    sy -= int(edge/m)
                    sx -= edge
                break_encountered = 1
                continue
            else:
                break

        break_encountered = 0

        last_box = window
        x_coord = int(sx - 0.5*edge)
        y_coord = int(sy - 0.5*edge)

        if(m<1):
            sy -= edge
            sx -= int(edge*m)
        else:
            sy -= int(edge/m)
            sx -= edge

    if isVerticalLine == 0:
        divs = 3
        r_value_min = 0
        final_box = last_box
        for i in range(divs):
            last_box_copy = last_box[:, last_box.shape[1]*i//divs:]
            points = np.array(np.argwhere([last_box_copy != 0]))[:,1:3]
            if len(points) != 0:
                x = points[:,0]
                y = points[:,1]
                _, _, r_value, _, _ = stats.linregress(y, x)
                if abs(r_value) > r_value_min:
                    final_box = last_box_copy
                    r_value_min = abs(r_value)
    else:
        final_box = last_box
        return x_coord+np.nonzero(final_box)[0][0], y_coord+int(np.average(np.nonzero(final_box[np.nonzero(final_box)[0][0], :])[0]))

    nonzero = np.nonzero(final_box.T)
    return x_coord+nonzero[1][0], y_coord+nonzero[0][0]+(edge-final_box.shape[1])


def getEndPoints(img, playerMask):
    filter_size = 60
    lines = np.zeros(img.shape)
    playerMask = (1-playerMask)*255
    playerMask[img != 0] = 255
    # we use this as a canvas to print the complete lines we find from regression.
    # once a line has been found, we then do not consider any other window that containes that line, to reduce computation.
    x_min = np.array(np.where(img == 255))[:,0].T
    x_min = x_min[0]

    coords = []
    # temp_img = np.array(img)
    # temp_img = np.squeeze(np.stack((temp_img,) * 3, -1))

    for i in range(int(img.shape[0]/filter_size)):
        if (i+1)*filter_size < x_min:
            continue
        for j in range(int(img.shape[1]/filter_size)):
            # break
            edge = filter_size
            window = img[i*edge:(i+1)*edge, j*edge:(j+1)*edge]

            area = np.sum(window)/255
            ratio = area/(filter_size**2)   # The area of white pixels upon bounding box area. A low value suggests that the box contains a line.
            # print(ratio)
            # break
            # cv2.rectangle(temp_img, (j*edge, i*edge), ((j+1)*edge, (i+1)*edge), (0,0,255), 2)
            if(area > 60 and ratio < 0.30):
                if((np.sum(lines[i*edge:(i+1)*edge, j*edge:(j+1)*edge]) == 0)):     # This ensures that the same line isn't operated on twice
                    points = np.array(np.argwhere([window != 0])[::4])[:,1:3]
                    # [::4] is to take every fourth point only. Reducing number of points makes regression faster without any considerable accuracy loss.

                    x = points[:,0] + i*edge
                    y = points[:,1] + j*edge
                    slope, intercept, r_value, p_value, std_error = stats.linregress(y, x)
                    # print(r_value, std_error)
                    std_error = 1
                    if(abs(r_value) > 0.88 or (std_error > 0.5 and ((np.std(x)/np.std(y) > 3) or (np.std(x)/np.std(y) < 1/3)))):
                        if(abs(r_value) < 0.88):
                            if(np.std(x)/np.std(y) > 3):
                                slope = np.inf
                                isVerticalLine = 1
                            else:
                                lPts, rPts = np.where(window[:,0] == 255), np.where(window[:,-1] == 255)
                                if np.sum(lPts) == 0 or np.sum(rPts) == 0:
                                    slope = 0
                                else:
                                    l, r = np.average(lPts), np.average(rPts)
                                    slope = (r-l)/edge
                                isVerticalLine = 0
                        else:
                            isVerticalLine = 0
                        # print(slope)
                        # print(reg.coef_, reg.intercept_)
                        # cv2.rectangle(temp_img, (j*edge, i*edge), ((j+1)*edge, (i+1)*edge), (0,255,0), 2)
                        x1, y1 = find_right_end_point(img if isVerticalLine == 0 else playerMask, (i+0.5)*edge, (j+0.5)*edge, edge, slope, isVerticalLine)
                        x2, y2 = find_left_end_point(img if isVerticalLine == 0 else playerMask, (i+0.5)*edge, (j+0.5)*edge, edge, slope, isVerticalLine)
                        coords.append([[x1,y1], [x2,y2]])
                        cv2.line(lines, (y1,x1), (y2,x2),255,10)

    # cv2.namedWindow('hmm',cv2.WINDOW_NORMAL)
    # cv2.resizeWindow('hmm', 1280,720)
    # cv2.imshow('hmm', temp_img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # print("COORDS : ",coords)
    return np.array(coords)

###############

if __name__ == '__main__':
    time_init = time.time()
    from random import randint
    import os
    # os.chdir('..')
    imgDir = './../../Videos/imgs6/'
    filename = '73.jpg'
    img = cv2.imread(imgDir+filename)
    lineMask = img
    #ck 7 pm 3 cd 8
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # # print("["+str(rangeH)+"],["+str(rangeS)+"],["+str(rangeV)+"]")
    # # groundColorMask = rangeToMask(img,[rangeH],[rangeS],[rangeV])
    # groundColorMask = rangeToMask(img,[[0.26666666666666666, 0.35]],[[0.3686274509803922, 0.6627450980392157]],[[0.615686274509804, 0.8313725490196079]])
    # show(groundColorMask)
    frameNum = filename.split('.')[0]
    # rangeH, rangeS, rangeV = [0.28888888888888886, 0.3888888888888889], [0.3843137254901961, 0.6549019607843137], [0.5176470588235295, 0.7411764705882353]
    # rangeH, rangeS, rangeV = [0.35, 0.45555555555555555], [0.25098039215686274, 0.5058823529411764], [0.43529411764705883, 0.6039215686274509] #ck
    # rangeH, rangeS, rangeV = [0.26666666666666666, 0.3611111111111111], [0.39215686274509803, 0.6313725490196078], [0.22745098039215686, 0.596078431372549]
    rangeH, rangeS, rangeV = [0.2388888888888889, 0.45], [0.03529411764705882, 0.5019607843137255], [0.37254901960784315, 0.6392156862745098]

    # rangeH,rangeS,rangeV = getGroundColor(img)
    # print(rangeH, rangeS, rangeV)
    groundColorMask = rangeToMask(img, [rangeH],[rangeS],[rangeV])

    dbDir = '../DB/data6.db'
    db = connectDB(dbDir)
    playerData, ballData, goalData = getFrameData(db, frameNum)
    disconnectDB(db)
    playerMask = np.array(getPlayersMask(playerData, ballData))

    thres_val = getLineRange(img,groundColorMask,playerMask)
    # thres_val = 142
    # print(thres_val)
    lineMask = getLineMask(img,groundColorMask,playerMask,thres_val)

    coords = getEndPoints(lineMask, playerMask)
    # coords,_ = lineMerge(coords)
    # coords=coords.astype(np.int_)
    print('Time = ', time.time() - time_init)

    lineMask = np.squeeze(np.stack((lineMask,) * 3, -1))
    # colors = [(255,0,0), (0,255,0), (0,0,255), (255,255,0), (255,0,255), (0,255,255), (255, 100, 0), (113, 66, 244)]*2
    for p in range(len(coords)):
        point = coords[p]
        # idx = randint(0, len(colors)-1)
        color = (randint(0,255), randint(0,255), randint(0,255))
        # print(color)
        cv2.circle(lineMask,(point[0][1], point[0][0]), 10, color, -10)
        cv2.circle(lineMask,(point[1][1],point[1][0]), 10, color, -10)
        # colors.pop(idx)
    cv2.namedWindow('hmm',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('hmm', 1280,720)
    cv2.imshow('hmm', lineMask)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.namedWindow('hmm',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('hmm', 1280,720)
    cv2.imshow('hmm', playerMask*255)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


    # cv2.imwrite('points_final.png', lineMask)
