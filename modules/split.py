import numpy as np
import os

def create_execution_script(**options):

    script_string = "python " + os.path.realpath(__file__)+ " "+options['input'][0].workdir + " " +options['workdir']
    return script_string


#needs to handle more divisions
def data(workdir,**options):
    channel = 0
    if 'channel' in options:
        channel = options['channel']

    if channel==1:
        data = np.load(workdir+"/d1.npy")
        target = np.load(workdir+"/t1.npy")
    else:
        data = np.load(workdir+"/d0.npy")
        target = np.load(workdir+"/t0.npy")

    return {
        'datatype': 'dataset',
        'data': data,
        'target': target,
    }




if __name__ == "__main__":
    import sys
    import numpy as np

    path_to_data = sys.argv[1]
    workdir = sys.argv[2]

    data = np.load(path_to_data+"/data_array.npy")
    target = np.load(path_to_data+"/target.npy")

    split_data = np.array_split(data,2)
    split_target = np.array_split(target,2)

    np.save(workdir+"/d0",split_data[0])
    np.save(workdir+"/t0",split_target[0])
    np.save(workdir+"/d1",split_data[1])
    np.save(workdir+"/t1",split_target[1])
