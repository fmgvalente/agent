from sklearn.externals import joblib
from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import GaussianNB, MultinomialNB


#since this is a very light datatype we do some side effects here
#dont do this, this just saves launching a process
def create_execution_script(**options):
    #C=2, kernel="rbf", gamma=3, cache_size=1000, probability=False, class_weight='auto'
    tmp_options = options #because refs...
    del tmp_options['input']
    #classifier = svm.SVC(tmp_options)
    classifier = BernoulliNB()
    joblib.dump(classifier, options['workdir']+"/svm.pkl")

    script_string = ""
    return script_string


def data(workdir):
    classifier = joblib.load(workdir+"/svm.pkl") 
    return { 'datatype' : 'model', 'model' : classifier}

