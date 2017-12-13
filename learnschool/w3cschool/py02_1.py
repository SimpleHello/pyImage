#_*_ conding=utf-8 _*_

#两个乒乓球队进行比赛，各出三人。甲队为a,b,c三人，乙队为x,y,z三人。已抽签决定比赛名单。有人向队员打听比赛的名单。a说他不和x比，c说他不和x,z比，请编程序找出三队赛手的名单。
def meth01():
	for i in ["a","b","c"]:
	    for j in ["x","y","z"]:
	            if( i =="a" ) and (j == "x"):
	            	pass
	            elif ( i =="c" ) and ((j == "y") or (j=="z")):
	            	pass
	            else:
	                print i,j

def meth02():
	list = [1,2,3,4]
	print list[2]
	return list


print meth01()