from module import Module


#node definition area
init 	= Module("init")
final 	= Module("final")
a 		= Module("feature_extraction")
b 		= Module("void")
c 		= Module("void")
d 		= Module("text_printer")
e 		= Module("void")

#edge definition area
init 	>> 		a
init 	>> 		b
a 		>> 		c
b 		>> 		c
c 		>> 		d
c 		>> 		e



#	workflow:
#
# init -----a	 d
#      \     \  /
#   	\	  c 
#	     \   /  \
#          b     e
#
#


