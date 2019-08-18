python3 test_extensive_outer_boundaries.py

###### README ######


*ground_color.py : Calculates ground color range. Takes colored image as input. Returns H, S, V ranges.

*lines.py : Calculates white line color threshold. Takes colored image as input. Returns threshold value.

*end_points.py : Computes end points of various lines. Takes binary (0/255) image of lines. Returns array of end points.

*merge_lines.py : merges lines, i.e., output of end_points.py

goalLine.py : detects the 4 points on the frame of the goal post. Takes the colored image and the position of goal post from Deep learning output as inputs.
              Returns the topLeft, topRight, bottomLeft and bottomRight points on the goal post respectively.

*inputPoints.py : module for creating Tkinter GUI.

*inputGoalPoints.py : creates a GUI to take input of goal points manually. Images to be stored in 'goalImgs' in parent dir. Saves 'goalData.dat'.
                     If goalDataCollector is not used, set input file to 'goalDataEmpty.dat'

*goalDataCollector.py : Optional file that takes images from 'goalImgs' and tries to compute 'goalData.dat' automatically. Potentially useless.

*dictMaker.py : uses inputPoints.py GUI to take inputs of all keypoints for every match. The files to be used are specified in the code itself. Saves 'pointsDictData.dat'

*pitchMaker.py : uses the 'pointsDictData.dat' file to create new pitches using homography. Also saves a dat file for every pitch containing locations of new points.

*dataCalculator.py : uses the 'pointsDictData.dat' file to compute angles of different lines on the ground for every match. Saves 'matchData.dat'

*find_outline_boundaries.py : computes the outer boundaries for given frame. Takes stands mask and player mask. Returns endpoints of outer boundaries.

*find_inner_boundaries.py : Computes case_in, para and per line information using outer boundaries data

*ellipse_points.py : Finds any two points on the ellipse around the center line, if the center line is visible.

*ellipse_points_mean.py : finds all points on the ellipse, slightly slower code, potentially useless.

*lineIdentification.py : uses the 'pointsDictData.dat' file and the output of lines.py to identify
                        1. 18 yard box line (penalty box line)
                        2. Side Lines (Top and Bottom) on the penalty box *
                        3. Bottom Boundary line
                        4. Center Line
                        * : top side line is only detected if para line is visible and bottom side line is detected only if bottom boundary is visible.
                        Takes output of find_inner_boundaries as input along with output of matchData.dat for the given match.

*threshSelector.py : module which takes white color threshold calculated on left, center and right, and whenever the center part is detected,
                    tries all the three ranges and selects the best one.

*hgraphy.py : dummy code for homography

DLdata.py : modules for connecting/disconnecting to database and for retrieving player mask

*mergeDicts.py : module for taking two dicts (created using GUI), and merging them. Takes two dicts as arguments, and transforms points from second dict to the first one.
                Doesn't change the input dicts, returns the new one.
