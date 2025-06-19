# src/application/exceptions.py

class ApplicationException(Exception):
    """Base exception for application layer errors."""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

class NotFoundException(ApplicationException):
    """Exception raised when an entity is not found."""
    def __init__(self, message: str = "Recurso no encontrado"):
        super().__init__(message, status_code=404)

class ConflictException(ApplicationException):
    """Exception raised when a resource conflict occurs (e.g., unique constraint violation)."""
    def __init__(self, message: str = "Conflicto de recurso"):
        super().__init__(message, status_code=409)

class InvalidInputException(ApplicationException):
    """Exception raised for invalid input data."""
    def __init__(self, message: str = "Datos de entrada inválidos"):
        super().__init__(message, status_code=400)

class UnauthorizedException(ApplicationException):
    """Exception raised for unauthorized access."""
    def __init__(self, message: str = "No autorizado"):
        super().__init__(message, status_code=401)