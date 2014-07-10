from module import Module


#node definition area
init 	= Module("init",0)
final 	= Module("final",1)
a 		= Module("csv",2)
b 		= Module("train_svm",3)
c 		= Module("report",4)

#edge definition area
init 	>> 		a
a 		>> 		b
b 		>> 		c
c 		>>		final


#	workflow:
#
# init -----a	 d  final
#      \     \  /    /
#   	\	  c     /
#	     \   /  \  /
#          b     e
#
#
