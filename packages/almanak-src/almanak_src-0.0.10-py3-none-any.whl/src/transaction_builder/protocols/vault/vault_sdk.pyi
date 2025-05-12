from _typeshed import Incomplete
from src.almanak_library.enums import Chain as Chain, Network as Network
from src.almanak_library.models.sdk import ISDK as ISDK
from src.strategy.models import VaultConfig as VaultConfig
from src.transaction_builder.protocols.transaction_utils import get_gas_buffer as get_gas_buffer, get_transaction_fees as get_transaction_fees
from src.utils.config import Config as Config
from src.utils.utils import get_logger as get_logger, get_web3_by_network_and_chain as get_web3_by_network_and_chain

logger: Incomplete

class VaultSDK(ISDK):
    """
    A Vault SDK containing the functions that will be called on the Almanak vault SC.
    """
    MAX_UINT_128: Incomplete
    MAX_UINT_256: Incomplete
    network: Incomplete
    chain: Incomplete
    web3: Incomplete
    vault_abi: Incomplete
    erc20_abi: Incomplete
    fee_registry_abi: Incomplete
    def __init__(self, network: Network, chain: Chain) -> None: ...
    def get_vault_contract(self, vault_address: str) -> object: ...
    def get_underlying_contract(self, vault_address: str) -> object: ...
    def get_fee_registry_contract(self, vault_address: str) -> object: ...
    def get_valuator_address(self, vault_address: str) -> str: ...
    def get_protocol_fee_receiver(self, vault_address: str) -> str:
        """
        Get the protocol fee receiver address for a vault.
        Uses the fee registry from the vault's roles storage.

        Args:
            vault_address: The address of the vault

        Returns:
            str: The protocol fee receiver address
        """
    def get_total_assets(self, vault_address: str, block_identifier: int | None = None) -> int:
        """
        Get the current total assets value from the vault contract.
        This is how much the vault thinks it has in assets.

        Returns:
            int: Current total assets value
        """
    def get_proposed_total_assets(self, vault_address: str, block_identifier: int | None = None) -> int:
        """
        Get the proposed total assets value from the vault contract.
        This is the value set by the valuator that has not yet been committed.

        This method directly accesses the contract storage to retrieve the newTotalAssets value
        from the diamond storage pattern used in the ERC7540 contract.

        Returns:
            int: Proposed total assets value (or MAX_UINT_256 if not set)
        """
    def valuator_update_total_assets(self, vault_address: str, valuator_address: str, new_total_assets: int, set_gas_override: int | None = None, block_identifier: int | None = None) -> dict:
        """
        Update the total assets in the vault contract.
        Can only be called by the valuator.

        Returns:
            dict: Transaction dictionary
        """
    def settle_deposit(self, vault_address: str, safe_address: str, total_assets: int, set_gas_override: int | None = None, block_identifier: int | None = None) -> dict:
        """
        Settle pending deposits in the vault contract. Only the Safe can call this.
        The safe needs to accept the on-chain value of total_assets from valuator before settling.
        Performance/Managing/Protocol Fees are taken by default when settling.
        Redemptions are also processed when settling deposits

        # TODO: Check that we will have enough assets in the safe to settle the deposit
        # and redemptions.

        Returns:
            dict: Transaction dictionary
        """
    def settle_redeem(self, vault_address: str, safe_address: str, total_assets: int, set_gas_override: int | None = None, block_identifier: int | None = None) -> dict:
        """
        Settle pending redemptions in the vault contract.
        Only the Safe can call this.
        The safe needs to accept the on-chain value of total_assets from valuator before settling.
        Performance/Managing/Protocol Fees are taken by default when settling.

        # TODO: Check that we will have enough assets in the safe to settle the redemption

        Returns:
            dict: Transaction dictionary
        """
    def get_pending_deposits(self, vault_address: str, block_identifier: int | None = None) -> int:
        """
        Get the amount of assets currently waiting in the deposit silo.

        Returns:
            pending_assets_amount: int
        """
    def get_required_assets_for_redemption(self, vault_address: str, include_pending_deposits: bool, block_identifier: int | None = None) -> int | None:
        """
        Calculate the amount of assets needed in the safe to process all pending redemptions.
        If include_pending_deposits is True,
        the amount of assets in the pending deposits will also be included.

        # TODO: Verify all addresses against the config
        Returns:
            int: required_assets or None if there are no pending redemptions
        """
    def get_pending_redemptions(self, vault_address: str, block_identifier: int | None = None) -> int:
        """
        Get the amount of shares currently waiting in the silo to be redeemed.

        Returns:
            int: Amount of shares pending redemption
        """
