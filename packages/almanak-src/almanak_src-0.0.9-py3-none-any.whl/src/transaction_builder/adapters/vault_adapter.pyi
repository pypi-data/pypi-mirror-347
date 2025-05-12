from _typeshed import Incomplete
from src.almanak_library.enums import ActionType as ActionType, Chain as Chain, Network as Network, Protocol as Protocol, TransactionType as TransactionType
from src.almanak_library.models.action import Action as Action
from src.almanak_library.models.params import SettleDepositParams as SettleDepositParams, SettleRedeemParams as SettleRedeemParams, UpdateTotalAssetsParams as UpdateTotalAssetsParams
from src.almanak_library.models.sdk import ISDK as ISDK
from src.almanak_library.models.transaction import Transaction as Transaction
from src.transaction_builder.adapters.base_adapter import ProtocolAdapter as ProtocolAdapter
from src.utils.utils import get_logger as get_logger
from typing import Any, Callable
from web3 import Web3 as Web3

logger: Incomplete

class VaultAdapter(ProtocolAdapter):
    def __init__(self) -> None: ...
    @property
    def protocol(self) -> Protocol: ...
    @property
    def supported_actions(self) -> dict[ActionType, Callable]: ...
    def handle_action(self, action_type: ActionType, params: Any, web3: Web3, protocol_sdk: ISDK, action: Action, network: Network, chain: Chain, block_identifier: int | None = None) -> list[Transaction]:
        """Delegate to the appropriate handler method."""
    def handle_update_total_assets(self, params: UpdateTotalAssetsParams, web3: Web3, protocol_sdk: ISDK, action: Action, network: Network, chain: Chain, block_identifier: int | None = None) -> list[Transaction]:
        """
        Handles the process of updating total assets in the vault.
        """
    def handle_settle_deposit(self, params: SettleDepositParams, web3: Web3, protocol_sdk: ISDK, action: Action, network: Network, chain: Chain, block_identifier: int | None = None) -> list[Transaction]:
        """
        Handles the process of settling deposits in the vault.
        """
    def handle_settle_redeem(self, params: SettleRedeemParams, web3: Web3, protocol_sdk: ISDK, action: Action, network: Network, chain: Chain, block_identifier: int | None = None) -> list[Transaction]:
        """
        Handles the process of settling redemptions in the vault.
        """
