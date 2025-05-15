"""
FluidGrids SDK exceptions
"""


class FluidGridsError(Exception):
    """Base exception for all FluidGrids SDK errors."""
    pass


class FluidGridsAPIError(FluidGridsError):
    """Exception raised when the FluidGrids API returns an error."""
    pass


class FluidGridsAuthenticationError(FluidGridsAPIError):
    """Exception raised when authentication with the FluidGrids API fails."""
    pass


class FluidGridsResourceNotFoundError(FluidGridsAPIError):
    """Exception raised when a requested resource is not found."""
    pass


class FluidGridsValidationError(FluidGridsAPIError):
    """Exception raised when request data fails validation."""
    pass 