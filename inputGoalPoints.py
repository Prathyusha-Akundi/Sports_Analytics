import tkinter as tk
from PIL import ImageTk, Image
import numpy as np

def prepareLists():
    leftGoalPoints = ['leftGoalPostTopLeftPoint', 'leftGoalPostTopRightPoint', 'leftGoalPostBottomLeftPoint', 'leftGoalPostBottomRightPoint']
    rightGoalPoints = ['rightGoalPostTopLeftPoint', 'rightGoalPostTopRightPoint', 'rightGoalPostBottomLeftPoint', 'rightGoalPostBottomRightPoint']

    return ('leftGoalPoints', leftGoalPoints), ('rightGoalPoints', rightGoalPoints)


def prepareDict(dic, pointsList):
    for sometuple in pointsList:
        for point in sometuple[1]:
            dic[point] = (-1,-1)

    return dic

def redrawPoints(panel, dic):
    panel.delete('marker')
    for key in dic.keys():
        x, y = dic[key]
        x = x*1280//1920
        y = y*720//1080
        panel.create_oval(x-5, y-5, x+5, y+5, fill='red', tag='marker')

def updateDict(dic, selectionLabel, panel):
    def setDictVal(event):
        mouseX = event.x*1920//1280
        mouseY = event.y*1080//720
        if selectionLabel.cget('text') != 'None':
            dic[selectionLabel.cget('text')] = (mouseX, mouseY)
            redrawPoints(panel, dic)
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


def collectPoints(imgDir, pointsDict):
    window = tk.Tk()
    window.title("inputPoints")
    window.geometry("1510x720")
    window.configure(background='grey')
    im = Image.open(imgDir)
    im.thumbnail((1280, 720), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(im)

    buttonsFrame = tk.Frame(window)
    buttonsFrame.pack(side='right')

    pointsList = prepareLists()
    if pointsDict == {}:
        pointsDict = prepareDict(pointsDict, pointsList)

    L = tk.Label(buttonsFrame, text = 'Currently Selected', width=25, bg='black', fg='white')
    L.pack(side='top')
    selectionLabel = tk.Label(buttonsFrame, text='None', width=25)
    selectionLabel.pack(side='top')

    R = tk.Button(buttonsFrame, text = 'REMOVE', width=25, bg='red4', fg='white')
    R.pack(side = 'bottom')

    for sometuple in pointsList:
        for point in sorted(sometuple[1], key=len)[::-1]:
            B = tk.Button(buttonsFrame, text = point, width=25)
            B.pack(side = 'bottom')
            B.bind('<Button-1>', buttonFunc(selectionLabel))
        L = tk.Label(buttonsFrame, text = sometuple[0], width=25, bg='black', fg='white')
        L.pack(side='bottom')

    panel = tk.Canvas(window)
    panel.bind('<Button-1>', updateDict(pointsDict, selectionLabel, panel))
    panel.pack(side = "left", fill = "both", expand = "yes")
    panel.create_image(1280//2,720//2, image=img)
    R.bind('<Button-1>', removeButton(pointsDict, selectionLabel, panel))

    window.mainloop()

    return pointsDict


def goalRatioCalculator(top1, top2, bottom1, bottom2):
    top1, top2, bottom1, bottom2 = np.array(top1), np.array(top2), np.array(bottom1), np.array(bottom2)
    topLeftRatio = np.linalg.norm(top1-top2)/np.linalg.norm(top1-bottom1)
    leftRightRatio = np.linalg.norm(top1-bottom1)/np.linalg.norm(top2-bottom2)

    def angle(pt1, pt2):
        return np.arctan((pt2[1]-pt1[1])/(pt2[0]-pt1[0]))*180/np.pi

    goalLineAngle = angle(top1, top2)
    goalLineAngleRange = [goalLineAngle-4, goalLineAngle+4]

    return topLeftRatio, leftRightRatio, goalLineAngleRange


if __name__ == '__main__':
    import os
    import pickle
    f = open('goalData '+"(empty)"+'.dat', 'rb')
    goalDict = pickle.load(f)
    f.close()
    print(goalDict)

    for dir_num, goalData in goalDict.items():
        print(dir_num)
        # goalData = np.array(goalData)
        goalData = np.array([item for sublist in goalData for subsublist in sublist for item in subsublist])
        if (goalData.flatten() == 0).any():
            imgDir = './goalImgs/imgs'+str(dir_num)+'/'
            filenames = sorted(os.listdir(imgDir))
            dbDir = '../DB/data{0}.db'.format(dir_num)
            goalPoints = collectPoints(imgDir+filenames[0], {})
            goalPoints = collectPoints(imgDir+filenames[1], goalPoints)
            print(goalPoints)
            [lbottom1, lbottom2, ltop1, ltop2, rbottom1, rbottom2, rtop1, rtop2] = [goalPoints[x] for x in sorted(goalPoints.keys())]
            if (np.array(goalPoints.values()) == (-1,-1)).any():
                pass
            else:
                topLeftRatio1, leftRightRatio1, goalLineAngleRange1 = goalRatioCalculator(ltop1, ltop2, lbottom1, lbottom2)
                topLeftRatio2, leftRightRatio2, goalLineAngleRange2 = goalRatioCalculator(rtop1, rtop2, rbottom1, rbottom2)

                goalDict[dir_num] = [[[topLeftRatio1], [topLeftRatio2]], [[leftRightRatio1], [leftRightRatio2]], [goalLineAngleRange1, goalLineAngleRange2]]

    print(goalDict)
    f = open('goalData.dat', 'wb')
    pickle.dump(goalDict, f)
    f.close()
