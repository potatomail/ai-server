import json
from functools import wraps
from flask import Flask, request, Response, abort

from config import *
from classifiers.factory import generate_factory
from ai import decoding


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
@check_token
def test():
    print(request.files)
    images = request.files.get('images', None)
    #print(images)
    if images is None:
        abort(400, 'Image field not found.')
    image = decoding(images.read())
    #print(image)
    #for image in images:
        #print(image)
    for model_name in SUPPORTED_MODELS:
        model = generate_factory(model_name)
            #print(model)
            #print(image)
        print(model)
        if model.predict(image):
            return Response(response=json.dumps({'result': 1}), status=200, mimetype="application/json")


    return Response(response=json.dumps({'result': 0}), status=200, mimetype="application/json")


# start flask app
app.run(host="0.0.0.0", port=5000, debug=True)