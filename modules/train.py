import os
from sklearn.externals import joblib


#one input is dataset, the other is 
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
            return ""

    script_string = "python3 "+ os.path.realpath(__file__) + " "+options['workdir']
    return script_string



def data(workdir, channel, **options):
    return {
        'datatype' : 'model',
        'model': joblib.load(workdir+"/trained.pkl")
    }
    


if __name__ == "__main__":
    import sys
    import numpy as np
    from sklearn.externals import joblib

    workdir = sys.argv[1]

    data = np.load(workdir+"/data.npy")
    target = np.load(workdir+"/target.npy")
    classifier = joblib.load(workdir+"/svm.pkl")

    classifier.fit(data, target)
    joblib.dump(classifier, workdir+"/trained.pkl")
