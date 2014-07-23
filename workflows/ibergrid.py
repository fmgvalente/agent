from module import Module

#node definition area
init	= Module('init',1)
ds		= Module('dataset',2,	src='bcdr_01.csv', truth='last')
split	= Module('split',3,		ratio=0.7, strategy='random')
svm_a   = Module('svm',4,		kernel='rbf', gamma=3)
svm_b   = Module('svm',5,		kernel='linear', c=2)
svm_c   = Module('psvm',6)
nb      = Module('naive_bayes',7)
sgd     = Module('sgd',8)
tree    = Module('extra-trees',9)

train_svm_a    = Module('train', 10, input=[svm_a,split[0]])
train_svm_b    = Module('train', 11, input=[svm_b,split[0]])
train_svm_c    = Module('train', 12, input=[svm_c,split[0]])
train_nb       = Module('train', 13, input=[nb,split[0]])
train_sgd      = Module('train', 14, input=[sgd,split[0]])
train_tree     = Module('train', 15, input=[tree,split[0]])
test_svm_a     = Module('train', 16, input=[train_svm_a, split[1]])
test_svm_b     = Module('train', 17, input=[train_svm_b, split[1]])
test_svm_c     = Module('train', 18, input=[train_svm_c, split[1]])
test_nb        = Module('train', 19, input=[train_nb, split[1]])
test_sgd       = Module('train', 20, input=[train_sgd, split[1]])
test_tree      = Module('train', 21, input=[train_tree, split[1]])
report         = Module('report', 22, input=[test_svm_a, test_svm_b, test_svm_c, test_nb, test_sgd, test_tree])
finit          = Module('finit', 23, input=report)
#edge definition area
#edges can be defined as input = name in module definition area
#or here using operator >>
init   >>   ds
ds     >>   split