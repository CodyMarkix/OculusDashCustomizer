class InvalidSizeException(BaseException):
    def __str__(self):
        return "The image provided is of an invalid size! You need a 1024x1024 px image."
    
class NotImplementedException(BaseException):
    def __str__(self):
        return "This feature is not yet implemented you impatient silly man!"