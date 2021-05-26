from classifiers.base import ClassifierBase

class student(ClassifierBase):
    def __init__(self):
        super().__init__('student')
        # self.model = keras.models.load_model('./student.h5')
        self.model = True