import cv2
import numpy as np
from copy import deepcopy
from inputPoints import collectPoints

def mapPoint(pt, h):
    pt1 = np.array([pt[0], pt[1], 1])
    pt1 = np.reshape(pt1, (3,1))
    pt2 = np.matmul(h, pt1)
    pt2 = pt2 / pt2[2][0]
    pt2 = pt2.astype(np.int_)
    pt2 = [pt2[0][0], pt2[1][0]]
    return np.array(pt2)


def calcHMat(h, points):
    hInv = np.linalg.inv(h)
    mappedPoints = np.array([[0,0]])

    for pt in points:
        pt2 = mapPoint(pt,hInv)
        # cv2.circle(im_src, (abs(pt2[0][0]), abs(pt2[1][0])), 2, (0,0,255), -2)
        mappedPoints = np.append(mappedPoints, [pt2] ,axis=0)

    mappedPoints = mappedPoints[1:]
    pts_dst = points
    pts_src = mappedPoints
    h, status = cv2.findHomography(pts_src, pts_dst)

    return h

def adjustPitch(field, widthDist, centerDist, extwidth):
    field = np.array(field)
    field[180-widthDist:180,:] = field[37:37+widthDist,:]
    field[:180-widthDist,:] = 0
    field[416:416+widthDist,:] = field[560-widthDist:560,:]
    field[416+widthDist:,:] = 0
    fieldNew = np.array(field)
    fieldNew[:,:349] = 0
    fieldNew[:,458:] = 0
    fieldNew[:,349-154-centerDist:349] = field[:,:154+centerDist]
    fieldNew[:,458: 800-(652-458-centerDist)] = field[:,652-centerDist:800]
    
    lineThickness = 2
    const_d=98
    left_v= 349-centerDist-const_d
    right_v= 458+centerDist+const_d
    print(left_v,right_v) 
    fieldNew= cv2.line(fieldNew, (left_v, 180-widthDist-extwidth), (right_v ,  180-widthDist-extwidth), (255,255,0), lineThickness)
    fieldNew= cv2.line(fieldNew, (left_v, 180-widthDist-extwidth), (left_v,  180-widthDist ), (255,255,0), lineThickness)
    fieldNew= cv2.line(fieldNew, (right_v, 180-widthDist-extwidth), (right_v,  180-widthDist ), (255,255,0), lineThickness)
    return fieldNew


def mapPoint(pt, h):
    pt1 = np.array([pt[0], pt[1], 1])
    pt1 = np.reshape(pt1, (3,1))
    pt2 = np.matmul(h, pt1)
    pt2 = pt2 / pt2[2][0]
    pt2 = pt2.astype(np.int_)
    pt2 = [pt2[0][0], pt2[1][0]]
    return np.array(pt2)


def adjustPitchPoints(pitchPointsDict, widthDist, centerDist,  extwidth):
    for k in pitchPointsDict.keys():
        pitchPointsDict[k] = list(pitchPointsDict[k])

    currCenterDist = abs(pitchPointsDict['leftBoxTopRightCorner'][0] - pitchPointsDict['ellipseLeftPoint'][0])
    horizontalShift = abs(currCenterDist - centerDist)
    currWidthDist = abs(pitchPointsDict['leftBoxTopRightCorner'][1] - pitchPointsDict['topLeftCorner'][1])
    verticalShift = abs(currWidthDist - widthDist)

    # print(pitchPointsDict['leftBoxTopRightCorner'])

    pitchPointsDict['leftBoxTopLeftCorner'][0] += horizontalShift
    pitchPointsDict['leftBoxTopRightCorner'][0] += horizontalShift
    pitchPointsDict['leftBoxBottomLeftCorner'][0] += horizontalShift
    pitchPointsDict['leftBoxBottomRightCorner'][0] += horizontalShift
    pitchPointsDict['leftGoalPostLeftPoint'][0] += horizontalShift
    pitchPointsDict['leftGoalPostRightPoint'][0] += horizontalShift
    pitchPointsDict['topLeftCorner'][0] += horizontalShift
    pitchPointsDict['bottomLeftCorner'][0] += horizontalShift
    pitchPointsDict['topLeftIntersection'][0] += horizontalShift
    pitchPointsDict['bottomLeftIntersection'][0] += horizontalShift

    pitchPointsDict['rightBoxTopLeftCorner'][0] -= horizontalShift
    pitchPointsDict['rightBoxTopRightCorner'][0] -= horizontalShift
    pitchPointsDict['rightBoxBottomLeftCorner'][0] -= horizontalShift
    pitchPointsDict['rightBoxBottomRightCorner'][0] -= horizontalShift
    pitchPointsDict['rightGoalPostLeftPoint'][0] -= horizontalShift
    pitchPointsDict['rightGoalPostRightPoint'][0] -= horizontalShift
    pitchPointsDict['topRightCorner'][0] -= horizontalShift
    pitchPointsDict['bottomRightCorner'][0] -= horizontalShift
    pitchPointsDict['topRightIntersection'][0] -= horizontalShift
    pitchPointsDict['bottomRightIntersection'][0] -= horizontalShift



    pitchPointsDict['topLeftCorner'][1] += verticalShift
    pitchPointsDict['centerTopPoint'][1] += verticalShift
    pitchPointsDict['topRightCorner'][1] += verticalShift

    pitchPointsDict['bottomLeftCorner'][1] -= verticalShift
    pitchPointsDict['centerBottomPoint'][1] -= verticalShift
    pitchPointsDict['bottomRightCorner'][1] -= verticalShift

    pitchPointsDict['exttopLeftIntersection']=[ pitchPointsDict['topLeftIntersection'][0] , pitchPointsDict['topLeftIntersection'][1]- extwidth]
    pitchPointsDict['exttopRightIntersection']=[ pitchPointsDict['topRightIntersection'][0] , pitchPointsDict['topRightIntersection'][1]- extwidth]
    pitchPointsDict['exttopLeftCorner']=[ pitchPointsDict['topLeftCorner'][0] , pitchPointsDict['topLeftCorner'][1]- extwidth]
    pitchPointsDict['exttopRightCorner']=[ pitchPointsDict['topRightCorner'][0] , pitchPointsDict['topRightCorner'][1]- extwidth]
    pitchPointsDict['exttopCenterIntersection']= [ pitchPointsDict['centerTopPoint'][0] , pitchPointsDict['centerTopPoint'][1]-extwidth]

    for k in pitchPointsDict.keys():
        pitchPointsDict[k] = tuple(pitchPointsDict[k])

    return pitchPointsDict


def pitchMaker(pitch, pitchPointsDict, pointsDictList):
    
    hGraphyPtsLeft = ['leftBoxTopLeftCorner','leftBoxTopRightCorner', 'leftBoxBottomLeftCorner', 'leftBoxBottomRightCorner']
    hGraphyPtsRight = ['rightBoxTopLeftCorner', 'rightBoxTopRightCorner', 'rightBoxBottomLeftCorner', 'rightBoxBottomRightCorner']
    # widthPtsLeft = ['topLeftIntersection', 'leftBoxTopLeftCorner']
    # widthPtsRight = ['topRightIntersection', 'rightBoxTopRightCorner']
    widthPtsLeft = ['topLeftCorner', 'leftBoxTopLeftCorner']
    widthPtsRight = ['topRightCorner', 'rightBoxTopRightCorner']
    lengthPtsLeft = ['ellipseLeftPoint', 'leftBoxTopRightCorner']
    lengthPtsRight = ['ellipseRightPoint', 'rightBoxTopLeftCorner']
    
    extrawidth_initPts_left= ['topLeftCorner','topLeftIntersection']
    extrawidth_initPts_right= ['topRightCorner', 'topRightIntersection']
    extrawidth_refPts_left=['exttopLeftCorner','exttopLeftIntersection']
    extrawidth_refPts_right=['exttopRightCorner', 'exttopRightIntersection']

    widthDists, centerDists = [], []
    extrawidthDists= []
    for i in range(2):
        im_new=deepcopy(pitch)
        hGraphyPts = hGraphyPtsLeft if i == 0 else hGraphyPtsRight
        widthPts = widthPtsLeft if i == 0 else widthPtsRight
        lengthPts = lengthPtsLeft if i == 0 else lengthPtsRight
        extrawidth_points_init= extrawidth_initPts_left if i==0 else extrawidth_initPts_right
        extrawidth_points_ref= extrawidth_refPts_left if i==0 else extrawidth_refPts_right
        
        pointsDict = pointsDictList[3*i]
        print(pointsDict)
        imgPoints = np.array([pointsDict[x] for x in hGraphyPts])
        pitchPoints = np.array([pitchPointsDict[x] for x in hGraphyPts])

        h, status = cv2.findHomography(imgPoints, pitchPoints)

        #check_output

        
        for k, pt in pointsDict.items():
            mappedPt = mapPoint(pt, h)
            cv2.circle(im_new, (mappedPt[0], mappedPt[1]), 2, (0,0,255), -2)

        
        cv2.imshow('hmm', im_new)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        #delete this 


        
        # im_dst = cv2.warpPerspective(pitch, np.linalg.inv(h), (im_new.shape[0],im_new.shape[1]))
        extrawidthPtsOnPitch1 = np.array([mapPoint(pointsDict[extrawidth_points_init[0]], h), mapPoint(pointsDict[extrawidth_points_ref[0]], h)])
        extrawidthPtsOnPitch2 = np.array([mapPoint(pointsDict[extrawidth_points_init[1]], h), mapPoint(pointsDict[extrawidth_points_ref[1]], h)])
        extrawidth1= abs(extrawidthPtsOnPitch1[0][1] - extrawidthPtsOnPitch1[1][1])
        extrawidth2= abs(extrawidthPtsOnPitch2[0][1] - extrawidthPtsOnPitch2[1][1])
        extrawidthDists.append(extrawidth1)
        extrawidthDists.append(extrawidth2)

        widthPtsOnPitch = np.array([mapPoint(pointsDict[widthPts[0]], h), mapPoint(pointsDict[widthPts[1]], h)])
        lengthPtsOnPitch = np.array([mapPoint(pointsDict[lengthPts[0]], h), mapPoint(pointsDict[lengthPts[1]], h)])

        widthDist = abs(widthPtsOnPitch[0][1] - widthPtsOnPitch[1][1])
        centerDist = abs(lengthPtsOnPitch[0][0] - lengthPtsOnPitch[1][0])

        widthDists.append(widthDist)
        centerDists.append(centerDist)

    print(extrawidthDists) 
    print(widthDists)
    print(centerDists)    
    widthDist = int(np.average(widthDists))
    centerDist = int(np.average(centerDists))
    extwidthDist= int(np.average(extrawidthDists))
    print(widthDist, centerDist, extwidthDist)

    pitch = adjustPitch(pitch, widthDist, centerDist, extwidthDist)
    pitchPointsDict = adjustPitchPoints(pitchPointsDict, widthDist, centerDist, extwidthDist)

    return pitch, pitchPointsDict


if __name__ == '__main__':
    import pickle

    f = open('pitchPointsData.dat', 'rb')
    pitchPointsDict = pickle.load(f)
    f.close()

    f = open('pointsDictData.dat', 'rb')
    pointsDicts = pickle.load(f)
    f.close()

    pitchDir = './pitch.png'
    pitchImg = cv2.imread(pitchDir)

    pitchSaveDir = './pitches/'

    for filename, pointsDictList in pointsDicts.items():
        # print(pitchPointsDict)
        if(filename=="imgs3"):
            if pointsDictList != []:
                pitch, newPitchPointsDict = pitchMaker(pitchImg, pitchPointsDict, pointsDictList)
                
                print(pitchSaveDir + filename + '.jpg')
                cv2.imwrite(pitchSaveDir + filename + '.jpg', pitch)
                f = open(pitchSaveDir + filename + '.dat', 'wb')
                pickle.dump(newPitchPointsDict, f)
                f.close()
                f = open('pitchPointsData.dat', 'rb')
                pitchPointsDict = pickle.load(f)
                f.close()
    # pitch = adjustPitch(pitchImg, 50, 50)
    # cv2.imwrite('testPitch.jpg', pitch)

    # im_src = cv2.imread('559.png')
    # im_dst = cv2.imread('pitch.png')
    #
    # ### Data to be changed ####
    # pts_src = np.array([[1208, 351],  [1870, 317], [1857, 408], [1390, 448]])       # 4 points on penalty box
    # pts_dst = np.array([[654, 183], [750, 183], [717, 248], [654, 260]])            # first point should be the top left point on the box
    # pBoxExtendedPt = np.array([1053, 265])  # On main Image, extended point from penalty box on top line
    # cornerPt = [1648, 239]  # On main Image, top right corner pt of pitch
    # ellipsePoint = np.array([117,588]) # Rightmost point on ellipse on main image
    # ######
    # pitchCorner = np.array([750,38])    # Point on 2D pitch, don't change this
    # penaltyBoxCorner = np.array([750, 182])  #Point on 2D pitch, don't change this
    #
    # h, status = cv2.findHomography(pts_src, pts_dst)
    #
    # # im_dst1 = cv2.warpPerspective(im_src, h, (im_dst.shape[1], im_dst.shape[0]))
    # # cv2.imshow('hmm', im_dst1)
    # # cv2.waitKey(0)
    # # cv2.destroyAllWindows()
    #
    # ############
    #
    # points = np.array(pts_dst)
    #
    # for i in range(16):
    #     # points[:,1] = points[:,1] - 5
    #     points = points - 5
    #     h = calcHMat(h, points)
    #
    # pt2 = mapPoint(pBoxExtendedPt, h)
    # im_dst1 = cv2.warpPerspective(im_src, h, (im_dst.shape[1], im_dst.shape[0]))
    # cv2.circle(im_dst1, (abs(pt2[0]), abs(pt2[1])), 2, (255,0,0), -2)
    #
    # pt = pts_src[0]
    # pt3 = mapPoint(pt, h)
    # cv2.circle(im_dst1, (abs(pt3[0]), abs(pt3[1])), 2, (255,0,0), -2)
    # dist = ( (pt3[0]-pt2[0])**2 + (pt3[1]-pt2[1])**2 )**0.5
    #
    # widthDist = int(dist)
    #
    # pitch = cv2.imread('pitch.png', 0)
    # _ = adjustPitch(pitch, widthDist)
