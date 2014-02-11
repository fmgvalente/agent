


a = module("feature_extraction")
b = module("void")
c = module("void")
d = module("text_printer")



flow = [("a",["b","c","d"]),("c",["d"])]





if __name__ == "__main__":
	print("testing workflow")
	x = workflow(23,"feature_extraction")
	x.run()
	x.collect()



