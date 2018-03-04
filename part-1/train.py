import pandas as pd
from hyperopt import fmin, tpe, hp, Trials

# validation metrics
from sklearn.metrics import roc_curve, auc
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

# sklearn models
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.naive_bayes import BernoulliNB
from sklearn.neighbors import KNeighborsClassifier


class ModelSearch(object):
    def __init__(self, X, y):
        self.X = X
        self.y = y

    @staticmethod
    def define_model_space():
        space = hp.choice('classifier_type', [
            {
                'type': 'naive_bayes'
            },
            {
                'type': 'logistic_regression',
                'C': hp.uniform('C_lr', 0.0, 2.0)
            },
            {
                'type': 'randomforest',
                'max_depth': hp.choice('max_depth_rf', range(1, 20)),
                'n_estimators': hp.choice('n_estimators_rf', [100, 200, 300, 400]),
                'criterion': hp.choice('criterion', ["gini", "entropy"])
            },
            {
                'type': 'gradient_boosting',
                'max_depth': hp.choice('max_depth_gb', range(1, 20)),
                'min_samples_split': hp.choice('min_samples_split', range(5, 50)),
                'min_samples_leaf': hp.choice('min_samples_leaf', range(5, 50)),
                'n_estimators': hp.choice('n_estimators_gb', [100, 200, 300, 400]),
            },
            {
                'type': 'knn',
                'n_neighbors': hp.choice('knn_n_neighbors', range(1, 50))
            }
        ])
        return space

    def objective_function(self, params):
        # split data into cross-validation and validation data
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.2)

        t = params['type']
        del params['type']
        if t == 'naive_bayes':
            clf = BernoulliNB(**params)
        elif t == 'logistic_regression':
            clf = LogisticRegression(**params)
        elif t == 'randomforest':
            clf = RandomForestClassifier(**params)
        elif t == 'gradient_boosting':
            clf = GradientBoostingClassifier(**params)
        elif t == 'knn':
            clf = KNeighborsClassifier(**params)
        else:
            return 0

        model = clf.fit(X_train, y_train)
        #yhat_test = model.predict_proba(X_test)[:, 1]
        yhat_test = model.predict(X_test)
        acc = accuracy_score(y_test, yhat_test)
        print(acc)
        #fpr, tpr, _ = roc_curve(y_test, yhat_test)
        #roc_auc = auc(fpr, tpr)
        return 1-acc


def main():

    dat = pd.read_csv('./data/iris_data.csv')

    X = dat[[x for x in dat.columns if x != 'class']]

    y = dat['class']

    search = ModelSearch(X, y)

    trials = Trials()
    objective = search.objective_function
    model_space = search.define_model_space()
    best = fmin(objective,
                model_space,
                algo=tpe.suggest,
                max_evals=100,
                trials=trials)

    print(best)

if __name__ == '__main__':
    main()
