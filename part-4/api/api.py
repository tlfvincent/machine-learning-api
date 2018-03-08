import socket
import pickle
import traceback
import pandas as pd
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import BaseConfig
from helpers.middleware import setup_metrics


class IrisService(Flask):
    def load_classifier(self):
        pickle_path = "./models/model.pickle"
        with open(pickle_path, 'rb') as handle:
            clf = pickle.load(handle)
            features = pickle.load(handle)

        return clf, features

    def __init__(self, *args, **kwargs):
            super(IrisService, self).__init__(*args, **kwargs)
            # load sketchy classifier in memory
            self.classifier, self.features = self.load_classifier()


iris_service = IrisService(__name__)
setup_metrics(iris_service)
iris_service.config.from_object(BaseConfig)
db = SQLAlchemy(iris_service)

from schemas import Classifications


@iris_service.route("/")
def index():
    """
    When you request the root path, you'll get the index.html template.
    """
    try:
        return "Hello World! My Hostname is: {0}".format(socket.gethostname())
    except Exception as e:
        return jsonify({'error': str(e), 'trace': traceback.format_exc()})


@iris_service.route("/predict", methods=['POST'])
def get_predictions():
    """
    On request, this returns a list of ``ndata`` randomly made data points.
    :param ndata: (optional)
        The number of data points to return.
    :returns data:
        A JSON string of ``ndata`` data points.
    """
    try:
        json_ = request.json
        query = pd.get_dummies(pd.DataFrame.from_records([json_]))
        query = query.reindex(columns=iris_service.features, fill_value=0)

        probas_ = iris_service.classifier.predict_proba(query)
        predictions = {'Iris-setosa': probas_[0][0],
                       'Iris-versicolor': probas_[0][1],
                       'Iris-virginica': probas_[0][2]}

        response = jsonify({'prediction': predictions, "status_code": 200})
        return response
    except Exception as e:
        return jsonify({'error': str(e), 'trace': traceback.format_exc()})


if __name__ == "__main__":
    iris_service.run(host='0.0.0.0', port=5000, debug=True)
