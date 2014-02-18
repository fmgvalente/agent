from module import Module

init = Module("init")
final = Module("final")
a = Module("feature_extraction")
b = Module("void")
c = Module("void")
d = Module("text_printer")
e = Module("void")

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


