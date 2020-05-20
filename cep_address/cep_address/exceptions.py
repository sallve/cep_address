class ServiceError(Exception):
    def __init__(self, service, message=""):
        self.service = service
        self.message = message

    def __str__(self):
        return f"ServiceError has been raised in {self.service}\n{self.message}"


class ValidationError(Exception):
    def __init__(self, message=""):
        self.message = message

    def __str__(self):
        return f"ValidationError has been raised, {self.message}"


class InvalidCepLength(Exception):
    def __init__(self, message=""):
        self.message = message

    def __str__(self):
        return f"InvalidCepLength has been raised, {self.message}"
