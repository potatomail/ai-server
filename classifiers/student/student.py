from classifiers.base import ClassifierBase
import keras

class student(ClassifierBase):
    def __init__(self):
        super().__init__('student')
        self.model = keras.models.load_model('./models/student.h5')
        self.model = True