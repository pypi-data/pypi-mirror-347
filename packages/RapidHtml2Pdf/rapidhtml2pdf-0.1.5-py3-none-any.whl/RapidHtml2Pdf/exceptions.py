class H2PError(Exception):
    """Base exception for h2p package."""
    pass

class RenderError(H2PError):
    """Raised when an error occurs during rendering."""
    def __init__(self, message: str):
        super().__init__(f"RenderError: {message}")

class AssetError(H2PError):
    """Raised when an error occurs in asset fetching or inlining."""
    def __init__(self, message: str):
        super().__init__(f"AssetError: {message}")

class ConfigurationError(H2PError):
    """Raised when provided configuration options are invalid."""
    def __init__(self, message: str):
        super().__init__(f"ConfigurationError: {message}")
