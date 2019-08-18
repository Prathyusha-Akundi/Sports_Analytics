'''
Cases:
--- Case #n : (size(lower_bound),size(upper_bound)) left/right side of pitch ---
Case 1: (3,3) left
Case 2: (3,3) right
Case 3: (2,3) left, upper_bound first line is considered
Case 4: (2,3) left, upper_bound first line is not considered
Case 5: (2,3) right, upper_bound second line is considered
Case 6: (2,3) right, upper_bound second line is not considered
Case 7: (2,2) considering only lower_bound for para_lines
Case 8: (3,2) considering only lower_bound for para_lines
Case 9: (3,2) considering only upper_bound for para_lines
Case 10: (1 or 2,2) considering only upper_bound for para_lines
Case 11: (2,0)
Case 12: (3,0) left
Case 13: (3,0) right
'''

def new_case_in(case_in, para_lines, para_lines1, per_lines, per_lines1, goalpost):
    if(len(goalpost==0)):
        return [case_in, para_lines, para_lines1, per_lines, per_lines1]
    else:
        if case_in==1 or or case_in==2 or case_in==3 or case_in==5:
            if goalpost[0]>=per_lines[0] and goalpost[0]<=per_lines[3]:
                return [case_in, para_lines, para_lines1, per_lines, per_lines1]

            else:
                if case_in==1:
                    return [2, per_lines, per_lines1, para_lines, para_lines1]
                elif case_in==2:
                    return [1, per_lines, per_lines1, para_lines, para_lines1]
                elif case_in==3:
                    return [5, per_lines, per_lines1, para_lines, para_lines1]
                else:
                    return [3, per_lines, per_lines1, para_lines, para_lines1]

        else:
            if (goalpost[0]>=para_lines[0] and goalpost[0]>=para_lines[3]) or (goalpost[0]<=para_lines[0] and goalpost[0]<=para_lines[3]):
                return [case_in, para_lines, para_lines1, per_lines, per_lines1]

            else:
                return [15, per_lines, per_lines1, para_lines, para_lines1]
