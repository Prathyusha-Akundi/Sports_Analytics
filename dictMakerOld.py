import cv2
import numpy as np
from goalLine import getGoalLine
from ground_color import getGroundColor, rangeToMask
from find_outline_boundaries import findOuterBoundaries, improveCorner
from find_inner_boundaries import find_inner_boundaries
from lines_and_mag import lines_and_mag
from lines import getStandMask, getLineMask, getLineRange
from end_points import getEndPoints
from line_merge import lineMerge
from DLdata import connectDB, disconnectDB, getFrameData, getPlayersMask

def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return np.array([x, y])

def getPointsForDict(img, dbDir):
    db = connectDB(dbDir)
    playerData, ballData, goalData = getFrameData(db, frameNum)
    disconnectDB(db)
    bBox = goalData[0]

    # rangeH, rangeS, rangeV = getGroundColor(img)
    # print(rangeH, rangeS, rangeV)
    rangeH, rangeS, rangeV = [0.25555555555555554, 0.37222222222222223], [0.27450980392156865, 0.6705882352941176], [0.1568627450980392, 0.5176470588235295]
    ground_mask = rangeToMask(img, [rangeH],[rangeS],[rangeV])
    player_mask = np.array(getPlayersMask(playerData, ballData))
    white_thres = getLineRange(img, ground_mask, player_mask)

    [top1, top2, bottom1, bottom2] = getGoalLine(img, bBox, white_thres, [1.3885779892102874, 1.42697065429588], [1.049079754601227, 0.9644970414201184], [[-19.38738787344459, -9.387387873444592], [8.677776114838897, 18.6777761148389]])
    stands_mask = getStandMask(ground_mask, player_mask)
    upper_bound, lower_bound = findOuterBoundaries(stands_mask, player_mask)
    upper_bound, status = improveCorner(img, goalData, upper_bound, white_thres)
    print(upper_bound, lower_bound)

    case_in, para_lines, para_lines1, _, _ = find_inner_boundaries(upper_bound, lower_bound)

    lines_img = getLineMask(img, ground_mask, player_mask, white_thres)

    cv2.imshow('hmm', ground_mask*255)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imshow('hmm', lines_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imshow('hmm', stands_mask*255)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    coords = getEndPoints(lines_img)
    coords, lines = lineMerge(coords)
    center_line_idx, label, mag = lines_and_mag(lines, coords, case_in, para_lines, para_lines1)
    pLine = coords[label]
    pLine[0] = pLine[0][::-1]
    pLine[1] = pLine[1][::-1]
    pLineTop = pLine[0] if pLine[0][1] < pLine[1][1] else pLine[1]
    cv2.line(img, tuple(pLine[0]),tuple(pLine[1]),(0,255,0),3)
    cv2.circle(img,tuple(pLineTop), 5, (0,0,255), -5)

    [lPt, cPt, rPt] = upper_bound.T

    def absSlope(pt1, pt2):
        return abs((pt2[1]-pt1[1])/(pt2[0]-pt1[0]))

    if absSlope(lPt, cPt) < absSlope(cPt, rPt):
        ub1 = lPt
        ub2 = cPt
        alpha = 1
    else:
        ub1 = cPt
        ub2 = rPt
        alpha = -1

    extendedPt = line_intersection(pLine, (ub1, ub2))
    extendedPt = extendedPt.astype(np.int_)
    cv2.circle(img,tuple(extendedPt), 5, (0,0,255), -5)

    interPt = cPt

    if np.linalg.norm(interPt - cPt) < 500:
        status = 1
    else:
        interPt = cPt
        status = 0

    interPt = interPt.astype(np.int_)

    lastPoint = (interPt - extendedPt)
    cv2.circle(img,tuple(line_intersection(((lastPoint+pLineTop), pLineTop), (bottom1, bottom2)).astype(np.int_)), 5, (255,0,255), -5)
    alpha = alpha*np.pi/180
    rotMat = np.array([[np.cos(alpha), np.sin(alpha)],
                       [-1*np.sin(alpha), np.cos(alpha)]])
    lastPoint = np.matmul(rotMat, lastPoint)
    lastPoint = pLineTop + lastPoint

    lastPoint = line_intersection((lastPoint, pLineTop), (bottom1, bottom2))
    lastPoint = lastPoint.astype(np.int_)

    cv2.circle(img,tuple(lastPoint), 5, (0,0,255), -5)
    cv2.circle(img,tuple(bottom1), 5, (0,255,0), -5)
    cv2.circle(img,tuple(bottom2), 5, (0,255,0), -5)
    cv2.circle(img,tuple(ub1), 5, (255,0,0), -5)
    cv2.circle(img,tuple(ub2), 5, (255,0,0), -5)

    print(extendedPt, cPt, lastPoint, pLineTop)

    return interPt, status


if __name__ == '__main__':
    import os
    os.chdir('..')
    filename = '453.jpg' #453
    img = cv2.imread(filename, 1)
    frameNum = filename.split('.')[0]
    dbDir = './DB/data10.db'

    pt, status = getPointsForDict(img, dbDir)

    if status == 1:
        cv2.circle(img,(pt[0], pt[1]), 5, (0,0,255), -5)
    else:
        cv2.circle(img,(pt[0], pt[1]), 5, (0,255,255), -5)

    cv2.imshow('hmm', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
