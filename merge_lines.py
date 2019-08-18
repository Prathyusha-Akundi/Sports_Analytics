import math
import numpy as np

'''
Input: coords from end_points file.
Output: Combined coords
'''

def checkMergeability(line1, line2, idx):
    # There can be 3 cases of relative positioning for any 2 lines that are candidates for merging
    # Two of the cases where at least one point of 1 line lies within the points of the other line, are always mergeable
    # If two points lie isolated from each other, then they're merged only if they're close (enough)

    line1, line2 = np.array(line1), np.array(line2)
    lines = np.append(line1, line2, axis=0)
    order = np.argsort(lines[:,idx])[:2]

    if set(order) == set([0,1]) or set(order) == set([2,3]):
        middlePt1, middlePt2 = lines[np.argsort(lines[:,idx])[1:3]]
        if np.linalg.norm(middlePt1 - middlePt2) < 200:
            return 1
        else:
            return 0
    elif set(order) == set([0,2]) or set(order) == set([1,3]):
        return 1
    elif set(order) == set([1,2]) or set(order) == set([0,3]):
        return 1
    else:
        raise Exception('Error in merging...')


def lineMerge(coords):
    '''
    lines contains the slope and intercept of corresponding line in coords in the form [m,c]
    '''

    lines=[]
    for point in coords:
      if(point[0][1]==point[1][1]):
          m=1e9
          c=point[0][0]-point[0][1]*m
      else:
          m = (point[1][0]-point[0][0])/(point[1][1]-point[0][1])
          c = point[0][0]-point[0][1]*m
      lines.append([m,c])
    # print("LINEs before : ",lines)
    # print("COORDS BEFORE:", coords)
    '''
    Merging of elements in lines and coords with almost same slopes and intercepts.
    Detection of center line index depending on slope (at least 80 degrees), minimum length (atleast 300) and choosing longest of all such lines.
    Center line index is -1 if no such line is detected.
    If center line is detected, removal of all lines which intesect center line at y>0 takes place.
    If center line is detected and lies comfortably in left/right part of the frame, then lines with positive/negative (actually negative/positive) slopes are removed.
    The points on the detected lines are plotted on them and stored as an image in a folder named 'ep' as 'z.png' where z is the input image name without extension.
    '''

    ep_m=15*(math.pi)/180
    ep_c = 20
    groupLabels = [0 for i in range(len(coords))]
    see_len=len(coords)
    for i in range(see_len):
        for j in range(i+1, see_len):
            x_s = [coords[i][0][1],coords[i][1][1],coords[j][0][1],coords[j][1][1]]
            x_s.sort()
            x_op = (x_s[1] + x_s[2])/2
            y_1= x_op * lines[i][0] + lines[i][1]
            y_2= x_op * lines[j][0] + lines[j][1]

            y_s = [coords[i][0][0],coords[i][1][0],coords[j][0][0],coords[j][1][0]]
            y_s.sort()
            y_op = (y_s[1] + y_s[2])/2
            x_1= (y_op - lines[i][1])/lines[i][0] if lines[i][0] != 0 else np.inf
            x_2= (y_op - lines[j][1])/lines[j][0] if lines[j][0] != 0 else np.inf

            m_1=lines[i][0]
            m_2=lines[j][0]
            if(abs(lines[i][0])>=5.67):
              m_1 = abs(m_1)
            if(abs(lines[j][0])>=5.67):
              m_2 = abs(m_2)
            if(abs(math.atan(m_1)-math.atan(m_2))<ep_m and groupLabels[i]==0 and groupLabels[j]==0):
                if(abs(m_1)>=5.67 and abs(m_2)>=5.67 and abs(x_1 - x_2)<ep_c):
                    mergeable = checkMergeability(coords[i], coords[j], 0)
                    if mergeable == 0:
                        continue
                elif((abs(m_1)<5.67 or abs(m_2)<5.67) and abs(y_1 - y_2)<ep_c):
                    mergeable = checkMergeability(coords[i], coords[j], 1)
                    if mergeable == 0:
                      continue
                else:
                    continue


                pnt = np.append(coords[i], coords[j], axis=0)
                pnt = sorted(pnt, key = lambda x : x[0])
                pnt = np.array([pnt[0], pnt[-1]])

                coords[i]=pnt
                if(pnt[0][1]==pnt[1][1]):
                  m=1e9
                  c=pnt[0][0]-pnt[0][1]*m
                else:
                  m = (pnt[1][0]-pnt[0][0])/(pnt[1][1]-pnt[0][1])
                  c = pnt[0][0]-pnt[0][1]*m

                lines[i]=[m,c]
                groupLabels[j]=1

    coords1=[]
    lines1=[]
    for i in range(len(groupLabels)):
      if(groupLabels[i]==0):
          coords1.append(coords[i])
          lines1.append(lines[i])

    ###############


    coords = coords1
    lines = lines1
    # print("LINES : ",lines)
    # print("COORDS : ",coords)
    return np.array(coords), np.array(lines)


if __name__ == '__main__':
    coords = np.array([[[1,1], [2,2]], [[200,200], [400,400]]])
    lineMerge(coords)
