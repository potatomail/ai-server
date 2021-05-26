import keras

cnn_id = keras.models.load_model('./models/cnn_id.h5')
cnn_driver = keras.models.load_model('./models/cnn_driver.h5')
cnn_student = keras.models.load_model('./models/cnn_student.h5')

class ImageDecodeException(Exception):
    pass

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

class ImageClassifier:
    def classify(self, image: object):
        # classify image as something
        pass
