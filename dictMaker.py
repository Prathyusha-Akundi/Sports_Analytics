from inputPoints import collectPoints
from mergeDicts import mergeDicts

def makeDicts(rootFolder, imgsDict, pointsDict):
    if pointsDict == {}:
        for folder in imgsDict.keys():
            pointsDict[folder] = []

    for folder, imgs in imgsDict.items():
        print(folder)
        if len(imgs) == 4:
            dicts = []
            for img in imgs:
                imgDir = rootFolder + folder + '/' + img
                dic = collectPoints(imgDir)
                print(dic)
                print("\n")
                dicts.append(dic)
            [lDict, lcDict, rcDict, rDict] = dicts
            # 6lDict= {'topLeftCorner': (1068, 19), 'topRightCorner': (-1, -1), 'bottomLeftCorner': (-820, 707), 'bottomRightCorner': (-1, -1), 'centerTopPoint': (-1, -1), 'centerBottomPoint': (-1, -1), 'topLeftIntersection': (1707, 63), 'topRightIntersection': (-1, -1), 'bottomLeftIntersection': (211, 867), 'bottomRightIntersection': (-1, -1), 'leftGoalPostLeftPoint': (301, 303), 'leftGoalPostRightPoint': (492, 235), 'rightGoalPostLeftPoint': (-1, -1), 'rightGoalPostRightPoint': (-1, -1), 'leftBoxTopLeftCorner': (837, 108), 'leftBoxTopRightCorner': (1521, 163), 'leftBoxBottomLeftCorner': (-210, 489), 'leftBoxBottomRightCorner': (700, 604), 'rightBoxTopLeftCorner': (-1, -1), 'rightBoxTopRightCorner': (-1, -1), 'rightBoxBottomLeftCorner': (-1, -1), 'rightBoxBottomRightCorner': (-1, -1), 'ellipseTopPoint': (-1, -1), 'ellipseBottomPoint': (-1, -1), 'ellipseLeftPoint': (-1, -1), 'ellipseRightPoint': (-1, -1), 'exttopLeftCorner': (1106, 1), 'exttopLeftIntersection': (1752, 39), 'exttopCenterIntersection': (-1, -1), 'exttopRightIntersection': (-1, -1), 'exttopRightCorner': (-1, -1)}
            # 6lcDict= {'topLeftCorner': (-1, -1), 'topRightCorner': (-1, -1), 'bottomLeftCorner': (-1, -1), 'bottomRightCorner': (-1, -1), 'centerTopPoint': (1662, 97), 'centerBottomPoint': (1632, 1042), 'topLeftIntersection': (303, 49), 'topRightIntersection': (-1, -1), 'bottomLeftIntersection': (-1, -1), 'bottomRightIntersection': (-1, -1), 'leftGoalPostLeftPoint': (-1, -1), 'leftGoalPostRightPoint': (-1, -1), 'rightGoalPostLeftPoint': (-1, -1), 'rightGoalPostRightPoint': (-1, -1), 'leftBoxTopLeftCorner': (-1, -1), 'leftBoxTopRightCorner': (129, 145), 'leftBoxBottomLeftCorner': (-1, -1), 'leftBoxBottomRightCorner': (-1, -1), 'rightBoxTopLeftCorner': (-1, -1), 'rightBoxTopRightCorner': (-1, -1), 'rightBoxBottomLeftCorner': (-1, -1), 'rightBoxBottomRightCorner': (-1, -1), 'ellipseTopPoint': (1654, 298), 'ellipseBottomPoint': (1645, 522), 'ellipseLeftPoint': (1170, 387), 'ellipseRightPoint': (-1, -1), 'exttopLeftCorner': (-1, -1), 'exttopLeftIntersection': (336, 30), 'exttopCenterIntersection': (1663, 75), 'exttopRightIntersection': (-1, -1), 'exttopRightCorner': (-1, -1)}
            # 6rcDict= {'topLeftCorner': (-1, -1), 'topRightCorner': (-1, -1), 'bottomLeftCorner': (-1, -1), 'bottomRightCorner': (-1, -1), 'centerTopPoint': (240, 106), 'centerBottomPoint': (279, 1033), 'topLeftIntersection': (-1, -1), 'topRightIntersection': (1585, 85), 'bottomLeftIntersection': (-1, -1), 'bottomRightIntersection': (-1, -1), 'leftGoalPostLeftPoint': (-1, -1), 'leftGoalPostRightPoint': (-1, -1), 'rightGoalPostLeftPoint': (-1, -1), 'rightGoalPostRightPoint': (-1, -1), 'leftBoxTopLeftCorner': (-1, -1), 'leftBoxTopRightCorner': (-1, -1), 'leftBoxBottomLeftCorner': (-1, -1), 'leftBoxBottomRightCorner': (-1, -1), 'rightBoxTopLeftCorner': (1741, 177), 'rightBoxTopRightCorner': (-1, -1), 'rightBoxBottomLeftCorner': (-1, -1), 'rightBoxBottomRightCorner': (-1, -1), 'ellipseTopPoint': (252, 300), 'ellipseBottomPoint': (264, 522), 'ellipseLeftPoint': (-1, -1), 'ellipseRightPoint': (730, 397), 'exttopLeftCorner': (-1, -1), 'exttopLeftIntersection': (-1, -1), 'exttopCenterIntersection': (237, 85), 'exttopRightIntersection': (1548, 64), 'exttopRightCorner': (-1, -1)}
            # 6rDict= {'topLeftCorner': (-1, -1), 'topRightCorner': (664, 112), 'bottomLeftCorner': (-1, -1), 'bottomRightCorner': (2409, 768), 'centerTopPoint': (-1, -1), 'centerBottomPoint': (-1, -1), 'topLeftIntersection': (-1, -1), 'topRightIntersection': (57, 141), 'bottomLeftIntersection': (-1, -1), 'bottomRightIntersection': (1465, 898), 'leftGoalPostLeftPoint': (-1, -1), 'leftGoalPostRightPoint': (-1, -1), 'rightGoalPostLeftPoint': (1197, 315), 'rightGoalPostRightPoint': (1368, 381), 'leftBoxTopLeftCorner': (-1, -1), 'leftBoxTopRightCorner': (-1, -1), 'leftBoxBottomLeftCorner': (-1, -1), 'leftBoxBottomRightCorner': (-1, -1), 'rightBoxTopLeftCorner': (238, 238), 'rightBoxTopRightCorner': (879, 195), 'rightBoxBottomLeftCorner': (1012, 654), 'rightBoxBottomRightCorner': (1851, 558), 'ellipseTopPoint': (-1, -1), 'ellipseBottomPoint': (-1, -1), 'ellipseLeftPoint': (-1, -1), 'ellipseRightPoint': (-1, -1), 'exttopLeftCorner': (-1, -1), 'exttopLeftIntersection': (-1, -1), 'exttopCenterIntersection': (-1, -1), 'exttopRightIntersection': (16, 120), 'exttopRightCorner': (613, 94)}
            # 3lDict={'topLeftCorner': (1029, 291), 'topRightCorner': (-1, -1), 'bottomLeftCorner': (-1308, 553), 'bottomRightCorner': (-1, -1), 'centerTopPoint': (-1, -1), 'centerBottomPoint': (-1, -1), 'topLeftIntersection': (1456, 315), 'topRightIntersection': (-1, -1), 'bottomLeftIntersection': (-661, 685), 'bottomRightIntersection': (-1, -1), 'leftGoalPostLeftPoint': (283, 376), 'leftGoalPostRightPoint': (495, 349), 'rightGoalPostLeftPoint': (-1, -1), 'rightGoalPostRightPoint': (-1, -1), 'leftBoxTopLeftCorner': (849, 316), 'leftBoxTopRightCorner': (1284, 345), 'leftBoxBottomLeftCorner': (-364, 446), 'leftBoxBottomRightCorner': (255, 526), 'rightBoxTopLeftCorner': (-1, -1), 'rightBoxTopRightCorner': (-1, -1), 'rightBoxBottomLeftCorner': (-1, -1), 'rightBoxBottomRightCorner': (-1, -1), 'ellipseTopPoint': (-1, -1), 'ellipseBottomPoint': (-1, -1), 'ellipseLeftPoint': (-1, -1), 'ellipseRightPoint': (-1, -1), 'exttopLeftCorner': (1048, 289), 'exttopLeftIntersection': (1473, 309), 'exttopCenterIntersection': (-1, -1), 'exttopRightIntersection': (-1, -1), 'exttopRightCorner': (-1, -1)}


            # 3lcDict={'topLeftCorner': (-1, -1), 'topRightCorner': (-1, -1), 'bottomLeftCorner': (-1, -1), 'bottomRightCorner': (-1, -1), 'centerTopPoint': (1837, 265), 'centerBottomPoint': (1817, 1175), 'topLeftIntersection': (702, 244), 'topRightIntersection': (-1, -1), 'bottomLeftIntersection': (-1, -1), 'bottomRightIntersection': (-1, -1), 'leftGoalPostLeftPoint': (-1, -1), 'leftGoalPostRightPoint': (-1, -1), 'rightGoalPostLeftPoint': (-1, -1), 'rightGoalPostRightPoint': (-1, -1), 'leftBoxTopLeftCorner': (-1, -1), 'leftBoxTopRightCorner': (492, 276), 'leftBoxBottomLeftCorner': (-1, -1), 'leftBoxBottomRightCorner': (-1, -1), 'rightBoxTopLeftCorner': (-1, -1), 'rightBoxTopRightCorner': (-1, -1), 'rightBoxBottomLeftCorner': (-1, -1), 'rightBoxBottomRightCorner': (-1, -1), 'ellipseTopPoint': (1834, 361), 'ellipseBottomPoint': (1831, 501), 'ellipseLeftPoint': (1264, 402), 'ellipseRightPoint': (-1, -1), 'exttopLeftCorner': (-1, -1), 'exttopLeftIntersection': (727, 238), 'exttopCenterIntersection': (1836, 256), 'exttopRightIntersection': (-1, -1), 'exttopRightCorner': (-1, -1)}


            # 3rcDict={'topLeftCorner': (-1, -1), 'topRightCorner': (-1, -1), 'bottomLeftCorner': (-1, -1), 'bottomRightCorner': (-1, -1), 'centerTopPoint': (960, 502), 'centerBottomPoint': (966, 990), 'topLeftIntersection': (-1, -1), 'topRightIntersection': (1542, 502), 'bottomLeftIntersection': (-1, -1), 'bottomRightIntersection': (-1, -1), 'leftGoalPostLeftPoint': (-1, -1), 'leftGoalPostRightPoint': (-1, -1), 'rightGoalPostLeftPoint': (-1, -1), 'rightGoalPostRightPoint': (-1, -1), 'leftBoxTopLeftCorner': (-1, -1), 'leftBoxTopRightCorner': (-1, -1), 'leftBoxBottomLeftCorner': (-1, -1), 'leftBoxBottomRightCorner': (-1, -1), 'rightBoxTopLeftCorner': (1690, 526), 'rightBoxTopRightCorner': (-1, -1), 'rightBoxBottomLeftCorner': (-1, -1), 'rightBoxBottomRightCorner': (-1, -1), 'ellipseTopPoint': (961, 553), 'ellipseBottomPoint': (960, 622), 'ellipseLeftPoint': (-1, -1), 'ellipseRightPoint': (1248, 579), 'exttopLeftCorner': (-1, -1), 'exttopLeftIntersection': (-1,-1), 'exttopCenterIntersection': (960, 496), 'exttopRightIntersection': (1533, 498), 'exttopRightCorner': (-1, -1)}


            # 3rDict={'topLeftCorner': (-1, -1), 'topRightCorner': (180, 447), 'bottomLeftCorner': (-1, -1), 'bottomRightCorner': (3006, 732), 'centerTopPoint': (-1, -1), 'centerBottomPoint': (-1, -1), 'topLeftIntersection': (-1, -1), 'topRightIntersection': (-349, 491), 'bottomLeftIntersection': (-1, -1), 'bottomRightIntersection': (2370, 896), 'leftGoalPostLeftPoint': (-1, -1), 'leftGoalPostRightPoint': (-1, -1), 'rightGoalPostLeftPoint': (946, 510), 'rightGoalPostRightPoint': (1206, 535), 'leftBoxTopLeftCorner': (-1, -1), 'leftBoxTopRightCorner': (-1, -1), 'leftBoxBottomLeftCorner': (-1, -1), 'leftBoxBottomRightCorner': (-1, -1), 'rightBoxTopLeftCorner': (-89, 522), 'rightBoxTopRightCorner': (412, 471), 'rightBoxBottomLeftCorner': (1248, 723), 'rightBoxBottomRightCorner': (1975, 619), 'ellipseTopPoint': (-1, -1), 'ellipseBottomPoint': (-1, -1), 'ellipseLeftPoint': (-1, -1), 'ellipseRightPoint': (-1, -1), 'exttopLeftCorner': (-1, -1), 'exttopLeftIntersection': (-1, -1), 'exttopCenterIntersection': (-1,-1), 'exttopRightIntersection': (-353, 484), 'exttopRightCorner': (160, 442)}

            # 2lDict={'topLeftCorner': (1041, 223), 'topRightCorner': (-1, -1), 'bottomLeftCorner': (-884, 920), 'bottomRightCorner': (-1, -1), 'centerTopPoint': (-1, -1), 'centerBottomPoint': (-1, -1), 'topLeftIntersection': (1689, 253), 'topRightIntersection': (-1, -1), 'bottomLeftIntersection': (198, 1032), 'bottomRightIntersection': (-1, -1), 'leftGoalPostLeftPoint': (270, 501), 'leftGoalPostRightPoint': (462, 433), 'rightGoalPostLeftPoint': (-1, -1), 'rightGoalPostRightPoint': (-1, -1), 'leftBoxTopLeftCorner': (813, 310), 'leftBoxTopRightCorner': (1506, 348), 'leftBoxBottomLeftCorner': (-243, 691), 'leftBoxBottomRightCorner': (682, 780), 'rightBoxTopLeftCorner': (-1, -1), 'rightBoxTopRightCorner': (-1, -1), 'rightBoxBottomLeftCorner': (-1, -1), 'rightBoxBottomRightCorner': (-1, -1), 'ellipseTopPoint': (-1, -1), 'ellipseBottomPoint': (-1, -1), 'ellipseLeftPoint': (-1, -1), 'ellipseRightPoint': (-1, -1), 'exttopLeftCorner': (1086, 205), 'exttopLeftIntersection': (1725, 234), 'exttopCenterIntersection': (-1, -1), 'exttopRightIntersection': (-1, -1), 'exttopRightCorner': (-1, -1)}


            # 2lcDict={'topLeftCorner': (-1, -1), 'topRightCorner': (-1, -1), 'bottomLeftCorner': (-1, -1), 'bottomRightCorner': (-1, -1), 'centerTopPoint': (1603, 205), 'centerBottomPoint': (1581, 1024), 'topLeftIntersection': (270, 180), 'topRightIntersection': (-1, -1), 'bottomLeftIntersection': (-1, -1), 'bottomRightIntersection': (-1, -1), 'leftGoalPostLeftPoint': (-1, -1), 'leftGoalPostRightPoint': (-1, -1), 'rightGoalPostLeftPoint': (-1, -1), 'rightGoalPostRightPoint': (-1, -1), 'leftBoxTopLeftCorner': (-1, -1), 'leftBoxTopRightCorner': (142, 262), 'leftBoxBottomLeftCorner': (-1, -1), 'leftBoxBottomRightCorner': (-1, -1), 'rightBoxTopLeftCorner': (-1, -1), 'rightBoxTopRightCorner': (-1, -1), 'rightBoxBottomLeftCorner': (-1, -1), 'rightBoxBottomRightCorner': (-1, -1), 'ellipseTopPoint': (1597, 378), 'ellipseBottomPoint': (1588, 573), 'ellipseLeftPoint': (1137, 456), 'ellipseRightPoint': (-1, -1), 'exttopLeftCorner': (-1, -1), 'exttopLeftIntersection': (294, 165), 'exttopCenterIntersection': (1602, 187), 'exttopRightIntersection': (-1, -1), 'exttopRightCorner': (-1, -1)}


            # 2rcDict={'topLeftCorner': (-1, -1), 'topRightCorner': (-1, -1), 'bottomLeftCorner': (-1, -1), 'bottomRightCorner': (-1, -1), 'centerTopPoint': (12, 205), 'centerBottomPoint': (41, 1085), 'topLeftIntersection': (-1, -1), 'topRightIntersection': (1411, 163), 'bottomLeftIntersection': (-1, -1), 'bottomRightIntersection': (-1, -1), 'leftGoalPostLeftPoint': (-1, -1), 'leftGoalPostRightPoint': (-1, -1), 'rightGoalPostLeftPoint': (-1, -1), 'rightGoalPostRightPoint': (-1, -1), 'leftBoxTopLeftCorner': (-1, -1), 'leftBoxTopRightCorner': (-1, -1), 'leftBoxBottomLeftCorner': (-1, -1), 'leftBoxBottomRightCorner': (-1, -1), 'rightBoxTopLeftCorner': (1572, 249), 'rightBoxTopRightCorner': (-1, -1), 'rightBoxBottomLeftCorner': (-1, -1), 'rightBoxBottomRightCorner': (-1, -1), 'ellipseTopPoint': (22, 390), 'ellipseBottomPoint': (27, 601), 'ellipseLeftPoint': (-1, -1), 'ellipseRightPoint': (523, 472), 'exttopLeftCorner': (-1, -1), 'exttopLeftIntersection': (-1, -1), 'exttopCenterIntersection': (10, 184), 'exttopRightIntersection': (1383, 147), 'exttopRightCorner': (-1, -1)}


            # 2rDict={'topLeftCorner': (-1, -1), 'topRightCorner': (430, 225), 'bottomLeftCorner': (-1, -1), 'bottomRightCorner': (2556, 953), 'centerTopPoint': (-1, -1), 'centerBottomPoint': (-1, -1), 'topLeftIntersection': (-1, -1), 'topRightIntersection': (-303, 270), 'bottomLeftIntersection': (-1, -1), 'bottomRightIntersection': (1384, 1116), 'leftGoalPostLeftPoint': (-1, -1), 'leftGoalPostRightPoint': (-1, -1), 'rightGoalPostLeftPoint': (1084, 450), 'rightGoalPostRightPoint': (1293, 522), 'leftBoxTopLeftCorner': (-1, -1), 'leftBoxTopRightCorner': (-1, -1), 'leftBoxBottomLeftCorner': (-1, -1), 'leftBoxBottomRightCorner': (-1, -1), 'rightBoxTopLeftCorner': (-103, 375), 'rightBoxTopRightCorner': (694, 319), 'rightBoxBottomLeftCorner': (838, 844), 'rightBoxBottomRightCorner': (1873, 721), 'ellipseTopPoint': (-1, -1), 'ellipseBottomPoint': (-1, -1), 'ellipseLeftPoint': (-1, -1), 'ellipseRightPoint': (-1, -1), 'exttopLeftCorner': (-1, -1), 'exttopLeftIntersection': (-1, -1), 'exttopCenterIntersection': (-1, -1), 'exttopRightIntersection': (-352, 246), 'exttopRightCorner': (372, 205)}



            
            f_lDict = mergeDicts(lDict, lcDict)
            f_lcDict= mergeDicts(lcDict, lDict)
            f_rcDict= mergeDicts(rcDict,rDict)
            f_rDict = mergeDicts(rDict, rcDict)
            
            if (lDict != False and rDict != False ) :
                pointsDicts[folder] = [f_lDict, f_lcDict, f_rcDict, f_rDict]
                print(pointsDicts[folder])
            else:
                pass
        else:
            pass

    return pointsDicts


if __name__ == '__main__':
    import pickle

    f = open('pointsDictData.dat', 'rb')
    pointsDicts = pickle.load(f)
    f.close()
    print(pointsDicts)
    # pointsDict = {}
    #fotmat ['l.jpg', 'cl.jpg', 'cr.jpg', 'r.jpg']
    imgsDict = {
    # 'imgs1': ['66.jpg','699.jpg','954.jpg','149.jpg'],
                # 'imgs2': ['146.jpg','326.jpg','225.jpg','621.jpg'],
                # 'imgs3': ['28.jpg','22.jpg','1343.jpg','1698.jpg'],
                # 'imgs4': ['50.jpg', '77.jpg', '363.jpg', '314.jpg'],
                # 'imgs5': ['510.jpg','508.jpg','73.jpg','71.jpg'],
                # 'imgs6': ['228.jpg', '214.jpg', '840.jpg', '747.jpg'],
                # 'imgs7': ['198.jpg','191.jpg','181.jpg','2.jpg'],
                # 'imgs8': ['462.jpg','1022.jpg','234.jpg','214.jpg'],
                # 'imgs9': [],
                # 'imgs10': ['439.jpg','968.jpg','1068.jpg','613.jpg']
                }

    rootFolder = '../../Videos/'
    pointsDicts = makeDicts(rootFolder, imgsDict, pointsDicts)
    print(pointsDicts)

    f = open('pointsDictData.dat', 'wb')
    pickle.dump(pointsDicts, f)
    f.close()
