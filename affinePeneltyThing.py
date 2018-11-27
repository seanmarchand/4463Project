import numpy as np
#Global variables 
S1=""
S2=""
match=0
mismatch=0
gapOpen=0
gapExtend=0
scoreMatrix=None
opened=False
#Calculates the score of an entry in the matrix
def score (matrix, i, j):
	global opened
	#Flag for if it was a match or mismatch
	x=0 
	if S1[i-1]==S2[j-1]:
		x=match
	else:
		x=mismatch
	if not opened:
	#Calculates which direction would be ideal
		upLeft = matrix[i - 1][j - 1] + x
		up   = matrix[i - 1][j] + gapOpen
		left = matrix[i][j-1] + gapOpen
		if up>upLeft or left>upLeft:
		#a gap was opened
			opened=True
	else:
		#We have already opened a gap
		upLeft = matrix[i - 1][j - 1] + x
		up   = matrix[i - 1][j] + gapExtend
		left = matrix[i][j-1] + gapExtend
		if upLeft>up and upLeft>left:
			opened =False
	return max(0,upLeft,up,left)
#Creates the matrix of distance scores
def makeMatrix(row,col):
	matrix = [[0 for i in range(col)] for j in range(row)]
	maxScore=0
	k=None
	for i in range (1,row):
		for j in range (1, col):
			nextt=score(matrix,i,j)
			if nextt> maxScore:
				maxScore=nextt
				k=(i,j)
			matrix[i][j] = nextt
	return matrix, k
def main(sequence1,sequence2,matchValue,mismatchValue,gapOvalue,gapEvalue):
	#gap open +gapextend*length of extension
	#Setting global values
	global S1
	global S2
	global match
	global mismatch
	global gapOpen
	global gapExtend
	global scoreMatrix
	S1=sequence1
	S2=sequence2
	match=matchValue
	mismatch=mismatchValue
	gapOpen=gapOvalue
	gapExtend=gapEvalue
	scoreMatrix =makeMatrix(len(S1)+1,len(S2)+1)[0]
	#Backtrace to find alignment 
#Calling main with inputs (eventually)
main("ATTAA","TAAAG",2,-1,-3,-.5)
#Setting up to backtrace
row=len(S1)
col=len(S2)
ans1=""
ans2=""
ans3=""
nextt=0
print (np.matrix(scoreMatrix))
#Just add a way to handle when it runs into 0,0
while (row!=1 or col!=1):
	nextt=scoreMatrix[row-1][col-1]
	#If we backtrace up
	if scoreMatrix[row][col]==scoreMatrix[row-1][col]-2:
		print "gap up"
		row-=1
		ans1+=S1[row]
		ans2+="-"
		ans3+=" "
	#If we backtrace left
	elif scoreMatrix[row][col]==scoreMatrix[row][col-1]-2:
		print "gap left"
		col-=1
		ans3+=" "
		ans1+="-"
		ans2+=S2[col]
	#If we find a match
	elif scoreMatrix[row][col]==nextt+2:
		print "match"
		row-=1
		col-=1
		ans3+="|"
		ans1+=S1[row]
		ans2+=S2[col]
	#If we find a mismatch
	elif scoreMatrix[row][col]==nextt-1:
		print "mismatch"
		row-=1
		col-=1
		ans3+=" "
		ans1+=S1[row]
		ans2+=S2[col]
	
#If we get to 1,1 we need to check if its a match or mismatch
if scoreMatrix[1][1]==0:
	#We had a mismatch to begin with
	ans3+=" "
	ans1+=S1[row-1]
	ans2+=S2[col-1]
else:
	#We had a match to begin with
	ans3+="|"
	ans1+=S1[row-1]
	ans2+=S2[col-1]

print ans1[::-1]
print ans3[::-1]
print ans2[::-1]


