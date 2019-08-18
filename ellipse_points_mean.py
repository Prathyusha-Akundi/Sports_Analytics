import cv2
import numpy as np
from scipy import stats


def getEllipsePoints(lineMask):
    avgs = np.array([[0,0]])
    i = 0
    while i < lineMask.shape[1]:
        arr = np.where(lineMask[:,i] == 255)[0]
        if arr != []:
            avg = (np.min(arr)+ np.max(arr))/2
            # print(avg)
            avgs = np.append(avgs, [[avg, i]], axis=0)
        i+=5

    avgs = avgs[1:]
    # print(avgs)
    avgs_floor = np.floor(avgs[:,0])
    mode = stats.mode(avgs_floor)
    mode = mode[0][0]

    avgs = avgs.astype(np.int_)

    points = []
    for avg in avgs:
        if abs(avg[0]-mode) < 20:
            arr = np.where(lineMask[:,avg[1]] == 255)[0]
            pt = [[avg[1], np.min(arr)], [avg[1], np.max(arr)]]
            points.append(pt)

    return np.array(points)


if __name__ == '__main__':
    import time
    main_img = cv2.imread('../124.png', 0)
    img = main_img
    # img = cv2.resize(img, (960,540))
    time_init = time.time()
    ellipsePts = getEllipsePoints(main_img)
    print('Time: ', time.time()-time_init)

    temp_img = np.squeeze(np.stack((main_img,) * 3, -1))
    for pair in ellipsePts:
        cv2.circle(temp_img, tuple(pair[0]), 2, (0,0,255), -2)
        cv2.circle(temp_img, tuple(pair[1]), 2, (0,255,0), -2)

    cv2.imshow('hmm', temp_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
