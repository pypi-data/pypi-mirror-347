from _typeshed import Incomplete
from src.almanak_library.enums import Chain as Chain, Network as Network, Protocol as Protocol
from src.almanak_library.models.sdk import ISDK as ISDK
from typing import Any

class SDKRegistry:
    def __init__(self) -> None: ...
    def register_sdk(self, protocol: Protocol, network: Network, chain: Chain, sdk_class: type[ISDK], config: dict[str, Any] | None = None):
        """Register an SDK class with optional configuration."""
    def get_sdk_class(self, protocol: Protocol, network: Network, chain: Chain) -> type[ISDK]:
        """Get the SDK class for a protocol/network/chain combination."""
    def get_protocol_config(self, protocol: Protocol) -> dict[str, Any]:
        """Get the configuration for a protocol."""

sdk_registry: Incomplete
