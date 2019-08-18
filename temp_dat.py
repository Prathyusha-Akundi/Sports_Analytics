
import pickle


f = open('pointsDictData.dat', 'rb')
pointsDicts = pickle.load(f)
f.close()

newpointsDicts={}


for folder in pointsDicts.keys():
	newpointsDicts[folder] = pointsDicts[folder]

for foldername, dicts in pointsDicts.items():
	print(foldername)
	if(foldername=="imgs3" or foldername== "imgs4" or foldername=="imgs6" or foldername=="imgs2" or foldername=="imgs1" or foldername=="imgs7"):
		points = pointsDicts[foldername]
		for r in range(len(points)):
			temppoints=points[r]

			for k in temppoints.keys():
				temppoints[k] = list(temppoints[k])

			

			if(r==1):
				
				temppoints['bottomLeftIntersection'][1]=temppoints['centerBottomPoint'][1]
				temppoints['bottomLeftCorner'][1]=temppoints['centerBottomPoint'][1]
				
				# temppoints['exttopCenterIntersection'][1]=temppoints['exttopLeftCorner'][1]
				# temppoints['exttopLeftIntersection'][1]=temppoints['exttopLeftCorner'][1]
				

			if(r==2):
				temppoints['bottomRightIntersection'][1]=temppoints['centerBottomPoint'][1]
				temppoints['bottomRightCorner'][1]=temppoints['centerBottomPoint'][1]

				# temppoints['exttopCenterIntersection'][1]=temppoints['exttopRightCorner'][1]
				# temppoints['exttopRightIntersection'][1]=temppoints['exttopRightCorner'][1]


			for k in temppoints.keys():
				temppoints[k] = tuple(temppoints[k])
			newpointsDicts[foldername][r]=temppoints

f = open('temppointsDictData.dat', 'wb')
pickle.dump(pointsDicts, f)
f.close()