import abc
from _typeshed import Incomplete
from abc import ABC, abstractmethod
from src.almanak_library.enums import ActionType as ActionType, Chain as Chain, Network as Network, Protocol as Protocol
from src.almanak_library.models.action import Action as Action
from src.almanak_library.models.sdk import ISDK as ISDK
from src.almanak_library.models.transaction import Transaction as Transaction
from src.utils.utils import get_blocknative_tip as get_blocknative_tip, get_logger as get_logger, retry_get_block as retry_get_block
from typing import Any, Callable
from web3 import Web3 as Web3

logger: Incomplete

class ProtocolAdapter(ABC, metaclass=abc.ABCMeta):
    """Base adapter interface for protocol-specific transaction handling."""
    GAS_BUFFER: float
    FEE_BUFFER: float
    ARBITRUM_ALCHEMY_GAS_BUFFER: float
    BASE_GAS_BUFFER: float
    def __init__(self) -> None: ...
    def set_fee_buffers(self, chain: Chain, network: Network):
        """Set appropriate fee buffers based on chain and network"""
    def get_transaction_fees(self, web3: Web3, chain: Chain, network: Network, block_identifier: Incomplete | None = None) -> dict[str, int]:
        """
        Get transaction fees based on current network conditions.
        Uses blocknative tip when available, otherwise falls back to web3 max_priority_fee.
        """
    @property
    @abstractmethod
    def protocol(self) -> Protocol:
        """Return the protocol this adapter handles."""
    @property
    @abstractmethod
    def supported_actions(self) -> dict[ActionType, Callable]:
        """Return a dictionary mapping action types to handler methods."""
    @abstractmethod
    def handle_action(self, action_type: ActionType, params: Any, web3: Web3, protocol_sdk: ISDK, action: Action, network: Network, chain: Chain, block_identifier: int | None = None) -> list[Transaction]:
        """Handle an action of the specified type."""
    def estimate_gas(self, transaction: Transaction, web3: Web3, network: Network, chain: Chain, block_identifier: int | None = None) -> int:
        """
        Estimate gas for Uniswap transactions using web3.
        """
