class ValidationError(Exception):
    MESSAGE = "Validation failed for the following properties, either missing or unknown: {}. "+\
                "Please check scicatproject.github.io/api-documentation/ for valid keys."
    
    def __init__(self, args):
        self.args = args
        
    def __str__(self):
        return self.MESSAGE.format(', '.join(self.args))