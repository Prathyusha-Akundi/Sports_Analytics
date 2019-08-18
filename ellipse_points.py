import cv2
import numpy as np
from scipy import stats
import time
from end_points import getEndPoints

'''
Input: bw image of lines on the ground
Output: Coordinates of two points on ellipse around centre line. These two points share the same horizontal coordinate. If no such points are found, [] is returned.

Image is resized to 858x480 dims, and only (sufficiently big) area around the centre line is considered to reduce computation.
Starting from centre line, pixels on each column are considered, seperated to bins, and if a two bins accumulates enough points, they're selected.
'''

def getEllipsePoints(lineMask, centerLine, paraLine, bottomBoundary, binTolerance = 10, thres = 15):
    lineMask = np.array(lineMask)
    paraLine = np.fliplr(np.reshape(paraLine, (2,2)))
    paraLine = sorted(paraLine, key = lambda x: x[1])
    if paraLine != []:
        cv2.line(lineMask, tuple(paraLine[0][::-1]), tuple(paraLine[1][::-1]), (0,0,0), 140)
        pts = np.array([[0,0], paraLine[0][::-1], paraLine[1][::-1], [1920,0]], np.int32)
        # pts = pts.reshape((-1,1,2))
        cv2.fillPoly(lineMask,[pts],0)
    if bottomBoundary != []:
        cv2.line(lineMask, tuple(bottomBoundary[0][0][::-1]), tuple(bottomBoundary[0][1][::-1]), (0,0,0), 140)
        pts = np.array([bottomBoundary[0][0][::-1], bottomBoundary[0][1][::-1], [1920, 1080], [0, 1080]], np.int32)
        # pts = pts.reshape((-1,1,2))
        cv2.fillPoly(lineMask,[pts],0)

    # print(paraLine, bottomBoundary)
    [[pt1, pt2]] = centerLine

    img = cv2.dilate(lineMask, np.ones((4,4), np.uint8))
    img = cv2.resize(img, (858, 480))

    horizontalSpan = 1200
    top = pt1[0]
    bottom = pt2[0]
    left = int((pt1[1]+pt2[1])/2 - horizontalSpan/2) if (pt1[1]+pt2[1])/2 - horizontalSpan/2 > 0 else 0             # Getteing area around the centre line
    right = int((pt1[1]+pt2[1])/2 + horizontalSpan/2) if (pt1[1]+pt2[1])/2 + horizontalSpan/2 < 1920 else 1920

    factor = img.shape[0]/1080  #above calcs are for 1080p, they need to be scaled by this factor

    top, bottom, left, right = int(top*factor), int(bottom*factor), int(left*factor), int(right*factor)

    i = int(min([pt1[1], pt2[1]])*factor)-10
    bins = {}
    points = {}
    foundOnLeft = 0
    nonCommonCoord = []
    while(i > left):
        arr = np.where(img[:,i] == 255)[0]
        idx = 0
        while idx < len(arr):
            x = arr[idx]
            added = 0
            for j in list(range(binTolerance//2))+list(np.array(list(range(binTolerance//2)))*-1):  # if some bin already exists within the binTolerance of the current point,
                if x+j in bins.keys():                                                              # the current point is added to that bin
                    bins[x+j] += 1
                    points[x+j].append(i)
                    arr = np.concatenate((arr[arr>x+j+binTolerance/2], arr[arr<x+j-binTolerance/2]))        #pixels near the one selected are removed.
                    added = 1
                    break
            if added == 0:
                bins[x] = 1
                points[x] = [i]
                arr = np.concatenate((arr[arr>x+binTolerance/2], arr[arr<x-binTolerance/2]))
                added = 1
            idx+=1

        moreThanThres = 0
        for x in bins.keys():
            if bins[x] > thres:
                moreThanThres +=1
                nonCommonCoord.append(x)
        if(moreThanThres >= 2):
            foundOnLeft = 1
            break
        else:
            nonCommonCoord = []
        i-=1

    if foundOnLeft == 1:        #if two bins are selected, they must also share some common horizontal coordinate at some point
        pointList = []
        for x in nonCommonCoord:
            pointList.append(points[x])

        commonCoord = list(set(pointList[0]) & set(pointList[1]))
        if commonCoord != []:
            commonCoord = commonCoord[0]
        else:
            foundOnLeft = 0


    foundOnRight = 0
    if(foundOnLeft == 0):
        i = int(max([pt1[1], pt2[1]])*factor)+10
        bins = {}
        points = {}
        nonCommonCoord = []
        while(i < right):
            arr = np.where(img[:,i] == 255)[0]
            idx = 0
            while idx < len(arr):
                x = arr[idx]
                added = 0
                for j in list(range(binTolerance//2))+list(np.array(list(range(binTolerance//2)))*-1):
                    if x+j in bins.keys():
                        bins[x+j] += 1
                        points[x+j].append(i)
                        arr = np.concatenate((arr[arr>x+j+binTolerance/2], arr[arr<x+j-binTolerance/2]))
                        added = 1
                        break
                if added == 0:
                    bins[x] = 1
                    points[x] = [i]
                    arr = np.concatenate((arr[arr>x+binTolerance/2], arr[arr<x-binTolerance/2]))
                    added = 1
                idx+=1

            moreThanThres = 0
            for x in bins.keys():
                if bins[x] > thres:
                    moreThanThres +=1
                    nonCommonCoord.append(x)
            if(moreThanThres >= 2):
                foundOnRight = 1
                break
            else:
                nonCommonCoord = []
            i+=1

    if foundOnRight == 1:
        pointList = []
        for x in nonCommonCoord:
            pointList.append(points[x])

        commonCoord = list(set(pointList[0]) & set(pointList[1]))
        if commonCoord != []:
            commonCoord = commonCoord[0]
        else:
            foundOnRight = 0

    # print(foundOnLeft, foundOnRight)

    if foundOnLeft == 1 or foundOnRight == 1:
        if commonCoord != 0:
            coords = np.array([[commonCoord, nonCommonCoord[0]], [commonCoord, nonCommonCoord[1]]])
            coords = coords/factor
            coords = coords.astype(np.int_)
        else:
            return []
    else:
        return []

    return np.array(coords)



if __name__ == '__main__':
    img = cv2.imread('../124.png', 0)
    time_init = time.time()
    coords = getEllipsePoints(img)
    print('Time: ', time.time()-time_init)

    print(coords)
    if coords != []:
        temp_img = np.squeeze(np.stack((img,) * 3, -1))
        cv2.circle(temp_img, (coords[0][0], coords[0][1]), 5, (0,0,255), -5)
        cv2.circle(temp_img, (coords[1][0], coords[1][1]), 5, (0,0,255), -5)
        cv2.imwrite('ellipsePoints.png', temp_img)
    else:
        print('No points found')
