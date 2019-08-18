import numpy as np
import cv2

def selectBestMask(mask1, mask2, mask3):
    kernel = np.ones((20,20),np.uint8)
    opened1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, kernel)
    opened2 = cv2.morphologyEx(mask2, cv2.MORPH_OPEN, kernel)
    opened3 = cv2.morphologyEx(mask3, cv2.MORPH_OPEN, kernel)
    openedSums = np.array([np.sum(opened1), np.sum(opened2), np.sum(opened3)])
    masks = np.array([mask1, mask2, mask3])
    maskSums = np.array([np.sum(x) for x in masks])
    maskSums[np.argwhere(openedSums != min(openedSums))] = 0
    mask = masks[np.argwhere(maskSums == max(maskSums))[0][0]]
    return mask




if __name__ == '__main__':
    from lines import *
    img_dir = '../'
    filename = '165.jpg'
    img = cv2.imread(img_dir + filename, 1)

    dir_num = 2
    frameNum = filename.split('.')[0]

    import pickle
    file_Name = "Pickle_File_color_data"
    fileObject = open(file_Name,'rb')
    color_ranges = pickle.load(fileObject)
    ground_color_range=color_ranges['ground_color']
    rangeH=ground_color_range[dir_num-1][0]
    rangeS=ground_color_range[dir_num-1][1]
    rangeV=ground_color_range[dir_num-1][2]

    groundColorMask = rangeToMask(img,[rangeH],[rangeS],[rangeV])

    dbDir = '../DB/data{0}.db'.format(dir_num)
    print(dbDir)
    db = connectDB(dbDir)
    playerData, ballData, goalData = getFrameData(db, frameNum)
    disconnectDB(db)
    playerMask = np.array(getPlayersMask(playerData, ballData))

    thres1, thres2, thres3 = 138, 143, 148
    mask1 = getLineMask(img, groundColorMask, playerMask, thres1)
    mask2 = getLineMask(img, groundColorMask, playerMask, thres2)
    mask3 = getLineMask(img, groundColorMask, playerMask, thres3)

    mask = selectBestMask(mask1, mask2, mask3)

    if(1):
        cv2.imshow('win', mask1)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        cv2.imshow('win', mask2)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        cv2.imshow('win', mask3)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        cv2.imshow('win', mask)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
