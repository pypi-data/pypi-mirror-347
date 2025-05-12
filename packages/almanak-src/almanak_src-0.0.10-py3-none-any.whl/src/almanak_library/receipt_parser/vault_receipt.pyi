from _typeshed import Incomplete
from pprint import pprint as pprint
from src.almanak_library.enums import ActionType as ActionType, Chain as Chain, Network as Network, Protocol as Protocol, TransactionType as TransactionType
from src.almanak_library.init_sdk import get_protocol_sdk as get_protocol_sdk
from src.almanak_library.models.action import Action as Action
from src.almanak_library.models.receipt import Receipt as Receipt, SettleDepositReceipt as SettleDepositReceipt, SettleRedeemReceipt as SettleRedeemReceipt, UpdateTotalAssetsReceipt as UpdateTotalAssetsReceipt
from src.almanak_library.models.sdk import ISDK as ISDK
from src.almanak_library.receipt_parser.i_receipt_parser import IReceiptParser as IReceiptParser
from src.transaction_builder.protocols.vault.vault_sdk import VaultSDK as VaultSDK
from src.utils.config import Config as Config
from src.utils.logger import get_logger as get_logger
from typing import Any

DEBUG: Incomplete
logger: Incomplete

class ReceiptParserVault(IReceiptParser):
    """
    Receipt parser for Vault-specific actions.
    Handles parsing transaction receipts for actions:
    - SETTLE_VAULT_DEPOSIT
    - SETTLE_VAULT_REDEEM
    - PROPOSE_VAULT_VALUATION
    """
    action_map: Incomplete
    protocol: Incomplete
    network: Incomplete
    chain: Incomplete
    sdk: Incomplete
    EVENT_SIGNATURES: Incomplete
    def __init__(self, protocol: Protocol, network: Network, chain: Chain) -> None: ...
    def initialize_sdk(self) -> ISDK: ...
    def find_receipt_by_transaction_hash(self, transaction_hash: str, receipts: list[dict[str, Any]]) -> dict[str, Any] | None:
        """
        Find a receipt that matches the given transactionHash from a list of receipts.

        Args:
            transaction_hash (str): The transaction hash to search for.
            receipts (List[Dict[str, Any]]): The list of receipts to search within.

        Returns:
            Optional[Dict[str, Any]]: The matching receipt if found, otherwise None.
        """
    def extract_settle_deposit_event(self, receipt: dict[str, Any], vault_address: str) -> dict[str, Any] | None:
        """
        Extract the SettleDeposit event from transaction logs.
        This event is emitted by the settleDeposit function.

        Args:
            receipt: The transaction receipt
            vault_address: The vault address

        Returns:
            Optional[Dict[str, Any]]: The processed SettleDeposit event or None if not found
        """
    def extract_total_assets_updated_event(self, receipt: dict[str, Any], vault_address: str) -> dict[str, Any] | None:
        """
        Extract the TotalAssetsUpdated event from transaction logs.
        This event is emitted when total assets are updated during settlement.

        Args:
            receipt: The transaction receipt
            vault_address: The vault address

        Returns:
            Optional[Dict[str, Any]]: The processed TotalAssetsUpdated event or None if not found
        """
    def extract_settle_redeem_event(self, receipt: dict[str, Any], vault_address: str) -> dict[str, Any] | None:
        """
        Extract the SettleRedeem event from transaction logs.
        This event is emitted by the settleRedeem function.

        Args:
            receipt: The transaction receipt
            vault_address: The vault address

        Returns:
            Optional[Dict[str, Any]]: The processed SettleRedeem event or None if not found
        """
    def get_fee_info(self, receipt: dict[str, Any], vault_address: str) -> dict[str, Any]:
        '''
        Extract fee information from transaction receipts.
        Looks for HighWaterMarkUpdated event and Transfer events to fee receivers.

        Args:
            receipt: The transaction receipt
            vault_address: The vault address

        Returns:
            Dict[str, Any]: Dictionary containing fee information
            {
                "old_high_water_mark": int,
                "new_high_water_mark": int,
                "protocol_fee_shares": int,
                "manager_fee_shares": int
            }
        '''
    def settle_deposit_parser(self, action: Action, chain: Chain, transfer_offset: int, multicall_action: bool, receipts: list[dict[str, Any]]) -> tuple[Receipt | None, int]:
        """
        Parse the receipt for a SETTLE_VAULT_DEPOSIT action.
        Tries to extract multiple relevant events:
        1. TotalAssetsUpdated event - from settleDeposit function
        2. Fees Taken - from settleDeposit function
        3. SettleDeposit event - from settleDeposit function
        4. SettleRedeem event - from settleDeposit function

        Some events may be optional depending on the specific operation.
        """
    def settle_redeem_parser(self, action: Action, chain: Chain, transfer_offset: int, multicall_action: bool, receipts: list[dict[str, Any]]) -> tuple[Receipt | None, int]:
        """
        Parse the receipt for a SETTLE_VAULT_REDEEM action.
        Tries to extract multiple relevant events:
        1. TotalAssetsUpdated event - from settleRedeem function
        2. Fees Taken - from settleRedeem function
        3. SettleRedeem event - from settleRedeem function

        Some events may be optional depending on the specific operation.
        """
    def update_total_assets_parser(self, action: Action, chain: Chain, transfer_offset: int, multicall_action: bool, receipts: list[dict[str, Any]]) -> tuple[Receipt | None, int]:
        """
        Parse the receipt for a PROPOSE_VAULT_VALUATION action.
        Looks for NewTotalAssetsUpdated event in the logs to get the updated total assets.
        """
