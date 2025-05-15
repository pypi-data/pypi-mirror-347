import pytest
from src.utils.exceptions import (
    APIError,
    ArgumentException,
    AuthenticationError,
    RagtasticError,
    RateLimitError,
    ValidationError,
)


def test_ragtastic_error_base():
    """Test base RagtasticError."""
    message = "Base Ragtastic error"
    with pytest.raises(RagtasticError, match=message):
        raise RagtasticError(message)


def test_api_error():
    """Test APIError initialization."""
    message = "API Error occurred"
    status_code = 500
    error = APIError(message, status_code)
    assert str(error) == message
    assert error.status_code == status_code
    assert isinstance(error, RagtasticError)

    error_no_code = APIError(message)
    assert str(error_no_code) == message
    assert error_no_code.status_code is None
    assert isinstance(error_no_code, RagtasticError)


def test_validation_error():
    """Test ValidationError."""
    message = "Validation failed"
    with pytest.raises(ValidationError, match=message):
        raise ValidationError(message)
    assert isinstance(ValidationError(message), RagtasticError)


def test_authentication_error():
    """Test AuthenticationError."""
    message = "Authentication failed"
    with pytest.raises(AuthenticationError, match=message):
        raise AuthenticationError(message)
    assert isinstance(AuthenticationError(message), RagtasticError)


def test_rate_limit_error():
    """Test RateLimitError."""
    message = "Rate limit exceeded"
    with pytest.raises(RateLimitError, match=message):
        raise RateLimitError(message)
    assert isinstance(RateLimitError(message), RagtasticError)


def test_argument_exception():
    """Test ArgumentException."""
    message = "Invalid argument"
    with pytest.raises(ArgumentException, match=message):
        raise ArgumentException(message)
    assert isinstance(ArgumentException(message), RagtasticError)
