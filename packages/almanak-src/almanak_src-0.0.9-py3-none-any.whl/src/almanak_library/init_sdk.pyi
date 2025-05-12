from src.almanak_library.enums import Chain as Chain, Network as Network, Protocol as Protocol
from src.almanak_library.sdk_registry import sdk_registry as sdk_registry
from src.transaction_builder.protocols.enso.src.enso_sdk.client import EnsoSDK as EnsoSDK
from src.transaction_builder.protocols.uniswap_v3.uniswap_v3_sdk import UniswapV3SDK as UniswapV3SDK
from src.transaction_builder.protocols.vault.vault_sdk import VaultSDK as VaultSDK
from src.utils.config import Config as Config
from src.utils.utils import get_web3_by_network_and_chain as get_web3_by_network_and_chain

def get_protocol_sdk(protocol: Protocol, network: Network, chain: Chain):
    """Get an SDK instance for a protocol with proper configuration."""
def initialize_sdks() -> None: ...
