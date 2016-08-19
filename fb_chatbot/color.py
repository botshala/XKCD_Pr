def perform():
	T=0
	input(T)
	while T>0:
		N=0
		input(N)
		str=''
		input(str)
		R=0
		G=0
		B=0
		for i in str:
			if i=='R':
				R=R+1
			if i=='G':
				G=G+1
			if i=='B':
				B=B+1
		max=0
		if R>max:
			max=R
		if G>max:
			max=G
		if B>max:
			max=B
		print(str(N-max)+'\n')
		T=T-1
if __name__=="__main__":
	perform()