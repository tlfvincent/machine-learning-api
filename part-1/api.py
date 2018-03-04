import socket
import pickle
import pandas as pd
from flask import Flask, request, jsonify


class IrisService(Flask):
    def load_classifier(self):
        pickle_path = "./models/model.pickle"
        with open(pickle_path, 'rb') as handle:
            clf = pickle.load(handle)

        return clf

    def __init__(self, *args, **kwargs):
            super(IrisService, self).__init__(*args, **kwargs)
            # load sketchy classifier in memory
            self.classifier = self.load_classifier()


iris_service = IrisService(__name__)


@iris_service.route("/")
def index():
    """
    When you request the root path, you'll get the index.html template.
    """
    return "Hello World! My Hostname is: {0}".format(socket.gethostname())


@iris_service.route("/predict", methods=['POST'])
def get_predictions(data):
    """
    On request, this returns a list of ``ndata`` randomly made data points.
    :param ndata: (optional)
        The number of data points to return.
    :returns data:
        A JSON string of ``ndata`` data points.
    """
    test_json = request.get_json()
    test = pd.read_json(test_json, orient='records')
    predictions = iris_service.classifier.predict(test)

    response = jsonify(predictions)
    response.status_code = 200

    return response

if __name__ == "__main__":
    iris_service.run(host='0.0.0.0', port="5000")

