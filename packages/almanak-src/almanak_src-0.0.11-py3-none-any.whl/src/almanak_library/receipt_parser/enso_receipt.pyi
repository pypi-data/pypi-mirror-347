from _typeshed import Incomplete
from src.almanak_library.enums import ActionType as ActionType, Chain as Chain, ExecutionStatus as ExecutionStatus, Network as Network, Protocol as Protocol, SwapSide as SwapSide, TransactionType as TransactionType
from src.almanak_library.init_sdk import get_protocol_sdk as get_protocol_sdk
from src.almanak_library.models.action import Action as Action
from src.almanak_library.models.receipt import ApproveReceipt as ApproveReceipt, Receipt as Receipt, SwapReceipt as SwapReceipt
from src.almanak_library.models.sdk import ISDK as ISDK
from src.almanak_library.receipt_parser.i_receipt_parser import IReceiptParser as IReceiptParser
from src.transaction_builder.protocols.enso.src.enso_sdk.client import EnsoSDK as EnsoSDK
from src.utils.config import Config as Config
from src.utils.logger import get_logger as get_logger
from typing import Any

DEBUG: Incomplete
logger: Incomplete

class ReceiptParserEnso(IReceiptParser):
    """
    Receipt parser for Enso protocol transactions.
    """
    action_map: Incomplete
    protocol: Incomplete
    network: Incomplete
    chain: Incomplete
    sdk: Incomplete
    def __init__(self, protocol: Protocol, network: Network, chain: Chain) -> None:
        """
        Initialize the Enso receipt parser.

        Args:
            protocol: The protocol (should be Protocol.ENSO)
            network: The network (e.g., Network.MAINNET)
            chain: The chain (e.g., Chain.BASE)
        """
    def initialize_sdk(self) -> ISDK:
        """
        Initialize the Enso SDK.

        Returns:
            An instance of the Enso SDK
        """
    def find_receipt_by_transaction_hash(self, transaction_hash: str, receipts: list[dict[str, Any]]) -> dict[str, Any] | None:
        """
        Find a receipt that matches the given transaction hash from a list of receipts.

        Args:
            transaction_hash: The transaction hash to search for
            receipts: The list of receipts to search within

        Returns:
            The matching receipt if found, otherwise None
        """
    def approve_parser(self, action: Action, chain: Chain, transfer_offset: int, multicall_action: bool, receipts: list[dict[str, Any]]) -> tuple[Receipt | None, int]:
        """
        Parse approve action receipts.

        Args:
            action: The approve action
            chain: The chain
            transfer_offset: Offset for transfer events in multicall transactions
            multicall_action: Whether this is part of a multicall
            receipts: The transaction receipts

        Returns:
            A tuple of (ApproveReceipt, used_transfers)
        """
    def swap_parser(self, action: Action, chain: Chain, transfer_offset: int, multicall_action: bool, receipts: list[dict[str, Any]]) -> tuple[Receipt | None, int]:
        """
        Parse swap action receipts for Enso protocol.

        For Enso swaps, we need to:
        1. Get the transaction receipt for gas info
        2. Use the SDK to get token balances before and after to determine amounts

        Args:
            action: The swap action
            chain: The chain
            transfer_offset: Offset for transfer events in multicall transactions
            multicall_action: Whether this is part of a multicall
            receipts: The transaction receipts

        Returns:
            A tuple of (SwapReceipt, used_transfers)
        """
