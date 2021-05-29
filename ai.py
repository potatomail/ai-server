import cv2
import numpy as np
import io
from PIL import Image

'''
cnn_id = keras.models.load_model('./models/cnn_id.h5')
cnn_driver = keras.models.load_model('./models/cnn_driver.h5')
cnn_student = keras.models.load_model('./models/cnn_student.h5')
'''

class ImageDecodeException(Exception):
    pass

'''
def decoding(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))
    print(image)
    print('--------------')
    image = np.array(image)
    print(image)
    image = image[:, :, 0:3]
    image = tf.image.convert_image_dtype(image, tf.float32)
    image = tf.image.resize_with_crop_or_pad(image, 86, 54)

    return image
'''
def decoding(test):
    width = 86
    height = 54
    test2 = []
    image = Image.open(io.BytesIO(test))
    image = image.resize((width, height))
    numpy_image = np.array(image)  # 이미지 타입을 넘파이 타입으로 변환
    test2.append(numpy_image / 255.)

    test2 = np.array(test2)
    return test2

'''
# data = binary 형태의 이미지
def security_check(data, models):
    x_test = decoding(data)

    for model in models:
        result = model.predict(x_test)

        for i in result:
            if i > 0.5:
                return True  # 한 개라도 걸리면
    return False
'''
class ImageClassifier:
    def classify(self, image: object):
        # classify image as something
        pass

