from module import Module


#node definition area
init 	= Module("init",0)
final 	= Module("final",1)
a 		= Module("plainzero",2)

#edge definition area
init 	>> 		a
a 		>>		final


