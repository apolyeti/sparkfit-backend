class SparkFitImage:
    def __init__(self, photo_id, predicted_classes, file_name, data, fabric, color, fit, category, data_url=None):
        self.photo_id = photo_id
        self.predicted_classes = predicted_classes
        self.file_name = file_name
        self.data = data
        if data_url is None:
            self.data_url = f'data:image/jpeg;base64,{data}'
        self.fabric = fabric
        self.color = color
        self.fit = fit
        self.category = category

    def to_dict(self):
        return {
            
            'predicted_classes': self.predicted_classes,
            'file_name': self.file_name,
            'data': self.data,
            'fabric': self.fabric,
            'color': self.color,
            'fit': self.fit
        }

class SparkFitUser:

    def __init__(self, first_name, last_name, email, clothes):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.clothes = clothes

    def to_dict(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'clothes': [item.to_dict() for item in self.clothes]
        }

