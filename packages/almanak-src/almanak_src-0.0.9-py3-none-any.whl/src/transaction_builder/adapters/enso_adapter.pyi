from _typeshed import Incomplete
from src.almanak_library.enums import ActionType as ActionType, Chain as Chain, Network as Network, Protocol as Protocol, TransactionType as TransactionType
from src.almanak_library.models.action import Action as Action
from src.almanak_library.models.params import ApproveParams as ApproveParams, SwapParams as SwapParams
from src.almanak_library.models.sdk import ISDK as ISDK
from src.almanak_library.models.transaction import Transaction as Transaction
from src.transaction_builder.adapters.base_adapter import ProtocolAdapter as ProtocolAdapter
from src.transaction_builder.protocols.enso.src.enso_sdk.exceptions import ValidationError as ValidationError
from src.transaction_builder.protocols.enso.src.enso_sdk.models import RouteParams as RouteParams, RoutingStrategy as RoutingStrategy
from src.utils.config import Config as Config
from src.utils.utils import get_logger as get_logger
from typing import Any, Callable
from web3 import Web3

logger: Incomplete

class EnsoAdapter(ProtocolAdapter):
    """Adapter for Enso protocol-specific transaction handling."""
    FALLBACK_GAS_LIMIT: int
    GAS_BUFFER: float
    ARBITRUM_GAS_BUFFER: float
    BASE_GAS_BUFFER: float
    def __init__(self) -> None: ...
    def get_routing_strategy(self):
        '''Get the Enso routing strategy from environment variable.

        Returns:
            str: The routing strategy to use for Enso transactions.
                  Defaults to "router" if not set.
        '''
    @property
    def protocol(self) -> Protocol: ...
    @property
    def supported_actions(self) -> dict[ActionType, Callable]: ...
    def handle_action(self, action_type: ActionType, params: Any, web3: Web3, protocol_sdk: ISDK, action: Action, network: Network, chain: Chain, block_identifier: int | None = None) -> list[Transaction]:
        """Delegate to the appropriate handler method."""
    def estimate_gas(self, transaction: Transaction, web3: Web3, network: Network, chain: Chain, block_identifier: int | None = None) -> int:
        """
        Apply chain-specific buffers to Enso API gas estimates.
        """
    def handle_approve(self, params: ApproveParams, web3: Web3, protocol_sdk: ISDK, action: Action, network: Network, chain: Chain, block_identifier: int | None = None) -> list[Transaction]:
        """Handle token approvals using the Enso API."""
    def handle_swap(self, params: SwapParams, web3: Web3, protocol_sdk: ISDK, action: Action, network: Network, chain: Chain, block_identifier: int | None = None) -> list[Transaction]:
        """Handle swaps using the Enso API."""
