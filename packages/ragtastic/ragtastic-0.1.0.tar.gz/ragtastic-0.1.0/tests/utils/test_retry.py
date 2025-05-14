from unittest.mock import MagicMock, call

import pytest
from src.utils.exceptions import (
    APIError,
    RagtasticError,
    RateLimitError,
    ValidationError,
)
from src.utils.retry import retry_with_backoff


def test_retry_success_on_first_attempt(mocker):
    """Test that the function is called once if it succeeds immediately."""
    mock_sleep = mocker.patch("time.sleep")
    mock_func = MagicMock(return_value="Success")

    @retry_with_backoff()
    def decorated_func():
        return mock_func()

    assert decorated_func() == "Success"
    mock_func.assert_called_once()
    mock_sleep.assert_not_called()


def test_retry_on_retryable_exception(mocker):
    """Test retry behavior on a default retryable exception (RateLimitError)."""
    mock_sleep = mocker.patch("time.sleep")
    mock_func = MagicMock()
    mock_func.side_effect = [RateLimitError("Retry me"), "Success"]

    @retry_with_backoff(max_retries=3, base_delay=0.1)
    def decorated_func():
        return mock_func()

    assert decorated_func() == "Success"
    assert mock_func.call_count == 2
    mock_sleep.assert_called_once()
    # Check if delay is roughly base_delay (allowing for jitter)
    args, _ = mock_sleep.call_args
    assert 0.1 * 0.5 <= args[0] <= 0.1 * 1.5


def test_retry_exceeds_max_retries(mocker):
    """Test that RagtasticError is raised after max_retries."""
    mock_sleep = mocker.patch("time.sleep")
    mock_func = MagicMock(side_effect=RateLimitError("Persistent error"))

    @retry_with_backoff(max_retries=2, base_delay=0.01)
    def decorated_func():
        return mock_func()

    with pytest.raises(
        RagtasticError, match="Max retries \\(2\\) exceeded"
    ) as exc_info:
        decorated_func()

    assert mock_func.call_count == 3  # Initial call + 2 retries
    assert mock_sleep.call_count == 2
    assert isinstance(exc_info.value.__cause__, RateLimitError)


def test_retry_with_custom_retryable_exceptions(mocker):
    """Test retry with a custom list of retryable exceptions."""
    mock_sleep = mocker.patch("time.sleep")
    mock_func = MagicMock()
    mock_func.side_effect = [ValidationError("Custom retry"), "Success"]

    @retry_with_backoff(retryable_exceptions=(ValidationError,))
    def decorated_func():
        return mock_func()

    assert decorated_func() == "Success"
    assert mock_func.call_count == 2
    mock_sleep.assert_called_once()


def test_no_retry_on_non_retryable_exception(mocker):
    """Test that non-specified exceptions are raised immediately (wrapped in RagtasticError)."""
    mock_sleep = mocker.patch("time.sleep")
    # APIError is not in the default retryable_exceptions
    mock_func = MagicMock(side_effect=APIError("Non-retryable"))

    @retry_with_backoff()
    def decorated_func():
        return mock_func()

    with pytest.raises(
        RagtasticError, match="Unhandled error: Non-retryable"
    ) as exc_info:
        decorated_func()

    mock_func.assert_called_once()
    mock_sleep.assert_not_called()
    assert isinstance(exc_info.value.__cause__, APIError)


def test_retry_delay_exponentiation_and_max_delay(mocker):
    """Test that delay increases exponentially and respects max_delay."""
    mock_sleep = mocker.patch("time.sleep")
    mock_func = MagicMock(
        side_effect=[
            RateLimitError("1"),
            RateLimitError("2"),
            RateLimitError("3"),
            "Success",
        ]
    )

    @retry_with_backoff(max_retries=3, base_delay=1, max_delay=2.5, jitter=False)
    def decorated_func():
        return mock_func()

    assert decorated_func() == "Success"
    assert mock_func.call_count == 4
    assert mock_sleep.call_count == 3
    expected_delays = [
        call(1.0),  # base_delay * (2**0)
        call(2.0),  # base_delay * (2**1)
        call(2.5),  # min(base_delay * (2**2)=4.0, max_delay=2.5)
    ]
    mock_sleep.assert_has_calls(expected_delays)


def test_retry_with_jitter(mocker):
    """Test that jitter is applied to the delay."""
    mock_random = mocker.patch("random.random", return_value=0.75)  # Predictable jitter
    mock_sleep = mocker.patch("time.sleep")
    mock_func = MagicMock(side_effect=[RateLimitError("Retry"), "Success"])

    @retry_with_backoff(base_delay=1.0, jitter=True)
    def decorated_func():
        return mock_func()

    assert decorated_func() == "Success"
    mock_sleep.assert_called_once()
    # delay = base_delay * (0.5 + random.random()) = 1.0 * (0.5 + 0.75) = 1.25
    args, _ = mock_sleep.call_args
    assert args[0] == pytest.approx(1.0 * (0.5 + 0.75))
    mock_random.assert_called_once()
