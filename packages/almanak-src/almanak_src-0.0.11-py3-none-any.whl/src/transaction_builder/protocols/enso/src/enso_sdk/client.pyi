from .exceptions import ConfigurationError as ConfigurationError, EnsoAPIError as EnsoAPIError, TokenError as TokenError, ValidationError as ValidationError, Web3ProviderError as Web3ProviderError
from .json_utils import EnsoJSONEncoder as EnsoJSONEncoder
from .models import Network as Network, Price as Price, Protocol as Protocol, Quote as Quote, RouteParams as RouteParams, RouteTransaction as RouteTransaction, Standard as Standard, Token as Token, TokenMetadata as TokenMetadata, TokenType as TokenType, VolumeData as VolumeData
from .utils import AmountHandler as AmountHandler, validate_ethereum_address as validate_ethereum_address
from _typeshed import Incomplete
from decimal import Decimal
from eth_account.signers.local import LocalAccount as LocalAccount
from src.utils.logger import get_logger as get_logger
from typing import Any
from web3.types import TxParams as TxParams

logger: Incomplete

class EnsoSDK:
    """
    Python SDK for interacting with the Enso Finance API.

    This SDK provides two main types of functionality:
    1. Core API methods - Used by the adapter for transaction preparation (get_route, approve_token_via_api)
    2. Direct execution methods - For standalone SDK usage (execute_swap, approve_token)
    """
    CHAIN_MAPPING: Incomplete
    ROUTER_ADDRESSES: Incomplete
    DELEGATE_ADDRESSES: Incomplete
    @staticmethod
    def log_retry_hook(response, *args, **kwargs): ...
    api_key: Incomplete
    base_url: Incomplete
    session: Incomplete
    w3: Incomplete
    def __init__(self, **kwargs) -> None:
        """Initialize the SDK with the provided parameters."""
    def set_web3_provider(self, provider_uri: str) -> None:
        """Set or update the Web3 provider."""
    def reset_session(self) -> None: ...
    def set_account(self, private_key: str) -> None:
        """Set the account for transaction signing."""
    def build_transaction(self, route_tx: RouteTransaction, gas_price_gwei: int | float | None = None, max_priority_fee_gwei: int | float | None = None, max_fee_gwei: int | float | None = None, gas_limit_buffer: float = 1.1) -> TxParams:
        """
        Build a complete transaction dict from route data.

        Args:
            route_tx: Route transaction object
            gas_price_gwei: Gas price in Gwei for legacy transactions
            max_priority_fee_gwei: Max priority fee in Gwei for EIP-1559 transactions
            max_fee_gwei: Max fee in Gwei for EIP-1559 transactions
            gas_limit_buffer: Multiplier to apply to the estimated gas (e.g., 1.1 for 10% buffer)

        Returns:
            Complete transaction parameters dict ready for signing
        """
    def get_networks(self, name: str | None = None, chain_id: str | None = None) -> list[Network]:
        """Get supported networks."""
    def get_price(self, chain_id: str, address: str) -> Price:
        """Get price for a token."""
    def get_aggregators(self) -> list[str]:
        """Get aggregators supported by the API."""
    def get_volume(self, chain_id: int) -> VolumeData:
        """Get chain USD volume and total transactions."""
    def get_token_decimals(self, token_address: str, chain_id: str | int) -> int:
        '''
        Get decimals for a token directly from the contract.

        Args:
            token_address: The token address to get decimals for
            chain_id: The chain ID or name (e.g., "base", 8453)

        Returns:
            The number of decimals for the token

        Raises:
            TokenError: If unable to determine token decimals
        '''
    def get_underlying_token_data(self, chain_id: str | int, token_addresses: str | list[str], protocol_slugs: str | list[str] | None = None, include_metadata: bool = False) -> list[Token]:
        '''Get token data for tokens with the specified underlying tokens.

        Args:
            chain_id: Chain ID or name (e.g., "ethereum", "base", 1, 8453)
            token_addresses: Single token address or list of addresses to filter by
            protocol_slugs: Optional protocol slug(s) to filter by
            include_metadata: Whether to include token metadata in the response

        Returns:
            List of Token objects sorted by APY (descending)
        '''
    def get_protocols(self, slug: str | None = None) -> list[Protocol]:
        """Get available protocols."""
    def get_protocols_by_chain(self, chains: str | list[str]) -> dict[str, list[str]]:
        '''Get protocols available on specified chains.

        Args:
            chains: Single chain name/ID or list of chain names/IDs (e.g., "arbitrum", "base", 1, 8453)

        Returns:
            Dictionary mapping chain names to lists of protocol slugs
            e.g., {
                "arbitrum": ["aave-v3", "uniswap-v3", ...],
                "base": ["baseswap", "aerodrome", ...]
            }
        '''
    def get_standards(self) -> list[Standard]:
        """Get standards and methods for bundle shortcuts."""
    def get_actions(self) -> list[dict[str, Any]]:
        """Get actions available for bundle shortcuts."""
    def get_route(self, params: RouteParams) -> RouteTransaction:
        """Get the best route from one token to another."""
    async def get_route_async(self, params: RouteParams) -> RouteTransaction:
        """Get the best route from one token to another (async version)."""
    def get_quote(self, params_or_token_in: RouteParams | list[str], token_out: list[str] | None = None, amount_in: list[str] | None = None, chain_id: int | None = None, from_address: str | None = None, routing_strategy: str | None = None, fee: list[str] | None = None, fee_receiver: str | None = None, disable_rfqs: bool | None = None, ignore_aggregators: list[str] | None = None, ignore_standards: list[str] | None = None) -> Quote:
        """
        Get a quote for converting between tokens.

        Args:
            params_or_token_in: Either a RouteParams object or a list of input token addresses
            token_out: List of output token addresses (not needed if RouteParams is provided)
            amount_in: List of input amounts in wei (not needed if RouteParams is provided)
            chain_id: Chain ID (not needed if RouteParams is provided)
            from_address: Address to get quote for (not needed if RouteParams is provided)
            routing_strategy: Routing strategy (not needed if RouteParams is provided)
            fee: Fee
            fee_receiver: Fee receiver
            disable_rfqs: Disable RFQs
            ignore_aggregators: Ignore aggregators
            ignore_standards: Ignore standards
        """
    def submit_route_transaction(self, route_params: RouteParams, gas_price_gwei: int | float | None = None, max_priority_fee_gwei: int | float | None = None, max_fee_gwei: int | float | None = None, gas_limit_buffer: float = 1.1) -> str:
        """
        Get optimal route and submit the transaction (synchronous version).

        Args:
            route_params: Route parameters for the swap
            gas_price_gwei: Gas price in Gwei for legacy transactions
            max_priority_fee_gwei: Max priority fee in Gwei for EIP-1559 transactions
            max_fee_gwei: Max fee in Gwei for EIP-1559 transactions
            gas_limit_buffer: Multiplier to apply to the estimated gas

        Returns:
            Transaction hash as a hex string
        """
    async def submit_route_transaction_async(self, route_params: RouteParams, gas_price_gwei: int | float | None = None, max_priority_fee_gwei: int | float | None = None, max_fee_gwei: int | float | None = None) -> str:
        """Get optimal route and submit the transaction (async version)."""
    def wait_for_transaction(self, tx_hash: str, timeout: int = 120, poll_interval: float = 0.1) -> dict:
        """Wait for a transaction to be mined and return the receipt."""
    async def execute_swap_async(self, route_params: RouteParams, wait_for_receipt: bool = True, timeout: int = 120, gas_price_gwei: int | float | None = None, max_priority_fee_gwei: int | float | None = None, max_fee_gwei: int | float | None = None) -> str | dict:
        """Complete helper function to execute a swap from start to finish (async version)."""
    def get_token_balance(self, token_address: str, account_address: str) -> dict[str, Decimal | str | int]:
        """
        Get token balance and info for an address.

        Args:
            token_address: Token address (use 0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE for ETH)
            account_address: Address to check balance for

        Returns:
            Dict containing:
            - balance: Token balance in human-readable format
            - symbol: Token symbol (e.g., 'ETH', 'USDC')
            - decimals: Number of decimals for the token
        """
    def validate_router_address(self, chain_id: int, spender_address: str) -> bool:
        """
        Validate that the spender address matches our expected router address.

        Args:
            chain_id: The chain ID
            spender_address: The spender address to validate

        Returns:
            True if the address matches, False otherwise
        """
    def get_router_address(self, chain_id: int, routing_strategy: str = 'router') -> str:
        """
        Get the Enso address for the specified chain and routing strategy.

        Args:
            chain_id: Chain ID
            routing_strategy: Routing strategy ('router' or 'delegate')

        Returns:
            The address for the specified chain and routing strategy

        Raises:
            ValidationError: If the chain ID is not supported
        """
    def get_token_allowance(self, token_address: str, owner_address: str, spender_address: str) -> int:
        """Get the current token allowance for a spender."""
    def approve_token_via_api(self, token_address: str, from_address: str | None = None, amount: int | Decimal | str | None = None, chain_id: str | int | None = None, routing_strategy: str = 'router') -> dict:
        '''
        Approve token spending using the Enso API endpoint.

        Args:
            token_address: Address of the token to approve
            from_address: Address of the token holder (defaults to account address if None)
            amount: Amount to approve in wei (defaults to max uint256 if None)
            chain_id: Chain ID (defaults to current chain if None)
            routing_strategy: Routing strategy to use (ensowallet, router, delegate)
                              Defaults to "router"

        Returns:
            dict: Transaction data returned by the API
        '''
    def approve_token(self, token_address: str, spender_address: str, amount: int | Decimal | None = None, gas_price_gwei: int | float | None = None, max_fee_gwei: int | float | None = 2.0, max_priority_fee_gwei: int | float | None = 0.5, gas_limit_buffer: float = 1.1, use_api: bool = False, routing_strategy: str = 'router') -> str:
        """
        Approve token spending for a spender address.

        Args:
            token_address: Address of the token to approve
            spender_address: Address of the spender (usually a router)
            amount: Amount to approve (defaults to max uint256 if None)
            gas_price_gwei: Gas price in Gwei for legacy transactions
            max_fee_gwei: Maximum fee per gas in Gwei for EIP-1559 transactions
            max_priority_fee_gwei: Maximum priority fee per gas in Gwei for EIP-1559 transactions
            gas_limit_buffer: Multiplier to apply to the estimated gas
            use_api: Whether to use the Enso API endpoint instead of direct web3 transaction
            routing_strategy: Routing strategy to use when use_api=True (ensowallet, router, delegate)

        Returns:
            str: Transaction hash as a hex string
        """
    def execute_swap(self, route_params: RouteParams, wait_for_receipt: bool = True, timeout: int = 120, gas_price_gwei: int | float | None = None, max_priority_fee_gwei: int | float | None = None, max_fee_gwei: int | float | None = None, gas_limit_buffer: float = 1.1) -> str | dict:
        """
        Execute a swap from start to finish (synchronous version).

        Args:
            route_params: Route parameters for the swap
            wait_for_receipt: Whether to wait for transaction receipt
            timeout: Timeout for waiting for receipt in seconds
            gas_price_gwei: Gas price in Gwei for legacy transactions
            max_priority_fee_gwei: Max priority fee in Gwei for EIP-1559 transactions
            max_fee_gwei: Max fee in Gwei for EIP-1559 transactions
            gas_limit_buffer: Multiplier to apply to the estimated gas

        Returns:
            Transaction hash or receipt depending on wait_for_receipt
        """
    def handle_failed_transaction(self, tx_hash: str, decode_errors: bool = True) -> dict[str, Any]:
        """
        Get detailed information about a failed transaction.

        Args:
            tx_hash: Transaction hash
            decode_errors: Whether to attempt to decode error messages

        Returns:
            Dict containing error information, revert reason, etc.
        """
