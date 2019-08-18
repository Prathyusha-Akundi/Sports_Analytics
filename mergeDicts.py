import numpy as np
import cv2
from inputPoints import collectPoints
from copy import deepcopy


def mergeDicts(dict1, dict2):
    dict1 = deepcopy(dict1)
    commonKeys = list(set([k for k,v in dict1.items() if v!=(-1,-1)]) & set([k for k,v in dict2.items() if v!=(-1,-1)]))
    print(commonKeys)
    if len(commonKeys) < 2:
        return False
    else:
        commonKeys = commonKeys[:2]
        a1 = np.array(dict1[commonKeys[0]])
        a2 = np.array(dict1[commonKeys[1]])
        b1 = np.array(dict2[commonKeys[0]])
        b2 = np.array(dict2[commonKeys[1]])
        xOffset, yOffset = (a1-b1)[0], (a1-b1)[1]
        scaleFactor = np.linalg.norm(a1-a2)/np.linalg.norm(b1-b2)

        def transformPoint(pt, refPt, xOffset, yOffset, scaleFactor):
            pt = np.array(pt)
            refPt = refPt + np.array([xOffset, yOffset])
            pt = pt + np.array([xOffset, yOffset])
            newPt = refPt + (pt-refPt)*scaleFactor
            return tuple(newPt.astype(np.int_))

        toBeTransformed = [k for k,v in dict2.items() if v!=(-1,-1)]

        refPt = b1
        for key in toBeTransformed:
            if dict1[key] == (-1,-1):
                dict1[key] = transformPoint(dict2[key], refPt, xOffset, yOffset, scaleFactor)

        return dict1


def plotPoints(img, ptsDict):
    for pt in ptsDict.values():
        cv2.circle(img, (pt[0]+4000, pt[1]+4000), 10, (0,0,255), -10)


if __name__ == '__main__':
    img1Dir = '../Videos/imgs7/171.jpg'
    img2Dir = '../Videos/imgs7/147.jpg'
    # img3Dir = '../../Videos/imgs7/181.jpg'

    dict1 = collectPoints(img1Dir)
    dict2 = collectPoints(img2Dir)
    # dict3 = collectPoints(img3Dir)

    dict1 = mergeDicts(dict1, dict2)
    # mergedDict = mergeDicts(dict1, dict3)
    if mergedDict != False:
        # print(np.array(list(zip(mergedDict.keys(), mergedDict.values()))))
        print(mergedDict)

        img1 = cv2.imread(img1Dir)
        img1 = cv2.copyMakeBorder( img1, 4000, 4000, 4000, 4000, borderType = cv2.BORDER_CONSTANT, value=(255,255,255))
        plotPoints(img1, mergedDict)
        cv2.imwrite('test.jpg', img1)
    else:
        print('Not sufficient points for merging')
