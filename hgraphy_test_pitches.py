import cv2
import numpy as np
from copy import deepcopy
import os
import pickle
imgsDict = {'imgs1': ['66.jpg','92.jpg','143.jpg','149.jpg'],
                'imgs2': ['146.jpg','326.jpg','225.jpg','232.jpg'],
                'imgs3': ['28.jpg','306.jpg','2326.jpg','1696.jpg'],
                'imgs4': ['50.jpg', '77.jpg', '90.jpg', '314.jpg'],
                'imgs5': ['510.jpg','519.jpg','74.jpg','68.jpg'],
                'imgs6': ['228.jpg', '214.jpg', '840.jpg', '747.jpg'],
                'imgs7': ['198.jpg','191.jpg','181.jpg','2.jpg'],
                'imgs8': ['462.jpg','1022.jpg','234.jpg','214.jpg'],
                'imgs9': [],
                'imgs10': ['439.jpg','968.jpg','1068.jpg','613.jpg']}

rootFolder = '../../Videos/'



f = open('pointsDictData.dat', 'rb')
pointsDicts = pickle.load(f)
f.close()

hGraphyPtsLeft = ['leftBoxTopLeftCorner','leftBoxTopRightCorner', 'leftBoxBottomLeftCorner', 'leftBoxBottomRightCorner']
hGraphyPtsRight = ['rightBoxTopLeftCorner', 'rightBoxTopRightCorner', 'rightBoxBottomLeftCorner', 'rightBoxBottomRightCorner']


for filename, pointsDictList in pointsDicts.items():
    imgs=imgsDict[str(filename)]

    if(filename=="imgs7"):
        f = open('./pitches/'+str(filename)+'.dat', 'rb')
        pitchpointsDict = pickle.load(f)
        f.close()

        os.system("rm -r "+"./pitches/check_homography/"+str(filename))
        os.system("mkdir "+"./pitches/check_homography/"+str(filename))

        for i in range(2):
            hGraphyPts = hGraphyPtsLeft if i == 0 else hGraphyPtsRight
            image_name = imgs[0] if i==0 else imgs[3]

            im_src = cv2.imread(rootFolder+"/"+str(filename)+"/"+image_name)
            im_dst= cv2.imread("./pitches/"+str(filename)+".jpg")

            pointsDict = pointsDictList[3*i]
            
            imgPoints = np.array([pointsDict[x] for x in hGraphyPts])
            pitchPoints = np.array([pitchpointsDict[x] for x in hGraphyPts])
            h, status = cv2.findHomography(imgPoints, pitchPoints)

            im_dst1 = cv2.warpPerspective(im_src, h, (im_dst.shape[1], im_dst.shape[0]))
            
            cv2.imwrite("./pitches/check_homography/"+str(filename)+"/"+str("i_")+image_name,im_src)
            cv2.imwrite("./pitches/check_homography/"+str(filename)+"/"+image_name,im_dst+im_dst1)


# def mapPoint(pt, h):
#     pt1 = np.array([pt[0], pt[1], 1])
#     pt1 = np.reshape(pt1, (3,1))
#     pt2 = np.matmul(h, pt1)
#     pt2 = pt2 / pt2[2][0]
#     pt2 = pt2.astype(np.int_)
#     pt2 = [pt2[0][0], pt2[1][0]]
#     return np.array(pt2)

# h, status = cv2.findHomography(pts_src, pts_dst)

# for k, pt in ptsDict.items():
#     mappedPt = mapPoint(pt, h)
#     cv2.circle(im_dst, (mappedPt[0], mappedPt[1]), 2, (0,0,255), -2)




    
    
        









