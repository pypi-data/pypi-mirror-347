class MedialoopsterError(Exception):
    """Base exception for all medialoopster errors."""
    pass


class MedialoopsterConnectionError(MedialoopsterError):
    """Raised when there is a connection error with the medialoopster API."""
    pass


class MedialoopsterAuthenticationError(MedialoopsterError):
    """Raised when authentication with the medialoopster API fails."""
    pass


class MedialoopsterNotFoundError(MedialoopsterError):
    """Raised when a requested resource is not found."""
    pass


class MedialoopsterTimeoutError(MedialoopsterError):
    """Raised when a request to the medialoopster API times out."""
    pass


class MedialoopsterValidationError(MedialoopsterError):
    """Raised when there is a validation error with the request or response."""
    pass
