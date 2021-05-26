class ClassifierBase:
    def __init__(self, name):
        self.name = name

    def predict(self, image):
        # returns True if any image predict results more than 0.5
        if getattr(self, 'model', None) is None:
            raise ValueError('Model is not loaded.')
        model = self.model
        return any([True for x in model.predict(image) if x > 0.5])
