import module


a = Module("feature_extraction")
b = Module("void")
c = Module("void")
d = Module("text_printer")



flow = [("a",["b","c","d"]),("c",["d"])]





if __name__ == "__main__":
	print("testing workflow")
	x = workflow(23,"feature_extraction")
	x.run()
	x.collect()



