import os

def create_execution_script(**options):
    import numpy as np
    from sklearn.externals import joblib

    inputs = options['input']
    channels = options['channel']
    for input_element, input_channel in zip(inputs,channels):
        elem_data = input_element.data(input_channel)


        if 'datatype' in elem_data:
            if(elem_data['datatype'] == 'dataset'):
                np.save(options['workdir']+"/data", elem_data['data'])
                np.save(options['workdir']+"/target", elem_data['target'])
            if(elem_data['datatype'] == 'model'):
                joblib.dump(elem_data['model'], options['workdir']+"/svm.pkl")
        else:
            return "ERROR: input not expected"

    script_string = "python3 "+ os.path.realpath(__file__) + " "+options['workdir']
    return script_string



def data(workdir, channel, **options):
    import numpy as np
    return {
        'datatype':'test',
        'score': np.load(workdir+'/scores.npy')
    }

if __name__ == "__main__":
    import sys
    import numpy as np
    from sklearn.externals import joblib

    workdir = sys.argv[1]

    data = np.load(workdir+"/data.npy")
    target = np.load(workdir+"/target.npy")
    classifier = joblib.load(workdir+"/svm.pkl")

    scores = classifier.score(data, target)
    np.save(workdir+'/scores', scores)

    #num_folds = 10
    #scoring_func = "f1"
    #print ("Cross-validating", num_folds, "fold...")
    #kfold = xval.StratifiedKFold(y=classifications, n_folds=num_folds)
    #scores = xval.cross_val_score(estimator=pipe, X=features, y=classifications, cv=kfold, scoring=scoring_func, n_jobs=-1)
    #np.save(scores)
