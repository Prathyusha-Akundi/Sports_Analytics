# from imageOperatives import *
from ground_color import getGroundColor,rangeToMask
# from find_inner_boundaries import *
# from find_outline_boundaries import *
# from test_outline_boundary import *
from lines import *
# from end_points import *
# from linesandmag import *
import pickle
import os 
import sys
'''
MAIN FUNCTION REGION BEGINS HERE
'''

'''
Get the ground colour range from
center frame (requires 3 images corresponding to center left, absolute center and center right frames)
(results stored in (left,right), (left1, right1) and (left2, right2))
and white colour ranges from
center frame (requires 3 images corresponding to center left, absolute center and center right frames)
(results stored in white_upperx, white_lowerx and v_thres_overallx),
left frame (requires 1 image)
(results stored in white_uppery, white_lowery and v_thres_overally) and
right frame (requires 1 image)
(results stored in white_upperz, white_lowerz and v_thres_overallz).
'''
caluclate_Ground_color_dictionary=[
['51.jpg','138.jpg','150.jpg','51.jpg','150.jpg'],
['144.jpg','161.jpg','401.jpg','144.jpg','401.jpg'],
['30.jpg','8.jpg','503.jpg','30.jpg','503.jpg'],
['75.jpg','88.jpg','150.jpg','75.jpg','150.jpg'],
['119.jpg','201.jpg','60.jpg','119.jpg','60.jpg'],
['1536.jpg','45.jpg','550.jpg','1536.jpg','550.jpg'],
['1.jpg','186.jpg','200.jpg','1.jpg','200.jpg'],
['385.jpg','246.jpg','1.jpg','385.jpg','1.jpg'],
['136.jpg','107.jpg','72.jpg','136.jpg','72.jpg'],
['1779.jpg','1.jpg','54.jpg','1779.jpg','54.jpg'],
]

os.system("rm -r Ground_Images_Used")
os.system("mkdir Ground_Images_Used")



Ground_color_array=[]
Line_color_array=[]
for file_test_number in range(10):

	## IMAGES URL
	centerL_name = '../Videos/imgs'+str(file_test_number+1)+'/'+caluclate_Ground_color_dictionary[file_test_number][0]
	centerC_name = '../Videos/imgs'+str(file_test_number+1)+'/'+caluclate_Ground_color_dictionary[file_test_number][1]
	centerR_name = '../Videos/imgs'+str(file_test_number+1)+'/'+caluclate_Ground_color_dictionary[file_test_number][2]
	imgL_name    = '../Videos/imgs'+str(file_test_number+1)+'/'+caluclate_Ground_color_dictionary[file_test_number][3]
	imgR_name    = '../Videos/imgs'+str(file_test_number+1)+'/'+caluclate_Ground_color_dictionary[file_test_number][4]
	
	prefix_name="Ground_Images_Used/imgs"+str(file_test_number+1)+"/"
	os.system("mkdir "+prefix_name)
	prefix_name_input_imgs=prefix_name+"/"+"Input"
	prefix_name_output_imgs=prefix_name+"/"+"Output"
	os.system("mkdir "+prefix_name_input_imgs)
	os.system("mkdir "+prefix_name_output_imgs)
	os.system("cp "+centerL_name+" "+prefix_name_input_imgs+"/Left_Image.jpg")
	os.system("cp "+centerC_name+" "+prefix_name_input_imgs+"/Center_Image.jpg")	
	os.system("cp "+centerR_name+" "+prefix_name_input_imgs+"/Right_Image.jpg")

	centerL = cv2.imread(centerL_name)
	# centerL = cv2.cvtColor(centerL, cv2.COLOR_BGR2RGB)
	centerC = cv2.imread(centerC_name)
	# centerC = cv2.cvtColor(centerC, cv2.COLOR_BGR2RGB)
	centerR = cv2.imread(centerR_name)
	# centerR = cv2.cvtColor(centerR, cv2.COLOR_BGR2RGB)
	imgL = cv2.imread(imgL_name)
	# imgL = cv2.cvtColor(imgL, cv2.COLOR_BGR2RGB)
	imgR = cv2.imread(imgR_name)
	# imgR = cv2.cvtColor(imgR, cv2.COLOR_BGR2RGB)

	rangeHL,rangeSL,rangeVL = getGroundColor(centerL)
	rangeHC,rangeSC,rangeVC = getGroundColor(centerC)
	rangeHR,rangeSR,rangeVR = getGroundColor(centerR)
	# print("sadfsahfds",rangeHR,rangeSR,rangeVR,"\n")


	rangeH = [min(rangeHL[0], rangeHC[0], rangeHR[0]), max(rangeHL[1], rangeHC[1], rangeHR[1])]
	rangeS = [min(rangeSL[0], rangeSC[0], rangeSR[0]), max(rangeSL[1], rangeSC[1], rangeSR[1])]
	rangeV = [min(rangeVL[0], rangeVC[0], rangeVR[0]), max(rangeVL[1], rangeVC[1], rangeVR[1])]
	print("GROUND COLOR RANGE :")
	# print("["+str(rangeH)+"],["+str(rangeS)+"],["+str(rangeV)+"]")
	print(rangeH,rangeS,rangeV)

	groundColorMaskCL = rangeToMask(centerL,[rangeH],[rangeS],[rangeV])
	groundColorMaskCC = rangeToMask(centerC,[rangeH],[rangeS],[rangeV])
	groundColorMaskCR = rangeToMask(centerR,[rangeH],[rangeS],[rangeV])

	cv2.imwrite(prefix_name_output_imgs+"/Left_Image.jpg",groundColorMaskCL*255)

	cv2.imwrite(prefix_name_output_imgs+"/Center_Image.jpg",groundColorMaskCC*255)

	cv2.imwrite(prefix_name_output_imgs+"/Right_Image.jpg",groundColorMaskCR*255)


	groundColorMaskL = rangeToMask(imgL,[rangeH],[rangeS],[rangeV])
	groundColorMaskR = rangeToMask(imgR,[rangeH],[rangeS],[rangeV])

	thresC = (getLineRange(centerL,groundColorMaskCL) + getLineRange(centerC,groundColorMaskCC) + getLineRange(centerR,groundColorMaskCR))/3
	thresL = getLineRange(imgL,groundColorMaskL)
	thresR = getLineRange(imgR,groundColorMaskR)
	    
	print("LINE THRESHOLDS : ",thresL,thresC,thresR)
	Ground_color_array.append([rangeH,rangeS,rangeV])
	Line_color_array.append([thresL,thresC,thresR])
	# print(Ground_color_array)
	# print(Line_color_array)

	left_line_output=getLineMask(imgL,groundColorMaskL,thresL)
	center_line_output=getLineMask(centerC,groundColorMaskCC,thresC)
	right_line_output=getLineMask(imgR,groundColorMaskR,thresR)
	
	cv2.imwrite(prefix_name_output_imgs+"/Left_Image_line.jpg",left_line_output)

	cv2.imwrite(prefix_name_output_imgs+"/Center_Image_line.jpg",center_line_output)

	cv2.imwrite(prefix_name_output_imgs+"/Right_Image_line.jpg",right_line_output)

	


Dict_Ground_Lines_color={}
Dict_Ground_Lines_color['ground_color']=Ground_color_array
Dict_Ground_Lines_color['Line color']=Line_color_array

file_Name = "Pickle_File_color_data"
os.system("rm "+file_Name)


fileObject = open(file_Name,'wb') 

pickle.dump(Dict_Ground_Lines_color,fileObject)   

print(Dict_Ground_Lines_color,"colors")
fileObject.close()



fileObject = open(file_Name,'rb')  
# load the object from the file into var b
color_values = pickle.load(fileObject)  

print(color_values,"got it!")

fileObject.close()

'''
TESTING ON FRAMES STARTS HERE
'''





# for z in range(6,180):

#     '''
#     Preparation of stands mask and players mask from the image.
#     Original frames are stored in a folder named 'new' as 'z.jpg' where z denotes an integer.
#     Stands mask is saved in a folder named 'sm' as 'z.jpg' where z is the input image name without extension.
#     Detected lines are saved in a folder named 'l' as 'z.jpg' where z is the input image name without extension.
#     '''
#     print()
#     print(z)
#     img = cv2.imread("../Videos/imgs1/"+str(z)+".jpg", 1)
#     img = cv2.resize(img, (1920, 1080),interpolation= cv2.INTER_AREA )
#     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

#     groundColorMask = rangeToMask(img,[rangeH],[rangeS],[rangeV])

#     nb_components,output,stats,centroids = cv2.connectedComponentsWithStats(groundColorMask,connectivity = 8)
#     sizes = stats[1:,-1]

#     groundMask = np.zeros((output.shape))
#     for i in range(0,nb_components-1):
#         if(sizes[i] >= 100000):
#             groundMask[ output == i+1 ] = 1
#     groundMask = groundMask.astype(np.uint8)

#     kernel = np.ones((100,100),np.uint8)
#     standsMask = cv2.morphologyEx(groundMask, cv2.MORPH_CLOSE, kernel)
#     cv2.imwrite('./testOutput/S'+str(z)+'.jpg', 255*standsMask) 

#     lb,ub = get_case_and_plines(standsMask)
#     print("Lower Bound: ", lb)
#     print("Upper Bound: ", ub)

#     case, para1,para2,per1,per2 = find_inner_boundaries(standsMask,ub,lb)
#     print("Case : ",case)
#     print("Para1, Para2 : ",para1,para2)
#     print("Per1, Per2 : ",per1,per2)

#     if case == 1 or case == 3 or case == 4:
#         lineMask = getLineMask(img,groundColorMask,thresL)
#     elif case == 2 or case == 5 or case == 6:
#         lineMask = getLineMask(img,groundColorMask,thresR)
#     else:
#         lineMask = getLineMask(img,groundColorMask,thresC)
#     cv2.imwrite('./testOutput/L'+str(z)+'.jpg', lineMask) 

#     coords = getEndPoints(lineMask)
#     coords,lines = lineMerge(coords)

#     for cd in coords:
#         cv2.line(img,(cd[0][1],cd[0][0]),(cd[1][1],cd[1][0]),(255,124,124),3)
#     cv2.imwrite('./testOutput/AL'+str(z)+'.jpg', img)    

#     centerLine, sideLine, magnification = final_lines_and_mag(lines,coords,case,para1,para2)

#     print("Magnification : ",magnification)

#     if(len(ub)!=0):
#         for i in range(1,len(ub[0])):
#             cv2.line(img,(int(ub[0][i-1]),int(ub[1][i-1])),(int(ub[0][i]),int(ub[1][i])),(255,0,0),3)

#     if(len(lb)!=0):
#         for i in range(1,len(lb[0])):
#             cv2.line(img,(int(lb[0][i-1]),int(lb[1][i-1])),(int(lb[0][i]),int(lb[1][i])),(0,0,255),3)

#     if(centerLine!=-1):
#         cv2.line(img, (coords[centerLine][0][1], coords[centerLine][0][0]), (coords[centerLine][1][1], coords[centerLine][1][0]), (255,255,0), 3)
#     if sideLine!=-1:
#         cv2.line(img, (coords[sideLine][0][1], coords[sideLine][0][0]), (coords[sideLine][1][1], coords[sideLine][1][0]), (0,255,0), 3)
       
#     cv2.imwrite('./testOutput/'+str(z)+'.jpg', img)