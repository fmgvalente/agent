from sklearn import svm
from sklearn.externals import joblib


#since this is a very light datatype we do some side effects here
#dont do this, this just saves launching a process
def create_execution_script(**options):
	tmp_options = options #because refs...
	del tmp_options['input']

	workdir = tmp_options['workdir']
	del tmp_options['workdir']

	channel = tmp_options['channel']
	del tmp_options['channel']

	#default values for parameters
	if 'C' not in tmp_options: #regularization
		tmp_options['C'] = 1 	
	if 'kernel' not in tmp_options:
		tmp_options['kernel'] = "rbf"
	if 'gamma' not in tmp_options:
		tmp_options['gamma'] = 3
	if 'cache_size' not in tmp_options:
		tmp_options['cache_size'] = 1000
	if 'probability' not in tmp_options:
		tmp_options['probability'] = False
	if 'class_weight' not in tmp_options:
		tmp_options['class_weight'] = 'auto'

	print("option:"+repr(options))

	classifier = svm.SVC(**tmp_options)
	joblib.dump(classifier, workdir+"/svm.pkl")

	script_string = ""
	return script_string


def data(workdir, channel, **options):
	classifier = joblib.load(workdir+"/svm.pkl") 
	return { 'datatype' : 'model', 'model' : classifier}

