import numpy as np
import pickle
from mergeDicts import mergeDicts

def dataCalculator(pointsDicts):

    def getAngle(pt1, pt2):
        return np.arctan((pt2[1]-pt1[1])/(pt2[0]-pt1[0]))

    parentAnglesDict = {}

    for foldername, pointsDictList in pointsDicts.items():
        print(foldername)
        anglesDict = {'leftAngles': {}, 'rightAngles': {}}
        if(foldername=="imgs3" or foldername== "imgs4" or foldername=="imgs6" or foldername=="imgs2" or foldername=="imgs1" or foldername=="imgs7"):
            if len(pointsDictList) != 0:

                pointsDict = pointsDictList[0]
                bottomLineAngle = getAngle(pointsDict['bottomLeftCorner'], pointsDict['bottomLeftIntersection'])
                topLineAngle = getAngle(pointsDict['topLeftCorner'], pointsDict['topLeftIntersection'])
                topSideLineAngle = getAngle(pointsDict['leftBoxTopLeftCorner'], pointsDict['leftBoxTopRightCorner'])
                bottomSideLineAngle = getAngle(pointsDict['leftBoxBottomLeftCorner'], pointsDict['leftBoxBottomRightCorner'])
                pBoxLineAngle = getAngle(pointsDict['leftBoxTopRightCorner'], pointsDict['leftBoxBottomRightCorner'])
                sideBoundaryAngle = getAngle(pointsDict['leftBoxTopLeftCorner'], pointsDict['leftBoxBottomLeftCorner'])
                anglesDict['leftAngles']['bottomLine'] = bottomLineAngle
                anglesDict['leftAngles']['topLine'] = topLineAngle
                anglesDict['leftAngles']['topSideLine'] = topSideLineAngle
                anglesDict['leftAngles']['bottomSideLine'] = bottomSideLineAngle
                anglesDict['leftAngles']['pBoxLine'] = pBoxLineAngle
                anglesDict['leftAngles']['sideBoundary'] = sideBoundaryAngle


                pointsDict = pointsDictList[3]
                bottomLineAngle = getAngle(pointsDict['bottomRightCorner'], pointsDict['bottomRightIntersection'])
                topLineAngle = getAngle(pointsDict['topRightCorner'], pointsDict['topRightIntersection'])
                topSideLineAngle = getAngle(pointsDict['rightBoxTopLeftCorner'], pointsDict['rightBoxTopRightCorner'])
                bottomSideLineAngle = getAngle(pointsDict['rightBoxBottomLeftCorner'], pointsDict['rightBoxBottomRightCorner'])
                pBoxLineAngle = getAngle(pointsDict['rightBoxTopLeftCorner'], pointsDict['rightBoxBottomLeftCorner'])
                sideBoundaryAngle = getAngle(pointsDict['rightBoxTopRightCorner'], pointsDict['rightBoxBottomRightCorner'])
                anglesDict['rightAngles']['bottomLine'] = bottomLineAngle
                anglesDict['rightAngles']['topLine'] = topLineAngle
                anglesDict['rightAngles']['topSideLine'] = topSideLineAngle
                anglesDict['rightAngles']['bottomSideLine'] = bottomSideLineAngle
                anglesDict['rightAngles']['pBoxLine'] = pBoxLineAngle
                anglesDict['rightAngles']['sideBoundary'] = sideBoundaryAngle

        parentAnglesDict[foldername] = anglesDict


    return parentAnglesDict


if __name__ == '__main__':
    f = open('pointsDictData.dat', 'rb')
    pointsDicts = pickle.load(f)
    f.close()

    matchData = dataCalculator(pointsDicts)
    print(matchData)

    f = open('matchData.dat', 'wb')
    pickle.dump(matchData, f)
    f.close()
