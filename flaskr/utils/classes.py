class SparkFitImage:
    """
    Class to represent a clothing item that is uploaded by the user.
    """
    def __init__(
        self,
        photo_id,
        predicted_classes,
        file_name,
        data,
        fabric,
        color,
        fit,
        category,
        data_url=None,
    ):
        self.photo_id = photo_id
        self.predicted_classes = predicted_classes
        self.file_name = file_name
        self.data = data
        if data_url is None:
            self.data_url = f"data:image/jpeg;base64,{data}"
        self.fabric = fabric
        self.color = color
        self.fit = fit
        self.category = category

    def to_dict(self):
        return {
            "predicted_classes": self.predicted_classes,
            "file_name": self.file_name,
            "data": self.data,
            "fabric": self.fabric,
            "color": self.color,
            "fit": self.fit,
        }


class SparkFitUser:
    """
    Class to represent a user in the application.
    """

    def __init__(self, first_name, last_name, email, clothes):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.clothes = clothes

    def to_dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "clothes": [item.to_dict() for item in self.clothes],
        }

class DynamoImage:
    """
    Class to represent a clothing item that is stored in DynamoDB.
    Differences from SparkFitImage:
    - Does not have the data attribute
    - Does not have the predicted_classes attribute
    """
    def __init__(self, photo_id, category, file_name, fabric, color, fit, data_url):
        self.photo_id = photo_id
        self.category = category
        self.file_name = file_name
        self.fabric = fabric
        self.color = color
        self.fit = fit
        self.data_url = data_url

    def to_dict(self):
        return {
            "photo_id": self.photo_id,
            "category": self.category,
            "file_name": self.file_name,
            "fabric": self.fabric,
            "color": self.color,
            "fit": self.fit,
            "data_url": self.data_url,
        }