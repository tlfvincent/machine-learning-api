import socket
import pickle
import pandas as pd
from flask import Flask, request, jsonify


class IrisService(Flask):
    def load_classifier(self):
        pickle_path = "./models/model.pickle"
        with open(pickle_path, 'rb') as handle:
            clf = pickle.load(handle)
            features = pickle.load(handle)

        print(features)
        return clf, features

    def __init__(self, *args, **kwargs):
            super(IrisService, self).__init__(*args, **kwargs)
            # load sketchy classifier in memory
            self.classifier, self.features = self.load_classifier()


iris_service = IrisService(__name__)


@iris_service.route("/")
def index():
    """
    When you request the root path, you'll get the index.html template.
    """
    return "Hello World! My Hostname is: {0}".format(socket.gethostname())


@iris_service.route("/predict", methods=['POST'])
def get_predictions():
    """
    On request, this returns a list of ``ndata`` randomly made data points.
    :param ndata: (optional)
        The number of data points to return.
    :returns data:
        A JSON string of ``ndata`` data points.
    """
    #return "Hello World! My Hostname is: {0}".format(socket.gethostname())
    json_ = request.json
    query = pd.get_dummies(pd.DataFrame.from_records([json_]))
    query = query.reindex(columns=iris_service.features, fill_value=0)

    probas_ = iris_service.classifier.predict_proba(query)
    predictions = {'Iris-setosa': probas_[0][0],
                   'Iris-versicolor': probas_[0][1],
                   'Iris-virginica': probas_[0][2]}

    response = jsonify({'prediction': predictions, "status_code": 200})
    return response



    # response = jsonify({'prediction': predictions, "status_code": 200})
    # return response

if __name__ == "__main__":
    iris_service.run(host='0.0.0.0', port=5010, debug=True)
