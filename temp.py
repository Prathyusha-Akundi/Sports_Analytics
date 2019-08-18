from DLdata import *
import numpy as np
import cv2
files_jpg = '122.jpg'
frameNum = files_jpg.split('.')[0]
img= cv2.imread(files_jpg)
dbDir = '../DB/data{0}.db'.format(4)
# print(dbDir)
db = connectDB(dbDir)
playerData, ballData, goalData = getFrameData(db, frameNum)
disconnectDB(db)

for data in playerData:
    print(data)
    cv2.rectangle(img, (data[0], data[1]), (data[2], data[3]), (0,0,255), 2)

cv2.imwrite('playerBoxes.jpg', img)
