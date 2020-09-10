class Danger:
    def __init__(
        self,
        lat,
        long,
        crime,
        precautions='',
    ):
        self.x = abs(lat)
        self.y = abs(long)
        self.lat = lat
        self.long = long
        self.crime, self.precautions = crime, precautions

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_coods(self):
        return (self.x, self.y)

    def to_dict(self):
        result = {
            "latitude": self.lat,
            "longitude": self.long,
            "crime": self.crime,
            "precautions": self.precautions,
        }
        return result

    def __str__(self):
        return f'{self.x}, {self.y}'

class SOS:
    def __init__(
        self,
        lat,
        long,
        email
    ):
        self.x = abs(lat)
        self.y = abs(long)
        self.lat = lat
        self.long = long
        self.email= email

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_coods(self):
        return (self.x, self.y)

    def to_dict(self):
        result = {
            "latitude": self.lat,
            "longitude": self.long,
            "email": self.email
        }
        return result

    def __str__(self):
        return f'{self.x}, {self.y}'
