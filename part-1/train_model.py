'''
train_model.py

###
Usage
from train_model import TrainModel
estimator_name = 'rf'
tm = TrainModel(Xscaled, y, estimator_name, estimators, nfolds=10)
est = tm.train_model()

###
Purpose
Class to train any input estimator for the given response vector
and input feature matrix
- X: the standardized feature matrix
- y: the response vector
- estimator: the estimator object to fit
- nfolds: the numer of cross validation folds
'''
# import standard library
import logging
import numpy as np

# validation metrics
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score
log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=log_fmt)


class TrainModel(object):
    def __init__(self,
                 X,
                 y,
                 estimator,
                 nfolds=10):
        self.X = X
        self.y = y
        self.estimator = estimator
        self.nfolds = nfolds

    def train_model(self):
        # check 10-fold CV as a last sanity check
        cv = StratifiedKFold(n_splits=self.nfolds, shuffle=True)
        cv.get_n_splits(self.X, self.y)
        fold_performance = cross_val_score(self.estimator,
                                           self.X,
                                           self.y,
                                           cv=cv,
                                           scoring='roc_auc',
                                           n_jobs=-1)
        mean_auc = np.mean(fold_performance)
        logging.info('Production Model AUC: {}.'.format(mean_auc))

        # if performance is adequate, reset est object and fit on full data
        if mean_auc >= 0.8:
            self.estimator.fit(self.X, self.y)
            return self.estimator
        else:
            raise LowScoreException("AUC is looking low! Time for some thorough evaluation!")


class LowScoreException(Exception):
    '''Raised when the Estimator is weak.

    Attributes:
        message -- explanation of why the specific score is not allowed
    '''

    def __init__(self, message):
        self.message = message
        self.alert_to_slack()

    def alert_to_slack(self):
        pass
