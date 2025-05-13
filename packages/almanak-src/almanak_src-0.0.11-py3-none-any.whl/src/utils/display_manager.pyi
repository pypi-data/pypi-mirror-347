from _typeshed import Incomplete
from decimal import Decimal
from src.almanak_library.enums import Chain as Chain
from src.utils.utils import get_block_explorer_url as get_block_explorer_url
from typing import Any

class DisplayManager:
    verbose: Incomplete
    def __init__(self, verbose: bool = False) -> None:
        """Initialize the display manager.

        Args:
            verbose: Whether to show detailed debug information
        """
    def display_token_positions(self, tokens: list, to_terminal: bool = True) -> str | None:
        """Display available positions sorted by APY.

        Args:
            tokens: List of token objects with metadata
            to_terminal: If True, prints to terminal. If False, returns formatted string.

        Returns:
            Formatted string if to_terminal=False, None otherwise
        """
    def get_selected_position(self, tokens: list, position_address: str, to_terminal: bool = True) -> dict | str | None:
        """Display details for a selected position.

        Args:
            tokens: List of token objects with metadata
            position_address: Address of the position to find
            to_terminal: If True, prints to terminal. If False, returns formatted string

        Returns:
            If to_terminal=False:
                - Dict containing position data if found
                - String error message if not found
            If to_terminal=True:
                None (prints to terminal instead)
        """
    def display_route_info(self, route, to_terminal: bool = True) -> str | None:
        """Display information about a route.

        Args:
            route: Route object with transaction details
            to_terminal: If True, prints to terminal. If False, returns formatted string

        Returns:
            Formatted string if to_terminal=False, None otherwise
        """
    def display_balance_changes(self, initial_balances, final_balances, token_decimals: dict[str, int] | None = None, to_terminal: bool = True) -> str | None:
        """Display changes in token balances.

        Args:
            initial_balances: Dict of initial token balances
            final_balances: Dict of final token balances
            token_decimals: Optional dict with token decimals for each token type ('eth', 'source', 'target')
            to_terminal: If True, prints to terminal. If False, returns formatted string

        Returns:
            Formatted string if to_terminal=False, None otherwise
        """
    def display_failed_transaction(self, chain: Chain, tx: dict[str, Any], receipt: dict[str, Any], gas_used: int, gas_limit: int, gas_percentage: float, revert_reason: str = 'Unknown error', decoded_error: str | None = None, to_terminal: bool = True) -> str | None:
        """Display information about a failed transaction.

        Args:
            chain: The blockchain chain
            tx: Transaction object
            receipt: Transaction receipt
            gas_used: Amount of gas used
            gas_limit: Gas limit for the transaction
            gas_percentage: Percentage of gas limit used
            revert_reason: Reason for transaction revert
            decoded_error: Decoded error message if available
            to_terminal: If True, prints to terminal. If False, returns formatted string

        Returns:
            Formatted string if to_terminal=False, None otherwise
        """
    def display_transaction_params(self, tx_params: dict[str, Any], to_terminal: bool = True) -> str | None:
        """Display transaction parameters.

        Args:
            tx_params: Transaction parameters
            to_terminal: If True, prints to terminal. If False, returns formatted string

        Returns:
            Formatted string if to_terminal=False, None otherwise
        """
    def display_quote_info(self, quote, to_terminal: bool = True) -> str | None:
        """Display information about a quote.

        Args:
            quote: Quote object or dictionary with price information
            to_terminal: If True, prints to terminal. If False, returns formatted string

        Returns:
            Formatted string if to_terminal=False, None otherwise
        """
    def display_transaction_confirmation(self, receipt: dict[str, Any], gas_used: int, gas_limit: int, gas_percentage: float, to_terminal: bool = True) -> str | None:
        """Display information about a confirmed transaction.

        Args:
            receipt: Transaction receipt
            gas_used: Amount of gas used
            gas_limit: Gas limit for the transaction
            gas_percentage: Percentage of gas limit used
            to_terminal: If True, prints to terminal. If False, returns formatted string

        Returns:
            Formatted string if to_terminal=False, None otherwise
        """
    def display_swap_summary(self, token_in: str, token_out: str, amount_in: int | float | Decimal, amount_out: int | float | Decimal, tx_cost: int | float | Decimal, token_in_decimals: int = 18, token_out_decimals: int = 18, to_terminal: bool = True) -> str | None:
        """Display a summary of a swap transaction.

        Args:
            token_in: Symbol of the input token
            token_out: Symbol of the output token
            amount_in: Amount of input token
            amount_out: Amount of output token
            tx_cost: Transaction cost in ETH
            token_in_decimals: Number of decimals for the input token
            token_out_decimals: Number of decimals for the output token
            to_terminal: If True, prints to terminal. If False, returns formatted string

        Returns:
            Formatted string if to_terminal=False, None otherwise
        """
    def display_route_path(self, response, to_terminal: bool = True) -> str | None:
        """Display the route path for a swap.

        Args:
            response: Response object with route information (Quote or RouteTransaction)
            to_terminal: If True, prints to terminal. If False, returns formatted string

        Returns:
            Formatted string if to_terminal=False, None otherwise
        """
    def display_api_response(self, response, to_terminal: bool = True) -> str | None:
        """Display the full API response for troubleshooting.

        Args:
            response: The API response object (Quote or RouteTransaction)
            to_terminal: If True, prints to terminal. If False, returns formatted string

        Returns:
            Formatted string if to_terminal=False, None otherwise
        """
