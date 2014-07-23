import logging

from sklearn import svm

#   execution_script
#
#   Input:
#       named options
#       state_dir = directory where state and tmp info is stored
#
#   Output:
#       returns a string containg a 
#
#   Invariants:
#   Creates a string containing a script, that, when executed schedules a task
#   for execution on the grid using whatever the grid makes available.

def execution_script(state_dir, input, options):
    logging.info("creating svm script:"+options)
#    file = open(output_dir+"/launch.sh", 'w')

    script = "#!/bin/sh\n"
    script += "#SBATCH --nodes=2\n"
    script += "#SBATCH --partition=gpu.test\n"
    script += "hostname>{}/exec_node\n".format(state_dir)
    script += "sleep 15\n"
    script += "touch {}\n".format(state_dir+"/_state_finished")

    #move to module
    script += "srun hostname>{}/exec_node\n".format(state_dir)
    script += "agent -ud {}".format(state_dir)

#    file.write(script)
#    file.close()

    #subprocess.Popen(["sbatch", output_dir+"/launch.sh"])
    #subprocess.Popen(["sh", output_dir+"/launch.sh"])


def collection_script(state_dir, options):
    print("collect svm from:"+state_dir)


#
#   Custom functionality
#

# Read data points from input file where field contains the
def read_data(filename, field):
    print("Reading file", filename)

    #if os.path.isfile(filename) is False:
    #    print("invalid file: ", filename)
    #    quit()

    #converterDict = dict(map(lambda s: (s, lambda x: 0 if math.isnan(float(x)) else float(x)), range(44)))
    #dataFromFile = np.genfromtxt(filename, delimiter=',', skip_header=1, converters=converterDict)
    #true_class = np.ravel(dataFromFile[:, field:])
    #positive_fraction = (sum(true_class)*100.0) / len(true_class)

    #print("Done!", len(true_class), "data points were read, with", len(dataFromFile[0,:-1]),"features (",positive_fraction,"% positive )")
    #return dataFromFile[:, 5:-1], true_class


def write_data(data, clas, filename="output.txt"):
    #print("\nWriting data to file", filename,"...")
    #print("Num feature:", len(data[0]))
    #print("Num samples:", len(data))

    #with open(filename, "w") as f: 
    #    for i, line in enumerate(data):
    #        for datum in line:
    #            f.write(str(datum) + "\t")
    #        f.write(str(clas[i]) + "\n")

    #print("Done!")
    pass

def train(data, kernel):
    # clf = svm.LinearSVC(C=2.0)
    classifier = svm.SVC(C=2, kernel="rbf", gamma=3, cache_size = 1000, probability=False)
    classifier.fit(data, classifier)
    # print clf.score(data, cla)
    return classifier

def main(inputFile, outputFile, field):

    # read data
#    features, classifications = read_data(inputFile, field)

    kernel = 'rbf'

    print ("Using", kernel, "classifier.")

    if kernel == 'linearsvm':
        clf = svm.SVC(C=2, kernel="rbf", gamma=3, cache_size=1000, probability=False, class_weight='auto') # , class_weight={1: 0.98, 0: 0.02}
    elif classifier == 'linearsvm':
        clf = svm.LinearSVC(C=2)
    else:
        print("Unknown kernel: "+ kernel)
        return

    # Feature importances (from extratrees)
    # clf.fit(data, clas)
    # print clf.feature_importances_ 
    
    steps.append(('svc', clf))

    print ("Creating pipeline...")
    pipe = Pipeline(steps)


    num_folds = 10
    scoring_func = "f1"
    print ("Cross-validating", num_folds, "fold...")
    kfold = xval.StratifiedKFold(y=classifications, n_folds=num_folds)
    
    scores = xval.cross_val_score(estimator=pipe, X=features, y=classifications, cv=kfold, scoring=scoring_func, n_jobs=-1)
    #scores = sum(scores)/len(scores)  # Average scores
    #metrics.confusion_matrix    #score_func=metrics.precision_recall_fscore_support,
    print ("Done!")

    print ("Average %s: %0.3f (+/- %0.3f)" % (scoring_func, scores.mean(), scores.std()*2))

if __name__ == '__main__':
    inputFile = "data.csv"
    outputFile = "out.svm_model"
    learnField = -1 #last element

    i = 1
    while i < len(sys.argv):
        
        if(sys.argv[i] == "-input" and i+1 < len(sys.argv)):
            inputFile = sys.argv[i+1]
            i += 1
            continue

        if(sys.argv[i] == "-output" and i+1 < len(sys.argv)):
            outputFile = sys.argv[i+1]
            i += 1
            continue

        if(sys.argv[i] == "-field" and i+1 < len(sys.argv)):
            learnField = int(sys.argv[i+1])
            i += 1
            continue

        i += 1

    main(inputFile, outputFile, learnField)



if __name__ == "__main__":
    print("no test here for main...")



