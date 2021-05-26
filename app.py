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

cnn_id = keras.models.load_model('./models/cnn_id.h5')
cnn_driver = keras.models.load_model('./models/cnn_driver.h5')
cnn_student = keras.models.load_model('./models/cnn_student.h5')

models = [cnn_id, cnn_driver, cnn_student]

def decoding(data):
    try:
        #en = np.frombuffer(data, dtype=np.uint8)  # int
        #img = cv2.imdecode(data, cv2.IMREAD_COLOR)
        img = cv2.resize(data, (86, 54))

        test = []
        numpy_image = img
        test.append(numpy_image / 255.)

        test = np.array(test)
    except Exception as e:
        print(str(e))

    return test


# data = binary 형태의 이미지
def security_check(data, models):
    x_test = decoding(data)

    for model in models:
        result = model.predict(x_test)

        for i in result:
            if i > 0.5:
                return True  # 한 개라도 걸리면
    return False

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