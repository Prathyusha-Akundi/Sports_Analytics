import tkinter as tk
from PIL import ImageTk, Image
import numpy as np
labelfont = ('times', 7) 

def paraPerAngle(pointsDict):
    if pointsDict['topRightCorner'] != (-1,-1) and pointsDict['bottomRightCorner'] != (-1,-1):
        paraLine = [pointsDict['topLeftCorner'], pointsDict['topRightCorner']]
        perLine = [pointsDict['topRightCorner'], pointsDict['bottomRightCorner']]
    elif pointsDict['topLeftCorner'] != (-1,-1) and pointsDict['bottomLeftCorner'] != (-1,-1):
        paraLine = [pointsDict['topLeftCorner'], pointsDict['topRightCorner']]
        perLine = [pointsDict['bottomLeftCorner'], pointsDict['topLeftCorner']]
    else:
        return 0

    def getSlope(pt1, pt2):
        return (pt2[0]-pt1[0])/(pt2[1]-pt1[1])

    paraSlope = getSlope(*tuple(paraLine))
    perSlope = getSlope(*tuple(perLine))

    return (np.arctan(perSlope) - np.arctan(paraSlope))*180/np.pi


def prepareLists():
    ExtendedPoints = ['exttopLeftCorner','exttopLeftIntersection', 'exttopCenterIntersection', 'exttopRightIntersection', 'exttopRightCorner']
    outerPoints = ['topLeftCorner', 'topRightCorner', 'bottomLeftCorner', 'bottomRightCorner', 'centerTopPoint', 'centerBottomPoint']
    outerPoints.extend(['topLeftIntersection', 'topRightIntersection', 'bottomLeftIntersection', 'bottomRightIntersection'])
    goalPoints = ['leftGoalPostLeftPoint', 'leftGoalPostRightPoint', 'rightGoalPostLeftPoint', 'rightGoalPostRightPoint']
    leftBoxPoints = ['leftBoxTopLeftCorner', 'leftBoxTopRightCorner', 'leftBoxBottomLeftCorner', 'leftBoxBottomRightCorner']
    rightBoxPoints = ['rightBoxTopLeftCorner', 'rightBoxTopRightCorner', 'rightBoxBottomLeftCorner', 'rightBoxBottomRightCorner']
    ellipsePoints = ['ellipseTopPoint', 'ellipseBottomPoint', 'ellipseLeftPoint', 'ellipseRightPoint']

    return ('outerPoints', outerPoints), ('goalPoints', goalPoints), ('leftBoxPoints', leftBoxPoints), ('rightBoxPoints', rightBoxPoints), ('ellipsePoints', ellipsePoints), ('extendedPoints',ExtendedPoints)


def prepareDict(dic, pointsList):
    for sometuple in pointsList:
        for point in sometuple[1]:
            dic[point] = (-1,-1)

    return dic


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


def redrawPoints(panel, dic):
    panel.delete('marker'+str(len(dic)))
    for key in dic.keys():
        x, y = dic[key]
        x = x*1280//1920
        y = y*720//1080
        color = 'red' if len(dic) != 4 else 'purple'
        panel.create_oval(x-5, y-5, x+5, y+5, fill=color, tag='marker'+str(len(dic)))

    if len(dic) != 4:
        refPts = ['rightBoxTopLeftCorner', 'rightBoxBottomLeftCorner', 'leftBoxTopRightCorner', 'leftBoxBottomRightCorner']
        extendedPts = ['topRightIntersection', 'bottomRightIntersection', 'topLeftIntersection', 'bottomLeftIntersection']
        for i in range(len(refPts)):
            pt1 = dic[refPts[i]]
            pt2 = dic[extendedPts[i]]
            if pt1 != (-1,-1) and pt2 != (-1,-1):
                if pt1[0] == pt2[0]:
                    edgePt1 = [pt1[0], 0]
                    edgePt2 = [pt2[0], 1080]
                else:
                    edgePt1 = line_intersection((pt1, pt2), ([0,0], [0,1080]))
                    edgePt2 = line_intersection((pt1, pt2), ([1920,0], [1920,1080]))
                panel.create_line(edgePt1[0]*1280//1920, edgePt1[1]*720//1080, edgePt2[0]*1280//1920, edgePt2[1]*720//1080, fill="red", tag='marker'+str(len(dic)))
    else:
        refPts = ['line1Pt1', 'line2Pt1']
        extendedPts = ['line1Pt2', 'line2Pt2']
        for i in range(len(refPts)):
            pt1 = dic[refPts[i]]
            pt2 = dic[extendedPts[i]]
            if pt1 != (-1,-1) and pt2 != (-1,-1):
                if pt1[0] == pt2[0]:
                    edgePt1 = [pt1[0], 0]
                    edgePt2 = [pt2[0], 1080]
                else:
                    edgePt1 = line_intersection((pt1, pt2), ([0,0], [0,1080]))
                    edgePt2 = line_intersection((pt1, pt2), ([1920,0], [1920,1080]))
                panel.create_line(edgePt1[0]*1280//1920, edgePt1[1]*720//1080, edgePt2[0]*1280//1920, edgePt2[1]*720//1080, fill="purple", tag='marker'+str(len(dic)))


def updateDict(dic1, dic2, selectionLabel, panel):
    def setDictVal(event):
        mouseX = event.x*1920//1280
        mouseY = event.y*1080//720
        if selectionLabel.cget('text') != 'None':
            if selectionLabel.cget('text') in dic1.keys():
                dic1[selectionLabel.cget('text')] = (mouseX, mouseY)
                redrawPoints(panel, dic1)
            else:
                dic2[selectionLabel.cget('text')] = (mouseX, mouseY)
                redrawPoints(panel, dic2)
    return setDictVal


def buttonFunc(selectionLabel):
    def targetSetter(event):
        target = event.widget.cget('text')
        selectionLabel.config(text=target)
    return targetSetter


def removeButton(dic, selectionLabel, panel):
    def remove(event):
        if selectionLabel.cget('text') != 'None':
            dic[selectionLabel.cget('text')] = (-1, -1)
            redrawPoints(panel, dic)
    return remove

def findIntersectionAndAssign(mainDict, tempDict, selectionLabel, panel):
    def intersectionFinder(event):
        if selectionLabel.cget('text') != 'None':
            mainDict[selectionLabel.cget('text')] = tuple(line_intersection((tempDict['line1Pt1'], tempDict['line1Pt2']), (tempDict['line2Pt1'], tempDict['line2Pt2'])).astype(np.int_))
            tempDict['line1Pt1'], tempDict['line1Pt2'], tempDict['line2Pt1'], tempDict['line2Pt2'] = (-1,-1), (-1,-1), (-1,-1), (-1,-1)
            redrawPoints(panel, mainDict)
            redrawPoints(panel, tempDict)
    return intersectionFinder


def collectPoints(imgDir):
    window = tk.Tk()
    window.title("inputPoints")
    window.geometry("1800x1000")
    window.configure(background='grey')
    im = Image.open(imgDir)
    im.thumbnail((1280, 720), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(im)

    buttonsFrame = tk.Frame(window)
    buttonsFrame.pack(side='right')

    pointsList = prepareLists()
    pointsDict = {}
    pointsDict = prepareDict(pointsDict, pointsList)

    tempPtsDict = {'line1Pt1': (-1,-1), 'line1Pt2': (-1,-1), 'line2Pt1': (-1,-1), 'line2Pt2': (-1,-1)}

    L = tk.Label(buttonsFrame, text = 'Currently Selected', width=25, bg='black', fg='white')
    L.pack(side='top')
    selectionLabel = tk.Label(buttonsFrame, text='None', width=25)
    selectionLabel.pack(side='top')

    R = tk.Button(buttonsFrame, text = 'REMOVE', width=25, bg='red4', fg='white')
    R.pack(side = 'bottom')

    for sometuple in pointsList:
        for point in sorted(sometuple[1], key=len)[::-1]:
            B = tk.Button(buttonsFrame, text = point,  font=labelfont, width=30, height=1)
            B.pack(side = 'bottom')
            B.bind('<Button-1>', buttonFunc(selectionLabel))
        L = tk.Label(buttonsFrame, text = sometuple[0], font=labelfont, width=30, height=1, bg='black', fg='white')
        L.pack(side='bottom')

    container = tk.Frame(window, width=1280, height = 880)
    container.pack(side='left')

    panel = tk.Canvas(container, width=1280, height=720)
    panel.bind('<Button-1>', updateDict(pointsDict, tempPtsDict, selectionLabel, panel))
    panel.pack(side = "top", fill = "both", expand = "yes")
    panel.create_image(img.width()//2, img.height()//2, image=img)

    botBar = tk.Frame(container, height = 160, width = 1280)
    botBar.pack(side='bottom')
    botBar.pack_propagate(0)
    interButton = tk.Button(botBar, text = 'Find point using intersection', width=20, height=10)
    interButton.pack(side = 'left')
    interButton.bind('<Button-1>', findIntersectionAndAssign(pointsDict, tempPtsDict, selectionLabel, panel))
    line2Pt2 = tk.Button(botBar, text = 'line2Pt2', width=20, height=2)
    line2Pt2.pack(side='right')
    line2Pt2.bind('<Button-1>', buttonFunc(selectionLabel))
    line2Pt1 = tk.Button(botBar, text = 'line2Pt1', width=20, height=2)
    line2Pt1.pack(side='right')
    line2Pt1.bind('<Button-1>', buttonFunc(selectionLabel))
    line1Pt2 = tk.Button(botBar, text = 'line1Pt2', width=20, height=2)
    line1Pt2.pack(side='right')
    line1Pt2.bind('<Button-1>', buttonFunc(selectionLabel))
    line1Pt1 = tk.Button(botBar, text = 'line1Pt1', width=20, height=2)
    line1Pt1.pack(side='right')
    line1Pt1.bind('<Button-1>', buttonFunc(selectionLabel))

    R.bind('<Button-1>', removeButton(pointsDict, selectionLabel, panel))

    window.mainloop()

    return pointsDict


if __name__ == '__main__':
    import pickle
    imgDir = './samples/views/45.jpg'
    pointsDict = collectPoints(imgDir)
    # print(np.array(list(zip(pointsDict.keys(), pointsDict.values()))))
    print(pointsDict)

    # f = open('pitchPointsData.dat', 'rb')
    # pointsDict = pickle.load(f)
    # f.close()
    # for k,v in pointsDict.items():
    #     if v!=(-1,-1):
    #         pointsDict[k] = (int(pointsDict[k][0]*0.667), int(pointsDict[k][1]*0.667))
    # f = open('pitchPointsData.dat', 'wb')
    # pickle.dump(pointsDict, f)
    # f.close()

    # import os
    # import pickle
    #
    # paraPerDict = {}
    #
    # for i in range(1,11):
    #     paraPerDict[i] = []
    #
    # for dir_num in range(1,11):
    #     imgDir = './cornerImgs/imgs'+str(dir_num)+'/'
    #     filenames = sorted(os.listdir(imgDir))
    #     dbDir = '../DB/data{0}.db'.format(dir_num)
    #
    #     for filename in filenames:
    #         pointsDict = collectPoints(imgDir+filename)
    #         paraPerDict[dir_num].append(paraPerAngle(pointsDict))
    #
    # print(paraPerDict)
    # f = open('paraPerData.dat', 'wb')
    # pickle.dump(paraPerDict, f)
    # f.close()
