import cv2
import numpy as np
from copy import deepcopy
from inputPoints import collectPoints
import pickle

# im_src = cv2.imread('../../Videos/imgs1/526.jpg')
im_src = cv2.imread('../Videos/imgs6/730.jpg')
# im_dst = cv2.imread('pitch.png')
im_dst = cv2.imread('./pitches/imgs6.jpg')

# ptsDict = collectPoints('../../Videos/imgs6/730.jpg')
# print(ptsDict)
ptsDict = {'leftBoxBottomLeftCorner': (-1, -1), 'rightGoalPostRightPoint': (-1, -1), 'rightBoxBottomRightCorner': (2640, 576), 'ellipseLeftPoint': (-1, -1), 'leftBoxBottomRightCorner': (-1, -1), 'rightBoxTopRightCorner': (1657, 192), 'leftGoalPostLeftPoint': (-1, -1), 'bottomLeftCorner': (-1, -1), 'leftBoxTopLeftCorner': (-1, -1), 'topLeftIntersection': (-1, -1), 'topRightIntersection': (-1, -1), 'topRightCorner': (-1, -1), 'centerTopPoint': (-1, -1), 'ellipseTopPoint': (-1, -1), 'bottomRightCorner': (-1, -1), 'ellipseBottomPoint': (-1, -1), 'centerBottomPoint': (-1, -1), 'bottomLeftIntersection': (-1, -1), 'topLeftCorner': (-1, -1), 'leftBoxTopRightCorner': (-1, -1), 'rightBoxTopLeftCorner': (1051, 222), 'leftGoalPostRightPoint': (-1, -1), 'rightBoxBottomLeftCorner': (1776, 643), 'ellipseRightPoint': (-1, -1), 'rightGoalPostLeftPoint': (-1, -1), 'bottomRightIntersection': (-1, -1)}

#testimg Desktop
# ptsDict = {'ellipseRightPoint': (-1, -1), 'centerBottomPoint': (-1, -1), 'leftGoalPostRightPoint': (-1, -1), 'ellipseBottomPoint': (-1, -1), 'leftBoxTopRightCorner': (-1, -1), 'rightBoxTopRightCorner': (1111, 558), 'rightBoxBottomLeftCorner': (1516, 697), 'topRightIntersection': (-1, -1), 'centerTopPoint': (-1, -1), 'leftBoxBottomRightCorner': (-1, -1), 'leftBoxTopLeftCorner': (-1, -1), 'topRightCorner': (-1, -1), 'rightGoalPostRightPoint': (-1, -1), 'bottomLeftIntersection': (-1, -1), 'bottomRightIntersection': (-1, -1), 'topLeftCorner': (-1, -1), 'bottomRightCorner': (-1, -1), 'bottomLeftCorner': (-1, -1), 'ellipseTopPoint': (-1, -1), 'leftBoxBottomLeftCorner': (-1, -1), 'leftGoalPostLeftPoint': (-1, -1), 'rightGoalPostLeftPoint': (-1, -1), 'topLeftIntersection': (-1, -1), 'ellipseLeftPoint': (-1, -1), 'rightBoxTopLeftCorner': (763, 576), 'rightBoxBottomRightCorner': (1982, 649)}

f = open('./pitches/imgs6.dat', 'rb')
pitchPts = pickle.load(f)
f.close()


for k in ptsDict.keys():
    ptsDict[k] = list(ptsDict[k])

for k in pitchPts.keys():
    pitchPts[k] = list(pitchPts[k])


pts_src = np.array([ptsDict['rightBoxTopLeftCorner'], ptsDict['rightBoxTopRightCorner'], ptsDict['rightBoxBottomRightCorner'], ptsDict['rightBoxBottomLeftCorner']])
pts_dst = np.array([pitchPts['rightBoxTopLeftCorner'], pitchPts['rightBoxTopRightCorner'], pitchPts['rightBoxBottomRightCorner'], pitchPts['rightBoxBottomLeftCorner']])


def mapPoint(pt, h):
    pt1 = np.array([pt[0], pt[1], 1])
    pt1 = np.reshape(pt1, (3,1))
    pt2 = np.matmul(h, pt1)
    pt2 = pt2 / pt2[2][0]
    pt2 = pt2.astype(np.int_)
    pt2 = [pt2[0][0], pt2[1][0]]
    return np.array(pt2)

h, status = cv2.findHomography(pts_src, pts_dst)

for k, pt in ptsDict.items():
    mappedPt = mapPoint(pt, h)
    cv2.circle(im_dst, (mappedPt[0], mappedPt[1]), 2, (0,0,255), -2)


im_dst1 = cv2.warpPerspective(im_src, h, (im_dst.shape[1], im_dst.shape[0]))

cv2.imshow('hmm', im_dst+im_dst1)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imshow('hmm', im_dst)
cv2.waitKey(0)
cv2.destroyAllWindows()

# cv2.imshow('hmm', im_dst)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
