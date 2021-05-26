from functools import wraps
from flask import Flask, request, Response
import jsonpickle
import numpy as np
import cv2
import keras

from config import *

# Initialize the Flask application
app = Flask(__name__)

def check_token(f):
    @wraps(f)
    def check_authorization(*args, **kwargs):
        if request.headers.get('X-Api-Key', None) == AUTH_TOKEN:
            return f(*args, **kwargs)
        return Response('Unknown token', 401)
    return check_authorization


# route http posts to this method
# 이미지가 아닌 다른 값이 들어올 경우 예외처리
@app.route('/api/test', methods=['POST'])
def test():
    r = request
    # convert string of image data to uint8
    nparr = np.frombuffer(r.data, np.uint8)
    # decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # do some fancy processing here....
    result = security_check(img, models)
    # build a response dict to send back to client
    response = {'result': result}
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)
    print(response_pickled)

    return Response(response=response_pickled, status=200, mimetype="application/json")


# start flask app
app.run(host="0.0.0.0", port=5000, debug=True)