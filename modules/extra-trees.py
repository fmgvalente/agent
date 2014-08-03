from sklearn.externals import joblib
from sklearn.ensemble import ExtraTreesClassifier


#since this is a very light datatype we do some side effects here
#dont do this, this just saves launching a process
def create_execution_script(**options):
    #C=2, kernel="rbf", gamma=3, cache_size=1000, probability=False, class_weight='auto'
    tmp_options = options #because refs...
    del tmp_options['input'] #we need to do so in order to serialize the classifier

    classifier = ExtraTreesClassifier(n_estimators=500, criterion="entropy")
    joblib.dump(classifier, options['workdir']+"/svm.pkl")

    script_string = ""
    return script_string


def data(workdir):
    classifier = joblib.load(workdir+"/svm.pkl") 
    return { 'datatype' : 'model', 'model' : classifier}

