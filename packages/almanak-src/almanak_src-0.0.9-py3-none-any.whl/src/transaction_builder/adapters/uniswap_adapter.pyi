from _typeshed import Incomplete
from src.almanak_library.enums import ActionType as ActionType, Chain as Chain, Network as Network, Protocol as Protocol, SwapSide as SwapSide, TransactionType as TransactionType
from src.almanak_library.models.action import Action as Action
from src.almanak_library.models.params import ApproveParams as ApproveParams, ClosePositionParams as ClosePositionParams, OpenPositionParams as OpenPositionParams, SwapParams as SwapParams, TransferParams as TransferParams, UnwrapParams as UnwrapParams, WrapParams as WrapParams
from src.almanak_library.models.sdk import ISDK as ISDK
from src.almanak_library.models.transaction import Transaction as Transaction
from src.transaction_builder.adapters.base_adapter import ProtocolAdapter as ProtocolAdapter
from src.utils.utils import get_logger as get_logger
from typing import Any, Callable
from web3 import Web3 as Web3

logger: Incomplete

class UniswapAdapter(ProtocolAdapter):
    """Adapter for Uniswap protocol-specific transaction handling."""
    GAS_BUFFER: float
    ARBITRUM_ALCHEMY_GAS_BUFFER: float
    BASE_GAS_BUFFER: float
    def __init__(self) -> None: ...
    @property
    def protocol(self) -> Protocol: ...
    @property
    def supported_actions(self) -> dict[ActionType, Callable]: ...
    def handle_action(self, action_type: ActionType, params: Any, web3: Web3, protocol_sdk: ISDK, action: Action, network: Network, chain: Chain, block_identifier: int | None = None) -> list[Transaction]:
        """Delegate to the appropriate handler method."""
    def handle_transfer(self, params: TransferParams, web3: Web3, protocol_sdk: ISDK, action: Action, network: Network, chain: Chain, block_identifier: int | None = None) -> list[Transaction]:
        """
        Handles the process of transferring tokens from one address to another.
        """
    def handle_wrap(self, params: WrapParams, web3: Web3, protocol_sdk: ISDK, action: Action, network: Network, chain: Chain, block_identifier: int | None = None) -> list[Transaction]:
        """
        the standard ERC20 deposit function for WETH does not inherently support a deadline parameter
        """
    def handle_unwrap(self, params: UnwrapParams, web3: Web3, protocol_sdk: ISDK, action: Action, network: Network, chain: Chain, block_identifier: int | None = None) -> list[Transaction]:
        """
        the standard ERC20 withdraw function for Wrap Token does not inherently support a deadline parameter
        """
    def handle_approve(self, params: ApproveParams, web3: Web3, protocol_sdk: ISDK, action: Action, network: Network, chain: Chain, block_identifier: int | None = None) -> list[Transaction]:
        """
        the ERC20 approve function itself does not natively support a deadline parameter
        """
    def handle_swap(self, params: SwapParams, web3: Web3, protocol_sdk: ISDK, action: Action, network: Network, chain: Chain, block_identifier: int | None = None) -> list[Transaction]:
        """
        Handles Uniswap V3 swaps
        """
    def handle_open_position(self, params: OpenPositionParams, web3: Web3, protocol_sdk: ISDK, action: Action, network: Network, chain: Chain, block_identifier: int | None = None) -> list[Transaction]:
        """
        Handles the process of opening a new liquidity position.
        It is important to note that you need to call the approve method for both tokens involved
        in the liquidity position before calling this function. The approve method should authorize the position manager contract
        to spend the specified amount of tokens on behalf of the user's address.
        """
    def handle_close_position_multicall(self, params: ClosePositionParams, web3: Web3, protocol_sdk: ISDK, action: Action, network: Network, chain: Chain, block_identifier: int | None = None) -> list[Transaction]:
        """
        Handles closing a liquidity position using multicall
        """
