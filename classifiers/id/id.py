from classifiers.base import ClassifierBase
import keras

class id(ClassifierBase):
    def __init__(self):
        super().__init__('ID')
        self.model = keras.models.load_model('./models/cnn_id.h5')

        self.model = True