import module


a = Module("feature_extraction")
b = Module("void")
c = Module("void")
d = Module("text_printer")


a >> c
b >> c
c >> d
c >> e


#	workflow:
#
#  -->a	   d
#	   \  /
#		c 
#	   /  \
#  -->b    e
#
#


