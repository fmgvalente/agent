#!/usr/bin/python

import numpy as np
from sklearn import svm
from sklearn import cross_validation as xval
from sklearn.grid_search import GridSearchCV
from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn import linear_model
#from sklearn.neural_network import BernoulliRBM
from sklearn.neighbors import RadiusNeighborsClassifier, NearestCentroid, KNeighborsClassifier
from sklearn.linear_model.sgd_fast import SquaredLoss, SquaredHinge
from sklearn.lda import LDA
from sklearn.linear_model import SGDClassifier
from sklearn.decomposition import *
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import GradientBoostingClassifier
#from sklearn.ensemble import AdaBoostClassifier
from sklearn.linear_model import RidgeClassifier, Perceptron
from sklearn.feature_selection import *
from sklearn import covariance
from sklearn import cross_validation
from sklearn import linear_model
from sklearn import preprocessing
from sklearn import tree
from sklearn import metrics
from sklearn import hmm
from sklearn.pipeline import Pipeline
from sklearn.utils import check_random_state
from sklearn.externals import joblib
# from mlp import MLPClassifier
import os
import sys
import math
import ast
import random
import pprint


# Read data points from input file where field contains the 
def read_data(filename, field):
    print("Reading file", filename)

    if os.path.isfile(filename) is False:
        print("invalid file: ", filename)
        quit()

    converterDict = dict(map(lambda s: (s, lambda x: 0 if math.isnan(float(x)) else float(x)), range(44)))
    dataFromFile = np.genfromtxt(filename, delimiter=',', skip_header=1, converters=converterDict)
    true_class = np.ravel(dataFromFile[:, field:])
    positive_fraction = (sum(true_class)*100.0) / len(true_class)

    print("Done!", len(true_class), "data points were read, with", len(dataFromFile[0,:-1]),"features (",positive_fraction,"% positive )")
    return dataFromFile[:, 5:-1], true_class


def write_data(data, clas, filename="output.txt"):
    print("\nWriting data to file", filename,"...")
    print("Num feature:", len(data[0]))
    print("Num samples:", len(data))

    with open(filename, "w") as f: 
        for i, line in enumerate(data):
            for datum in line:
                f.write(str(datum) + "\t")
            f.write(str(clas[i]) + "\n")

    print("Done!")


def train(data, cla):
    # clf = svm.LinearSVC(C=2.0)
    clf = svm.SVC(C=2, kernel="rbf", gamma=3, cache_size = 1000, probability=False)
    clf.fit(data, cla)
    # print clf.score(data, cla)
    return clf


def preprocess(data, cla):
    # print "\nScaling and normalizing data..."
    data = preprocessing.scale(data)
    data = preprocessing.normalize(data, norm='l2')
    # data = preprocessing.StandardScaler().fit_transform(data)
    # data = preprocessing.KernelCenterer().fit_transform(data)
    # data = preprocessing.binarize(data)
    # print "Done!"
    return data


def main(inputFile, outputFile, field):

    # read data
    features, classifications = read_data(inputFile, field)

    # preprocess
    # data = preprocess(data, clas)

    #print ("Training...")
    #steps = []
    #steps.append(('scale', preprocessing.StandardScaler()))
    #steps.append(('normalize', preprocessing.Normalizer()))

    #pipe = Pipeline(steps).fit(data)
    #joblib.dump(pipe, 'models/preprocessing_model_no_GO.pkl')
    #data = pipe.transform(data)
    #print ("Done preprocessing")

    #clf =  svm.SVC(C=2, kernel="rbf", gamma=3, cache_size=1000, probability=True, class_weight='auto')
    #clf.fit(data, clas)
    #joblib.dump(clf, 'models/classification_model_svm_no_GO.pkl')
    #print ("Done!")

    #return

    # clf = svm.LinearSVC(C=2, class_weight='auto')
    # clf.fit(data, clas)
    # print clf.coef_
    # print clf.score(data, clas)
    # return

    # Recursive feature elimination test
    # clf = svm.LinearSVC(C=2, class_weight='auto')
    # rfe = RFE(estimator=clf, n_features_to_select=1, step=1)
    # rfe.fit(data, clas)
    # print rfe.ranking_
    # print rfe.score(data, clas)
    # return

    # write_data(data, clas, "balanced_data_scalednormalized.txt")
    # return

    # clf = train(data, clas)
    # for sv in clf.support_vectors_:
    #     pprint.pprint(sv)
    # return

    # Get train and test sets
    # seed = random.randint(1,10000)
    # check_random_state(seed).shuffle(data)
    # check_random_state(seed).shuffle(clas)
    # data_train, data_test, class_train, class_test = cross_validation.train_test_split(data, clas, train_size=0.5, test_size=0.5)

    # Gradient Boosting
    # clf = GradientBoostingClassifier(n_estimators=200).fit(data_train, class_train)
    # print clf.score(data_test, class_test)  
    # return 

    # AdaBoost tests
    # clf2 = svm.SVC(C=2, kernel="rbf", gamma=3, cache_size=1000, probability=True, class_weight='auto') # , class_weight={1: 0.98, 0: 0.02}
    # ada_real = AdaBoostClassifier(base_estimator=clf2, n_estimators=50)
    # ada_real.fit(data_train, class_train)
    # print ada_real.score(data_test, class_test)
    # return


    # print [ "%.6f" % i for i in data[0]]
    # np.set_printoptions(precision=9, suppress=True)

    # pre-process
    # data = preprocess(data, clas)

    # Perform feature selection using linear SVC
    # print "\nPerforming feature selection..."
    # data = svm.LinearSVC().fit_transform(data, clas)
    # selector = SelectPercentile(f_classif, percentile=90)
    # data = selector.fit_transform(data, clas)
    # print "Done!"

    # Shrink data
    # Linear Discriminant Analysis (LDA)
    # clf = LDA(n_components=2)
    # data = clf.fit_transform(X=data, y=clas)

    # PCA
    # for i in xrange(1, 14):
    #     n_comp = i * 10
    #     descomp = NMF(n_components=n_comp)
    #     shrank_data = descomp.fit_transform(data)
    #     shrank_data = preprocess(shrank_data, clas)

    # clf = svm.SVC(C=2.0) # C=2.0, kernel="linear") # clf.cache_size = 1000
    # kfold = xval.StratifiedKFold(y=clas, n_folds=2)
    # rfecv = RFECV(estimator=clf, step=1, cv=kfold, scoring="f1")
    # rfecv.fit(data, clas)
    # print rfecv.ranking_
    # return

    # for i in xrange(1,14):

    # Randomize data to avoid picking the same Folds in the x-validation
    #print ("Shuffling data...")
    seed = random.randint(1,10000)
    check_random_state(seed).shuffle(features)
    check_random_state(seed).shuffle(classifications)

    steps = []

    print ("Creating pre-processing steps...")
    steps.append(('scale', preprocessing.StandardScaler()))
    steps.append(('normalize', preprocessing.Normalizer()))
    # steps.append(('StandardScaler', preprocessing.StandardScaler()))
    # steps.append(('binarize', preprocessing.Binarizer()))

    # print "Creating feature selection step..."
    # steps.append(('PCA', PCA(n_components=i*10)))
    # steps.append(('FastICA', FastICA(n_components=i*10)))
    # steps.append(('FactorAnalysis', FactorAnalysis(n_components=i*10)))
    # steps.append(('SparsePCA', SparsePCA(n_components=i*10)))
    # steps.append(('RandomizedPCA', RandomizedPCA(n_components=130)))

    # print "Performing feature selection with decision trees..."
    # fs = ExtraTreesClassifier(n_estimators=100, criterion="entropy")
    # fs.fit(data, clas)
    # data = fs.transform(data, threshold="0.55*mean")

    print ("Creating classifier step...")
    #classifier = 'svm' # Default to SVM
    classifier = 'SGD'


    print ("Using", classifier,"classifier.")

    if classifier == 'linearsvm':
        clf = svm.SVC(C=2, kernel="rbf", gamma=3, cache_size=1000, probability=False, class_weight='auto') # , class_weight={1: 0.98, 0: 0.02}
    elif classifier == 'bayes':
        clf = BernoulliNB()
    elif classifier == 'extratrees':
        clf = ExtraTreesClassifier(n_estimators=500, criterion="entropy")
    elif classifier == 'decisiontrees':
        clf = tree.DecisionTreeClassifier()
    elif classifier == 'linearsvm':
        clf = svm.LinearSVC(C=2)
    elif classifier == 'SGD':
        clf = SGDClassifier()
    else:
        print ("Unknown classifier in input!")
        return

    # Feature importances (from extratrees)
    # clf.fit(data, clas)
    # print clf.feature_importances_ 
    
    steps.append(('svc', clf))

    print ("Creating pipeline...")
    pipe = Pipeline(steps)


    ####### TESTING ########
    # if (False):
    #     print "Looking for the best parameters..."
    #     clf = svm.SVC(kernel="rbf", cache_size=1000, probability=False)
    #     C_range = np.arange(1, 40) / 10.0
    #     gamma_range = np.arange(1, 50) / 10.0
    #     print gamma_range
    #     param_grid = dict(gamma=gamma_range, C=C_range)
    #     kfold = xval.StratifiedKFold(y=clas, n_folds=5)
    #     grid = GridSearchCV(clf, param_grid=param_grid, cv=kfold, scoring="f1", n_jobs=-1)
    #     grid.fit(data, clas)
    #     print "The best classifier is: ", grid.best_estimator_
    #     print "Best score:", grid.best_score_
    #     print "Best parameters:", grid.best_params_
    #     return
    ########################

    num_folds = 10
    scoring_func = "f1"
    print ("Cross-validating", num_folds, "fold...")
    kfold = xval.StratifiedKFold(y=classifications, n_folds=num_folds)
    
    scores = xval.cross_val_score(estimator=pipe, X=features, y=classifications, cv=kfold, scoring=scoring_func, n_jobs=-1)
    #scores = sum(scores)/len(scores)  # Average scores
    #metrics.confusion_matrix    #score_func=metrics.precision_recall_fscore_support,
    print ("Done!")

    print ("Average %s: %0.3f (+/- %0.3f)" % (scoring_func, scores.mean(), scores.std()*2))

    # score, permutation_scores, pvalue = xval.permutation_test_score(estimator=pipe, X=data, y=clas, cv=kfold, scoring="f1", n_jobs=-1)
    # print "Permutations scores:\n", permutation_scores
    # print "Pvalue:\t", pvalue
    
    # Gradient boosting
    # clf = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0, max_depth=1, random_state=0)
    # score = xval.cross_val_score(estimator=clf, X=data, y=clas)
    # print score
    # print "Done!"

    # Using extremely randomized trees
    # clf = ExtraTreesClassifier(n_estimators=100, compute_importances=True, max_depth=None, min_samples_split=1, random_state=0, n_jobs=-1)
    # score = xval.cross_val_score(estimator=clf, X=data, y=clas, score_func=metrics.f1_score)
    # print score
    # print "Done!"

    # Print feature importances
    # importances = clf.feature_importances_
    # print importances
    # importances = importances.reshape(data.shape)
    # pl.matshow(importances, cmap=pl.cm.hot)
    # pl.title("Pixel importances with forests of trees")
    # pl.show()

    # Using random forests
    # clf = RandomForestClassifier(n_estimators=100)
    # score = xval.cross_val_score(estimator=clf, X=data, y=clas)
    # print score
    # print "Done!"

    # Using decision trees
    # clf = tree.DecisionTreeClassifier()
    # score = xval.cross_val_score(estimator=clf, X=data, y=clas)
    # print score
    # print "Done!"

    # Using Naive Bayes
    # gnb = BernoulliNB()
    # score = xval.cross_val_score(estimator=gnb, X=data, y=clas)
    # print score
    # print "Done!"

    # Using SGD
    # clf2 = linear_model.SGDClassifier()
    # score = xval.cross_val_score(estimator=clf2, X=data, y=clas)
    # print score


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
