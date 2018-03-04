import pandas as pd
import argparse
import pickle
from evaluate_model import EvaluateModel
from train_model import TrainModel

# sklearn models
from sklearn.neighbors import KNeighborsClassifier


def main(params):

    train = params.train
    evaluate = params.evaluate

    dat = pd.read_csv('./data/iris_data.csv')

    X = dat[[x for x in dat.columns if x != 'class']]

    y = dat['class']

    if evaluate == 1:
        search = EvaluateModel(X, y)
        trials = search.run_trials(100)
        with open('./models/trials.pickle', 'wb') as handle:
            pickle.dump(trials, handle)

    if train == 1:
        clf = KNeighborsClassifier(n_neighbors=11)
        tm = TrainModel(X, y, clf, nfolds=10)
        production_model = tm.train_model()
        with open('./models/model.pickle', 'wb') as handle:
            pickle.dump(production_model, handle)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('-e', '--evaluate', action='store', required=False,
                        type=int, dest='evaluate',
                        default=0,
                        help='specify whether to perform model selection')
    parser.add_argument('-t', '--train', action='store', required=False,
                        type=int, dest='train',
                        default=1,
                        help='specify whether to train classifier')

    params = parser.parse_args()

    main(params)
