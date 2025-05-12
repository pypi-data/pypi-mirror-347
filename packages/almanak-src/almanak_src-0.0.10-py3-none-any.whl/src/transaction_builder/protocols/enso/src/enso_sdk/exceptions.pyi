import requests
from _typeshed import Incomplete

class EnsoSDKError(Exception):
    """Base exception class for all Enso SDK errors."""

class EnsoAPIError(EnsoSDKError):
    """
    Exception raised for errors in the API response.

    Attributes:
        message: Error message
        response: The response object from the failed request
        status_code: HTTP status code of the response
        error_data: Parsed error data from the response, if available
        error_type: Classified error type (e.g., SERVER_ERROR, RATE_LIMIT)
        endpoint: The API endpoint that was called
        api_error_message: The specific error message from the API response
        correlation_id: Unique ID for tracing the request through logs
    """
    message: Incomplete
    response: Incomplete
    status_code: Incomplete
    endpoint: Incomplete
    correlation_id: Incomplete
    error_type: Incomplete
    api_error_message: Incomplete
    error_data: Incomplete
    def __init__(self, message: str, response: requests.Response, endpoint: str = None, correlation_id: str = None) -> None: ...

class Web3ProviderError(EnsoSDKError):
    """
    Exception raised for Web3 provider related errors.

    Attributes:
        message: Error message
        provider_uri: The URI of the Web3 provider that caused the error
    """
    message: Incomplete
    provider_uri: Incomplete
    def __init__(self, message: str, provider_uri: str | None = None) -> None: ...

class TransactionError(EnsoSDKError):
    """
    Exception raised for blockchain transaction errors.

    Attributes:
        message: Error message
        tx_hash: Transaction hash if available
        error_data: Additional error data
    """
    message: Incomplete
    tx_hash: Incomplete
    error_data: Incomplete
    def __init__(self, message: str, tx_hash: str | None = None, error_data: dict | None = None) -> None: ...

class ValidationError(EnsoSDKError):
    """
    Exception raised for validation errors.

    Attributes:
        message: Error message
        field: Name of the field that failed validation
        value: The invalid value
    """
    message: Incomplete
    field: Incomplete
    value: Incomplete
    def __init__(self, message: str, field: str | None = None, value: str | None = None) -> None: ...

class ConfigurationError(EnsoSDKError):
    """
    Exception raised for SDK configuration errors.

    Attributes:
        message: Error message
        parameter: Name of the configuration parameter that caused the error
    """
    message: Incomplete
    parameter: Incomplete
    def __init__(self, message: str, parameter: str | None = None) -> None: ...

class TokenError(EnsoSDKError):
    """
    Exception raised for token-related errors.

    Attributes:
        message: Error message
        token_address: Address of the token that caused the error
        chain_id: Chain ID where the error occurred
    """
    message: Incomplete
    token_address: Incomplete
    chain_id: Incomplete
    def __init__(self, message: str, token_address: str | None = None, chain_id: int | None = None) -> None: ...
