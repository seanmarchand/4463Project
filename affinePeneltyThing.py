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
highestPos=0
#Calculates the score of an entry in the matrix
def score (matrix,gapMatrix, i, j):
	global opened
	#Flag for if it was a match or mismatch
	x=0 
	if S1[i-1]==S2[j-1]:
		x=match
	else:
		x=mismatch
	extended=False
	upLeft = matrix[i - 1][j - 1] + x
	#Were just opening a gap now
	if gapMatrix[i-1][j]==0:
		up   = matrix[i - 1][j] + gapOpen
	else:
		up   = matrix[i - 1][j] + gapExtend
		extended=True
	if gapMatrix[i][j-1]==0:
		left = matrix[i][j-1] + gapOpen
	else:
		#A gap is already open
		left = matrix[i][j-1] + gapExtend
		extended=True
	#pull from second matrix at smae coordinates to determine if its an extension or new gap
	if (max(0,upLeft,up,left)==up or max(0,upLeft,up,left)==left) and extended==True:
		#Extended a gap
		return max(0,upLeft,up,left), 1
	elif (max(0,upLeft,up,left)==up or max(0,upLeft,up,left)==left) and extended==False:
		#New gap added
		return max(0,upLeft,up,left), 2
	return max(0,upLeft,up,left),0
#Creates the matrix of distance scores
def makeMatrix(row,col):
	matrix = [[0 for i in range(col)] for j in range(row)]
	gapMatrix = [[0 for i in range(col)] for j in range(row)]
	maxScore=0
	k=None
	for i in range (1,row):
		for j in range (1, col):
			nextt=score(matrix,gapMatrix,i,j)
			if nextt[0]> maxScore:
				maxScore=nextt[0]
				k=(i,j)
			matrix[i][j] = nextt[0]
			gapMatrix[i][j]=nextt[1]
	print (np.matrix(gapMatrix))
	return matrix, k
def main(sequence1,sequence2,matchValue,mismatchValue,gapOvalue,gapEvalue):
	global S1
	global S2
	global match
	global mismatch
	global gapOpen
	global gapExtend
	global scoreMatrix
	global highestPos
	S1=sequence1
	S2=sequence2
	match=matchValue
	mismatch=mismatchValue
	gapOpen=gapOvalue
	gapExtend=gapEvalue
	scoreMatrix,highestPos =makeMatrix(len(S1)+1,len(S2)+1)
main("ATCG","AG",5,-3,-4,-1)
#Setting up to backtrace
row=highestPos[0]
col=highestPos[1]
ans1=""
ans2=""
ans3=""
nextt=0
print highestPos
print (np.matrix(scoreMatrix))
while scoreMatrix[row][col]!=0:
	flag1=0
	flag2=0
	flag3=0
	flag4=0
	flag5=0
	flag6=0
	if scoreMatrix[row][col]==scoreMatrix[row-1][col-1]+match:
		flag1=scoreMatrix[row-1][col-1]
	if scoreMatrix[row][col]== scoreMatrix[row-1][col-1]+mismatch:
		flag2=scoreMatrix[row-1][col-1]
	if scoreMatrix[row][col]==scoreMatrix[row-1][col]+gapOpen:
		flag3=scoreMatrix[row-1][col]
	if scoreMatrix[row][col]==scoreMatrix[row][col-1]+gapOpen:
		flag4=scoreMatrix[row][col-1]
	if scoreMatrix[row][col]==scoreMatrix[row-1][col]+gapExtend:
		flag5=scoreMatrix[row-1][col]
	if scoreMatrix[row][col]==scoreMatrix[row][col-1]+gapExtend:
		flag6=scoreMatrix[row][col-1]
	maxx=max(flag1,flag2,flag3,flag4,flag5,flag6)
	if maxx==flag1:
		print "match"
		ans1+=S1[row-1]
		ans2+=S2[col-1]
		row-=1
		col-=1
		ans3+="|"
	elif maxx==flag2:		
		print "mismatch"
		ans1+=S1[row-1]
		ans2+=S2[col-1]
		row-=1
		col-=1
		ans3+=" "
	elif maxx==flag3 or maxx==flag5:
		print "gap up"
		#If we backtrace up
		ans1+=S1[row-1]
		ans2+="-"
		ans3+=" "
		row-=1
	elif maxx==flag4 or maxx==flag6:
		print "gap left"
		#If we backtrace up
		ans2+=S2[col-1]
		ans1+="-"
		ans3+=" "
		col-=1
print ans1[::-1]
print ans3[::-1]
print ans2[::-1]


