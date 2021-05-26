from classifiers.base import ClassifierBase

class id(ClassifierBase):
    def __init__(self):
        super().__init__('ID')
        # self.model = keras.models.load_model('./cnn_id.h5')

        self.model = True