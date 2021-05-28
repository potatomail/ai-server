from classifiers.base import ClassifierBase
import keras

class driver(ClassifierBase):
    def __init__(self):
        super().__init__('driver')
        self.model = keras.models.load_model('./models/cnn_driver.h5')
        self.model = True
