from module import Module


#node definition area
init 	= Module("init",0)
final 	= Module("final",1)
a 		= Module("feature_extraction",2)
b 		= Module("void",3)
c 		= Module("void",4)
d 		= Module("text_printer",5)
e 		= Module("void",6)

#edge definition area
init 	>> 		a
init 	>> 		b
a 		>> 		c
b 		>> 		c
c 		>> 		d
c 		>> 		e
e 		>>		final


#	workflow:
#
# init -----a	 d  final
#      \     \  /    /
#   	\	  c     /
#	     \   /  \  /
#          b     e
#
#
