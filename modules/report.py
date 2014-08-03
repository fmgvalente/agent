import numpy as np
import os
import sys

def create_execution_script(**options):

    inputs = options['input']
    scores = []

    for input_element in inputs:
        elem_data = input_element.data()

        if 'datatype' in elem_data:
            if(elem_data['datatype'] == 'test'):
                scores.append(elem_data['score'])
        else:
            return "ERROR: input not expected"

    np.save(options['workdir']+'/scores', scores)

    script_string="python3 "+ os.path.realpath(__file__) + " "+options['workdir']
    return script_string    

def data(workdir, **options):
     pass

if __name__ == "__main__":
    workdir = sys.argv[1]

    scores = np.load(workdir+"/scores.npy")

    with open(workdir+"/report.txt","w") as f:
        f.write("The score R^2 is defined as (1 - u/v), where u is the regression sum of squares ((y_true - y_pred) ** 2).sum() and v is the residual sum of squares ((y_true - y_true.mean()) ** 2).sum(). Best possible score is 1.0, lower values are worse.")
        f.write("\n")

        for v in scores:
            f.write(str(v))
            f.write("\n")

