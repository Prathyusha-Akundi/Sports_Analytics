import numpy as np
from merge_lines import lineMerge
# from line_merge import lineMerge

def lineToPointDistance(point, line):
    p1 = point
    p2, p3 = line
    d = np.linalg.norm(np.cross(p3-p2, p2-p1))/np.linalg.norm(p3-p2)
    return d


def lineToLineDistance(line1, line2, only1to2dist=0):
    arr = [lineToPointDistance(line1[0], line2), lineToPointDistance(line1[1], line2)]
    if only1to2dist == 0:
        arr.extend([lineToPointDistance(line2[0], line1), lineToPointDistance(line2[1], line1)])

    return min(arr)


def findIntersections(pBoxLine, bottomLines):
    def line_intersection(line1, line2):
        xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
        ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(xdiff, ydiff)
        if div == 0:
           return np.array([0, 0])

        d = (det(*line1), det(*line2))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        return np.array([x, y])

    points = []
    for line in bottomLines:
        interPt = line_intersection(line, pBoxLine[0])
        points.append(interPt)

    return np.array(points).astype(np.int_)


def linesOnCorrectSide(lines, pBoxLine, paraSlope):
    if np.sign(paraSlope) == 1:
        refPt = [0, 0]
    else:
        refPt = [0, 1920]

    def whichSideOfLine(point, line):
        x, y = point
        [[x1, y1], [x2, y2]] = line
        return (x-x1)*(y2-y1)-(y-y1)*(x2-x1)

    filtered = []
    for line in lines:
        midPt = (line[0]+line[1])//2
        if np.sign(whichSideOfLine(midPt, pBoxLine[0])) == np.sign(whichSideOfLine(refPt, pBoxLine[0])):
            filtered.append(line)

    return filtered



def lineIdentification(lines, coords, case, paraSlope, paraLine, perSlope, perLine, matchData):
    coords,lines = lineMerge(coords)

    def getSlope(pt1, pt2):
        return (pt2[0]-pt1[0])/(pt2[1]-pt1[1])

    pBoxLineAngleTolerance = 5
    pBoxLineLengthRatioTolerance = 0.66
    pBoxLineOffset = 70
    topSidelineTolerance = 5
    bottomSidelineTolerance = 5
    bottomBoundaryTolerance = 5
    bottomBoundaryOffsetTolerance = 150
    bottomSidelineBottomBoundaryAngleTolerance = 5
    topSidelineOffsetTolerance = 100
    bottomSidelineOffsetTolerance = 80
    pBoxLineParaLineAngleTolerance = 3
    centerLineMinLength = 500

    ############ Finding Center Line ############

    centerLine = []
    for line in coords:
        if(np.arctan(abs(getSlope(*tuple(line))))*180/np.pi >= 80 and np.linalg.norm(line[0]-line[1]) > centerLineMinLength):
            centerLine = [line]


    ############ View Detection ############

    if paraLine != []:
        paraLine = np.fliplr(np.reshape(paraLine, (2,2)))
        paraLine = sorted(paraLine, key = lambda x : x[1])
    if perLine != []:
        perLine = np.fliplr(np.reshape(perLine, (2,2)))
        perLine = sorted(perLine, key = lambda x : x[1])

    if paraLine != []:
        if paraLine[0][0] > paraLine[1][0]:
            viewAngle = 'rightAngles'
        else:
            viewAngle = 'leftAngles'
    elif perLine != []:
        if perLine[0][0] < perLine[1][0]:
            viewAngle = 'rightAngles'
        else:
            viewAngle = 'leftAngles'
    else:
        return [], [] ,[] ,[]

    anglesDict = matchData[viewAngle]


    ############ Finding Penalty Box Line ############

    pBoxLine = []

    if paraLine != []:
        paraLine = sorted(paraLine, key = lambda x : x[1])

        angleDiff = anglesDict['pBoxLine'] - anglesDict['topLine']
        pBoxSlope = np.tan(np.arctan(paraSlope) + angleDiff)

        if perLine != []:
            for line in coords:
                if abs(np.arctan(getSlope(*tuple(line))) - np.arctan(pBoxSlope))*180/np.pi < pBoxLineAngleTolerance:
                    pBoxLine.append(line)

            pBoxLine = [x for x in pBoxLine if lineToLineDistance(x, perLine) > pBoxLineOffset]
            pBoxLine = sorted(pBoxLine, key = lambda x: np.linalg.norm(x[0]-x[1]))[-2:]
            pBoxLine = sorted(pBoxLine, key = lambda x: lineToLineDistance(x, perLine))

            # print(pBoxLine)
            if len(pBoxLine) == 0 or len(pBoxLine) == 1:
                pass
            elif np.linalg.norm(pBoxLine[1][0] - pBoxLine[1][1]) > (np.linalg.norm(pBoxLine[0][0] - pBoxLine[0][1]))*pBoxLineLengthRatioTolerance:
                pBoxLine = pBoxLine[-1:]
            else:
                pBoxLine = pBoxLine[:1]
        else:
            for line in coords:
                if abs(np.arctan(getSlope(*tuple(line))) - np.arctan(pBoxSlope))*180/np.pi < pBoxLineAngleTolerance:
                    pBoxLine.append(line)
            pBoxLine = sorted(pBoxLine, key = lambda x: np.linalg.norm(x[0]-x[1]))[-1:]
            if pBoxLine != []:
                if viewAngle == 'rightAngles':
                    pBoxLine = pBoxLine if min(pBoxLine[0], key = lambda x: x[1])[1] > 1920//2 else []
                else:
                    pBoxLine = pBoxLine if max(pBoxLine[0], key = lambda x: x[1])[1] < 1920//2 else []
    elif perLine != []:
        angleDiff = anglesDict['pBoxLine'] - anglesDict['sideBoundary']
        pBoxSlope = np.tan(np.arctan(perSlope) + angleDiff)

        for line in coords:
            if abs(np.arctan(getSlope(*tuple(line))) - np.arctan(pBoxSlope))*180/np.pi < pBoxLineAngleTolerance:
                pBoxLine.append(line)
        pBoxLine = sorted(pBoxLine, key = lambda x: np.linalg.norm(x[0]-x[1]))[-3:]
        pBoxLine = sorted(pBoxLine, key = lambda x: lineToLineDistance(x, perLine, 1))[-1:]

    if perLine != [] and not paraLine != []:
        angleDiff = anglesDict['topLine'] - anglesDict['sideBoundary']
        paraSlope = np.tan(np.arctan(perSlope) + angleDiff)


    ############ Finding Bottom Boundary ############

    bottomLines = []
    topLines = []
    bottomBoundaryLines = []
    for i in range(len(lines)):
        angleDiff = anglesDict['topSideLine'] - anglesDict['topLine']
        topSideLineSlope = np.tan(np.arctan(paraSlope) + angleDiff)
        angleDiff = anglesDict['bottomSideLine'] - anglesDict['topLine']
        bottomSideLineSlope = np.tan(np.arctan(paraSlope) + angleDiff)
        angleDiff = anglesDict['bottomLine'] - anglesDict['topLine']
        bottomBoundarySlope = np.tan(np.arctan(paraSlope) + angleDiff)

        slope, intercept = lines[i]
        if abs(np.arctan(slope) - np.arctan(topSideLineSlope))*180/np.pi <= topSidelineTolerance:
            topLines.append(coords[i])
        if abs(np.arctan(slope) - np.arctan(bottomSideLineSlope))*180/np.pi < bottomSidelineTolerance:
            bottomLines.append(coords[i])
        if abs(np.arctan(slope) - np.arctan(bottomBoundarySlope))*180/np.pi < bottomBoundaryTolerance:
            bottomBoundaryLines.append(coords[i])

    bottomBoundaryLines = sorted(bottomBoundaryLines, key = lambda x : (x[0][0]+x[1][0])//2)
    bottomBoundaryLines = [x for x in bottomBoundaryLines if abs((x[0][0]+x[1][0])//2 - (bottomBoundaryLines[-1][0][0]+bottomBoundaryLines[-1][1][0])//2) < 150]
    bottomBoundary = sorted(bottomBoundaryLines, key = lambda x: np.linalg.norm(x[0]-x[1]))[-1:]
    if bottomBoundary != [] and pBoxLine != []:
        bottomBoundary = bottomBoundary if (bottomBoundary[0][0][0]+bottomBoundary[0][1][0])//2 > max(pBoxLine[0][0][0], pBoxLine[0][1][0]) + bottomBoundaryOffsetTolerance else []
    if bottomBoundary != [] and centerLine != []:
        bottomBoundaryBottomPt = sorted(bottomBoundary[0], key = lambda x: x[0])[1]
        centerLineBottomPt = sorted(centerLine[0], key = lambda x: x[0])[1]
        bottomBoundary = bottomBoundary if centerLineBottomPt[0] < bottomBoundaryBottomPt[0] else []


    ############ Finding Side Lines ############

    def lineDistSorter(refLine, minDist, defVal):
        def sorter(x):
            dist = lineToLineDistance(x, refLine, 1)
            if dist < minDist:
                return defVal
            else:
                return dist
        return sorter

    if pBoxLine != []:
        bottomLines = linesOnCorrectSide(bottomLines, pBoxLine, paraSlope)
        topLines = linesOnCorrectSide(topLines, pBoxLine, paraSlope)

    topLines = sorted(topLines, key = lineDistSorter(paraLine, topSidelineOffsetTolerance, 1e10)) if paraLine != [] else []

    if bottomBoundary != []:
        bottomLines = sorted(bottomLines, key = lineDistSorter(bottomBoundary[0], bottomSidelineOffsetTolerance, 1e10))
        sideLines = [topLines[0]] if topLines != [] else []
        sideLines.extend(bottomLines[:1])
    else:
        sideLines = [topLines[0]] if topLines != [] else []

    return np.array(pBoxLine), np.array(sideLines), np.array(bottomBoundary), np.array(centerLine), viewAngle
