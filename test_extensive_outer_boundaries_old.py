from ground_color import *
from find_outline_boundaries import *
from lines import *
import pickle
import os
import sys
from find_inner_boundaries import *
# from line_merge import *
from end_points import *
from goalLine import getGoalLine
from threshSelector import selectBestMask
from lineIdentification import lineIdentification, findIntersections
from ellipse_points import getEllipsePoints

file_Name = "Pickle_File_color_data"

fileObject = open(file_Name,'rb')
# load the object from the file into var b
color_ranges = pickle.load(fileObject)
fileObject.close()

f = open('goalData.dat', 'rb')
goalDict = pickle.load(f)
f.close()

# f = open('paraPerData.dat', 'rb')
# paraPerDict = pickle.load(f)
# f.close()

f = open('matchData.dat', 'rb')
matchDataDict = pickle.load(f)
f.close()

ground_color_range=color_ranges['ground_color']
line_color_range=color_ranges['Line color']

font = cv2.FONT_HERSHEY_SIMPLEX



f = open('pointsDictData.dat', 'rb')
pointsDicts = pickle.load(f)
f.close()







def GetKeyDict(hgraphyDict, pointsDictList, view, viewAngle):

	def transformPoint(pt, refPt, xOffset, yOffset, scaleFactor):
			pt = np.array(pt)
			refPt = refPt + np.array([xOffset, yOffset])
			pt = pt + np.array([xOffset, yOffset])
			newPt = refPt + (pt-refPt)*scaleFactor
			return tuple(newPt.astype(np.int_))

	dict_req={}
	
	if(view=="left"):
		key_list_l=['leftBoxBottomLeftCorner','topLeftCorner','centerTopPoint','ellipseBottomPoint', 'leftGoalPostRightPoint', 'leftGoalPostLeftPoint','leftBoxTopLeftCorner', 'leftBoxTopRightCorner', 'leftBoxBottomRightCorner' ]
	if(view=="right"):
		key_list_r=['rightBoxBottomRightCorner','topRightCorner','centerTopPoint','ellipseBottomPoint','rightGoalPostLeftPoint' , 'rightGoalPostRightPoint','rightBoxTopLeftCorner', 'rightBoxTopRightCorner', 'rightBoxBottomLeftCorner']
	if(view=="center"):
		# key_list_c1=['topLeftCorner', 'leftBoxBottomLeftCorner']
		key_list_c1=[]
		key_list_c2=['topRightCorner', 'rightBoxBottomRightCorner', 'centerTopPoint','ellipseBottomPoint' ]	

	keys_used=list(hgraphyDict.keys())

	print(hgraphyDict)

	a1 = np.array(hgraphyDict[keys_used[0]])
	a2 = np.array(hgraphyDict[keys_used[1]])
	print(a1)
	print(a2)
	# a1=np.flip(a1)
	# a2=np.flip(a2)

	if(view=="left"):

		dict2=pointsDictList[0]
		b1 = np.array(dict2[keys_used[0]])
		b2 = np.array(dict2[keys_used[1]])
		xOffset, yOffset = (a1-b1)[0], (a1-b1)[1]
		scaleFactor = np.linalg.norm(a1-a2)/np.linalg.norm(b1-b2)
		
		refPt = b1
		for key in key_list_l:
			dict_req[key] = transformPoint(dict2[key], refPt, xOffset, yOffset, scaleFactor)


	elif(view=="right"):

		dict2=pointsDictList[1]
		b1 = np.array(dict2[keys_used[0]])
		b2 = np.array(dict2[keys_used[1]])
		xOffset, yOffset = (a1-b1)[0], (a1-b1)[1]
		scaleFactor = np.linalg.norm(a1-a2)/np.linalg.norm(b1-b2)

		refPt = b1
		for key in key_list_r:
			dict_req[key] = transformPoint(dict2[key], refPt, xOffset, yOffset, scaleFactor)


	elif(view=="center"):

		dict2_l=pointsDictList[0]
		dict2_r=pointsDictList[1]

		if(keys_used[0]=="ellipse_center_point"):
			b1 = np.flip(np.array(dict2_l["ellipseBottomPoint"])+np.array(dict2_l["ellipseTopPoint"]))/2
		else:	
			b1 = np.flip(np.array(dict2_l[keys_used[0]]))	
		b2=np.flip(np.array(dict2_l[keys_used[1]]))

		xOffset1, yOffset1 = (a2-b2)[0], (a2-b2)[1]
		scaleFactor1 = np.linalg.norm(a1-a2)/np.linalg.norm(b1-b2)

		refPt = b2
		for key in key_list_c1:
			dict_req[key] = transformPoint(dict2_l[key], refPt, xOffset1, yOffset1, scaleFactor1)



		if(keys_used[0]=="ellipse_center_point"):
			b1 = (np.array(dict2_l["ellipseBottomPoint"])+np.array(dict2_l["ellipseTopPoint"]))/2
			b2=  np.array(dict2_r[keys_used[1]])
			print("nucleus")			
		else:	
			b1 = np.array(dict2_r[keys_used[0]])	
			b2=np.array(dict2_r[keys_used[1]])
		
		# b1=np.flip(b1)
		# b2=np.flip(b2)

		# b1= np.array([ 500, 2304 ])
		# b2= np.array([ 550, -167])
		# a1= np.array([1499.76942477,  895.66485595])
		# a2= np.array([1490.45304947 , 366.96055747])
		
		xOffset2, yOffset2 = (a1-b1)[0], (a1-b1)[1]
		scaleFactor2 = np.linalg.norm(a1-a2)/np.linalg.norm(b1-b2)		
		
		refPt = b1
		print("hello\n")
		print(xOffset2,yOffset2,scaleFactor2,"\n")
		print("p1",transformPoint(b1, refPt, xOffset2, yOffset2, scaleFactor2),b1,a1,"\n")
		print("p2",transformPoint(b2, refPt, xOffset2, yOffset2, scaleFactor2),b2,a2,"\n")


		for key in key_list_c2:
			dict_req[key] = transformPoint(dict2_r[key], refPt, xOffset2, yOffset2, scaleFactor2)	
			print("key",key,dict2_r[key],dict_req[key],"\n")
	return dict_req






def homography_img(img, img_pitch, hgraphyDict, pitchpointsDict, pointsDictList, view, viewAngle):
	# print(pitchpointsDict)
	try:
		keyDict =GetKeyDict(hgraphyDict, pointsDictList, view, viewAngle)
		hGraphyPts =keyDict.keys()
			
		imgPoints = np.array([keyDict[x] for x in hGraphyPts])
		pitchPoints = np.array([pitchpointsDict[x] for x in hGraphyPts])
		
		h, status = cv2.findHomography(imgPoints, pitchPoints)
		im_src= img
		im_dst= img_pitch
		print("Analyze")
		print(hGraphyPts)
		print(imgPoints,pitchPoints)
		# print(im_src.shape)
		# print(im_dst.shape)
		im_dst1 = cv2.warpPerspective(im_src, h, (im_dst.shape[1], im_dst.shape[0]))
	except:
		print("error")
		return img_pitch
	return im_dst1


def line_intersection(a, b):
		line1=a[0]
		line2=np.array([[b[1],b[0]],[b[3],b[2]]])
		# print("a,b\n")
		# print(a,b)
		# print("line_intersection\n")
		# print(line1,line2)
		# print("\n")

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

def point_projection(x,u,v):
	# print(x,u,v)

	n = v - u
	n = n/ np.linalg.norm(n, 2)

	P = u + n*np.dot(x - u, n)
	return P

def ellipse_center_point(ellipsePts, centerLine):
	center_point1=(ellipsePts[0][0]+ellipsePts[1][0])/2
	center_point2=(ellipsePts[0][1]+ellipsePts[1][1])/2
	center_point= point_projection(np.array([int(center_point2),int(center_point1)]),centerLine[0][0],centerLine[0][1])
	return center_point

def sort_top(xy_rev_array):
	array1=xy_rev_array[0]
	array2=xy_rev_array[1]
	if(array1[0]<array2[0]):
		return xy_rev_array[0]
	else:
		return xy_rev_array[1]


def hgraphy_points(img, view, case, ellipsePts, pBoxEndPoints, pBoxLine, sideLines, bottomBoundary, centerLine, upper_bound,lower_bound, goalPoints, para1, para2, per1, per2, viewAngle):
	# print(view, case)
	# print(goalPoints)
	# print(ellipsePts, pBoxEndPoints, pBoxLine, sideLines, bottomBoundary, centerLine, upper_bound,lower_bound)
	# print(pitchpointsDict, pointsDictList)
	if(para2!=[] ):
		Dict_select_list={}
		groundpointsDict_left=pointsDictList[0]
		groundpointsDict_right= pointsDictList[1]
		# print(goalPoints)
		if(view=='left'):
			if(goalPoints!=[] and (goalPoints[3][0]!=0 or goalPoints[3][1]!=0) ):
				if(case==15):
					
					Dict_select_list['leftGoalPostRightPoint']=goalPoints[3]
					Dict_select_list['leftGoalPostLeftPoint']=goalPoints[2]		
				elif(pBoxLine!=[]):
					# print(upper_bound)
					# print("goalPoints\n")
					# print(goalPoints)
					# print("\n")
					Dict_select_list['topLeftCorner']=upper_bound[:,1]
					if(goalPoints[3][0]!=0 or goalPoints[3][1]!=0 ):
						Dict_select_list['leftGoalPostRightPoint']=goalPoints[3]
					else:
						Dict_select_list['leftBoxTopRightCorner']= np.flip(sort_top(pBoxLine[0]))	
			else:
				# print("hello_left\n")
				if(pBoxLine!=[]):
					Dict_select_list['leftBoxTopRightCorner']= np.flip(sort_top(pBoxLine[0]))
					Dict_select_list['topLeftIntersection'] = np.flip(line_intersection([pBoxLine[0]],para2))

		if(view=='right'):
			if(goalPoints!=[] and (goalPoints[3][0]!=0 or goalPoints[3][1]!=0) ):
				if(case==16):
					Dict_select_list['rightGoalPostLeftPoint']=goalPoints[2]
					Dict_select_list['rightGoalPostRightPoint']=goalPoints[3]
							
				elif(pBoxLine!=[]):
					Dict_select_list['topRightCorner']=upper_bound[:,1]
					if(goalPoints[3][0]!=0 or goalPoints[3][1]!=0 ):
						Dict_select_list['rightGoalPostLeftPoint']=goalPoints[2]
					else:
						Dict_select_list['rightBoxTopLeftCorner']= np.flip(sort_top(pBoxLine[0]))	
			else:
				# print("hello_right\n")
				if(pBoxLine!=[]):
					# print(pBoxLine,para2)
					Dict_select_list['rightBoxTopLeftCorner']= np.flip(sort_top(pBoxLine[0]))
					Dict_select_list['topRightIntersection'] = np.flip(line_intersection([pBoxLine[0]],para2))

		if(view=='center'):
			if(centerLine!=[] and ellipsePts!=[] and upper_bound!=[] ):
				# print(ellipsePts,centerLine)
				Dict_select_list['ellipse_center_point']= np.flip(ellipse_center_point(ellipsePts, centerLine))
				Dict_select_list['centerTopPoint']= np.flip(line_intersection(centerLine,para2))
			
			elif(viewAngle=="leftAngles" and pBoxLine!=[]):
				Dict_select_list['leftBoxTopRightCorner']= np.flip(sort_top(pBoxLine[0]))
				# print(para2)
				Dict_select_list['topLeftIntersection'] = np.flip(line_intersection([pBoxLine[0]],para2))

			
			elif(viewAngle=="rightAngles" and pBoxLine!=[]):
				Dict_select_list['rightBoxTopLeftCorner']= np.flip(sort_top(pBoxLine[0]))
				# print(para2)
				Dict_select_list['topRightIntersection'] = np.flip(line_intersection([pBoxLine[0]],para2))
		return(Dict_select_list)

def hgraphy_points_draw(img,dict_draw):
	# print(dict_draw)
	for name, locations in dict_draw.items():
		cv2.putText(img,str(name),(int(locations[0]),int(locations[1])), font, 1,(0,0,255),2,cv2.LINE_AA)
		cv2.circle(img, (int(locations[0]),int(locations[1])), 10, (127,127,127), -10)

	return img



def getLinesFromCoords(coords):
	lines=[]
	for point in coords:
	  if(point[0][1]==point[1][1]):
		  m=1e9
		  c=point[0][0]-point[0][1]*m
	  else:
		  m = (point[1][0]-point[0][0])/(point[1][1]-point[0][1])
		  c = point[0][0]-point[0][1]*m
	  lines.append([m,c])

	  return lines

def Draw_Upper_Lower(img,groundColorMask,stands_mask,dir_name,file_name,upperBound,lowerBound):
	if upperBound != []:
		upperBound = np.fliplr(upperBound.T)
	if lowerBound != []:
		lowerBound = np.fliplr(lowerBound.T)

	if upperBound != []:
		cv2.line(img, tuple(upperBound[0][::-1]),tuple(upperBound[1][::-1]),(255,0,0),5)
		if len(upperBound) > 2:
			cv2.line(img, tuple(upperBound[1][::-1]),tuple(upperBound[2][::-1]),(255,0,0),5)
			cv2.circle(img, tuple(upperBound[1][::-1]), 10, (0,0,255), -10)
	if lowerBound != []:
		cv2.line(img, tuple(lowerBound[0][::-1]),tuple(lowerBound[1][::-1]),(255,0,0),5)
	temp_name=dir_name+"/"+file_name
	img[:,:,0]=img[:,:,0]+stands_mask*127
	img[:,:,1]=img[:,:,1]
	img[:,:,2]=img[:,:,2]#-groundColorMask*127

	return img


def Draw_goal(img, top1, top2, bottom1, bottom2):
	cv2.circle(img, (bottom1[0], bottom1[1]), 3, (255,0,0), -3)
	cv2.circle(img, (bottom2[0], bottom2[1]), 3, (255,0,0), -3)
	cv2.circle(img, (top1[0], top1[1]), 3, (255,0,0), -3)
	cv2.circle(img, (top2[0], top2[1]), 3, (255,0,0), -3)

	blank = np.array(img)
	pts = np.array([top1,top2,bottom2,bottom1], np.int32)
	cv2.fillPoly(blank, pts=[pts], color=(255,0,0))
	img = cv2.addWeighted(img,0.7,blank,0.3,0)

	return img


def Draw_cases_lines(img, dir_name,file_name,case,para_line,per_line,lineMask,coords):
	temp_name=dir_name+"/"+file_name
	# img=cv2.imread(temp_name)
	# print(para_line)
	if(len(para_line)==4):
		# cv2.line(img,(int(para_line[0]),int(para_line[1])-5),(int(para_line[2]),int(para_line[3])-5),(255,255,255),5)
		print_x=int((int(para_line[0])+int(para_line[2]))/2)
		print_y=int((int(para_line[1])+int(para_line[3]))/2)-20
		# print(print_x,print_y)
		cv2.putText(img,'para_line',(print_x,print_y), font, 2,(0,0,255),4,cv2.LINE_AA)
	if(len(per_line)==4):
		# cv2.line(img,(int(per_line[0])-5,int(per_line[1])),(int(per_line[2])-5,int(per_line[3])),(255,255,255),5)
		print_x=int((int(per_line[0])+int(per_line[2]))/2)-20
		print_y=int((int(per_line[1])+int(per_line[3]))/2)
		# print(print_x,print_y)

		cv2.putText(img,'per_line',(print_x,print_y), font, 2,(0,0,255),4,cv2.LINE_AA)

	cv2.putText(img,"case: "+str(case)+" ",(100,100),font,1,(255,255,255),2,cv2.LINE_AA)
	temp_points=np.where(lineMask==255)
	temp_r_real=img[:,:,0]
	temp_r_real[temp_points]=255
	img[:,:,0]=temp_r_real


	temp_r_real=img[:,:,1]
	temp_r_real[temp_points]=255
	img[:,:,1]=temp_r_real

	temp_r_real=img[:,:,2]
	temp_r_real[temp_points]=255
	img[:,:,2]=temp_r_real


	coords=coords.astype('int')
	# print(coords)
	for cd in coords:
		cv2.line(img,(cd[0][1],cd[0][0]),(cd[1][1],cd[1][0]),(0,0,255),3)

	# cv2.imwrite(temp_name,img)



def Draw_filtered_lines(img, dir_name, file_name, coords, color, thickness=3):
	temp_name=dir_name+"/"+file_name

	coords=coords.astype('int')
	# print(coords)
	for cd in coords:
		cv2.line(img,(cd[0][1],cd[0][0]),(cd[1][1],cd[1][0]),color,thickness)
	# cv2.imwrite(temp_name,img)




Master_test_dir="./../../Videos"
Sub_test_dir=os.listdir(Master_test_dir)


Sub_test_dir= sorted(Sub_test_dir,key=lambda x: int(os.path.splitext(x[4:])[0]))
print(Sub_test_dir)
Master_save_outer_boundaries="./Save_outer_boundaries"
os.system("rm -r "+Master_save_outer_boundaries)
os.system("mkdir "+Master_save_outer_boundaries)


for file_test_number in range(6,7):
	print(file_test_number)
	f = open('./pitches/imgs'+str(file_test_number)+'.dat', 'rb')
	pitchpointsDict = pickle.load(f)
	f.close()

	img_pitch= cv2.imread("./pitches/"+"imgs"+str(file_test_number)+".jpg")

	pointsDictList=pointsDicts['imgs'+str(file_test_number)]

	rangeH=ground_color_range[file_test_number-1][0]
	rangeS=ground_color_range[file_test_number-1][1]
	rangeV=ground_color_range[file_test_number-1][2]
	thresL=line_color_range[file_test_number-1][0]
	thresC=line_color_range[file_test_number-1][1]
	thresR=line_color_range[file_test_number-1][2]
	goalDictData = goalDict[file_test_number-1]
	# paraPerData = paraPerDict[dir_test_number+1]
	print(matchDataDict)
	matchData = matchDataDict['imgs'+str(file_test_number)]
	print(matchData)
	goalParams = ([goalDictData[0][0][0], goalDictData[0][1][0]], [goalDictData[1][0][0], goalDictData[1][1][0]], goalDictData[2])
	print(rangeH,rangeS,rangeV,"ground_color_ranges\n")
	print(thresL,thresC,thresR,"line_color_ranges\n")

	Sub_outerboundaries_save_Dir=Master_save_outer_boundaries+"/"+Sub_test_dir[file_test_number-1]
	os.system("mkdir "+Sub_outerboundaries_save_Dir)


	Current_Dir=Master_test_dir+"/"+Sub_test_dir[file_test_number-1]
	print(Current_Dir)
	for files_jpg in sorted(os.listdir(Current_Dir), key = lambda x: int(x.split('.')[0])):
		# print(files_jpg)
		# try:

			file_name_jpg=Current_Dir+"/"+files_jpg
			if(files_jpg[-4:]=='.jpg'):
				print(file_name_jpg)
				
				frameNum = files_jpg.split('.')[0]
				if(int(frameNum)>0):
					try: 
						dbDir = './database_folder/data{0}.db'.format(file_test_number)
						# print(dbDir)
						db = connectDB(dbDir)
						playerData, ballData, goalData = getFrameData(db, frameNum)
						disconnectDB(db)
						playerMask = np.array(getPlayersMask(playerData, ballData))
						goalPoints=[]
						ellipsePts=[]
						pBoxEndPoints=[]
						pBoxLine=[]
						sideLines=[]
						centerLine=[]
						viewAngle=[]

						if 1:
							img = cv2.imread(file_name_jpg)

							time_init = time.time()
							groundColorMask = rangeToMask(img,[rangeH],[rangeS],[rangeV])
							# print('Time_Ground_mask = ', time.time()-time_init , "\n")

							time_init = time.time()
							stands_mask = getStandMask(groundColorMask, playerMask)
							# print('Time_stand_mask = ', time.time()-time_init, "\n")

							# cv2.imshow('hmm', stands_mask*255)
							# cv2.waitKey(0)
							# cv2.destroyAllWindows()
							# cv2.imshow('hmm', playerMask*255)
							# cv2.waitKey(0)
							# cv2.destroyAllWindows()

							time_init = time.time()
							try:
								upper_bound,lower_bound=findOuterBoundaries(stands_mask, playerMask)
							except:
								continue
							# print('Time_lb_ub_mask = ', time.time()-time_init, "\n")

							case, para1, para2, per1, per2 = find_inner_boundaries(upper_bound,lower_bound, goalData)

							if case == 1 or case == 3 or case == 4 or case == 15:
								lineMask = getLineMask(img, groundColorMask, playerMask, thresL)
								white_thres = thresL
								view = 'left'
							elif case == 2 or case == 5 or case == 6 or case == 16:
								lineMask = getLineMask(img, groundColorMask, playerMask, thresR)
								white_thres = thresR
								view = 'right'
							else:
								lineMaskL = getLineMask(img, groundColorMask, playerMask, thresL)
								lineMaskC = getLineMask(img, groundColorMask, playerMask, thresC)
								lineMaskR = getLineMask(img, groundColorMask, playerMask, thresR)
								lineMask = selectBestMask(lineMaskL, lineMaskC, lineMaskR)
								white_thres = thresC
								view = 'center'

							coords = np.array(getEndPoints(lineMask, playerMask))
							# coords,lines = lineMerge(coords)

							if goalData != []:
								bBox = goalData[0]
								top1, top2, bottom1, bottom2 = getGoalLine(img, bBox, white_thres, view, *goalParams)
								goalPoints = [top1, top2, bottom1, bottom2]
								new_upper_bound = improveCorner(img, goalData, upper_bound, goalPoints)
								if len(upper_bound.T) == 3:
									if np.linalg.norm(new_upper_bound.T[1]-upper_bound.T[1]) < 200:
										upper_bound = new_upper_bound
										# print('...updated upper bound...')
								elif len(upper_bound.T) == 2:
									if np.linalg.norm(new_upper_bound.T[0]-upper_bound.T[0]) < 200 and np.linalg.norm(new_upper_bound.T[1]-upper_bound.T[1]) < 200:
										upper_bound = new_upper_bound
										# print('...updated upper bound...')
								img = Draw_goal(img, top1, top2, bottom1, bottom2)

							case, para1, para2, per1, per2 = find_inner_boundaries(upper_bound,lower_bound, goalData)
							lines = getLinesFromCoords(coords)

							pBoxLine, sideLines, bottomBoundary, centerLine , viewAngle= lineIdentification(lines, coords, case, para1, para2, per1, per2, matchData)
							pBoxEndPoints = findIntersections(pBoxLine, sideLines) if pBoxLine != [] else []

							if centerLine != []:
								ellipsePts = getEllipsePoints(lineMask, centerLine, para2, bottomBoundary)
								# print(ellipsePts)
							else:
								ellipsePts = []

							for pt in pBoxEndPoints:
								cv2.circle(img, tuple(pt[::-1]), 10, (0,0,255), -10)

							for pt in ellipsePts:
								cv2.circle(img, tuple(pt), 15, (255,255,0), -15)
								# cv2.circle(img, tuple(pair[1]), 10, (0,255,0), -10)


							img = Draw_Upper_Lower(img,groundColorMask,stands_mask,Sub_outerboundaries_save_Dir,files_jpg,upper_bound,lower_bound)
							Draw_cases_lines(img, Sub_outerboundaries_save_Dir,files_jpg,case,para2,per2,lineMask,coords)
							if sideLines != []:
								Draw_filtered_lines(img, Sub_outerboundaries_save_Dir, files_jpg, sideLines, (255,0,0))
							if bottomBoundary != []:
								cd = bottomBoundary[0]
								cv2.line(img,(cd[0][1],cd[0][0]),(cd[1][1],cd[1][0]),(0,255,255),3)
							if pBoxLine != []:
								Draw_filtered_lines(img, Sub_outerboundaries_save_Dir, files_jpg, pBoxLine, (0,255,0))
							if centerLine != []:
								Draw_filtered_lines(img, Sub_outerboundaries_save_Dir, files_jpg, centerLine, (127,127,255), 10)
							
					except:
						print("error")
					hgraphyDict=hgraphy_points(img, view, case, ellipsePts, pBoxEndPoints, pBoxLine, sideLines, bottomBoundary, centerLine, upper_bound,lower_bound, goalPoints , para1, para2, per1, per2, viewAngle)
					# print(hgraphyDict)
					if(hgraphyDict!=None and hgraphyDict!={} ):
						img=hgraphy_points_draw(img, hgraphyDict)
						
						hgraphy_img=homography_img(img, img_pitch, hgraphyDict, pitchpointsDict, pointsDictList, view, viewAngle)
						
						
						img = cv2.resize(img, dsize=(hgraphy_img.shape[1],hgraphy_img.shape[0]), interpolation=cv2.INTER_CUBIC)

						# print(img.shape)
						# print(hgraphy_img.shape)

						img=np.concatenate((img, hgraphy_img+img_pitch), axis=1)

						
						


					temp_name=Sub_outerboundaries_save_Dir+"/"+files_jpg
					cv2.imwrite(temp_name,img)


						# break
			# except:
			# 	print("Error")
