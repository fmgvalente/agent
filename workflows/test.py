from Module import *

init = Module("init")
final = Module("final")
a = Module("feature_extraction")
b = Module("void")
c = Module("void")
d = Module("text_printer")

init >> a
init >> b
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


