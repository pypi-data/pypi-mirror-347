from src.almanak_library.enums import Protocol as Protocol
from src.transaction_builder.adapters.base_adapter import ProtocolAdapter as ProtocolAdapter

class ProtocolAdapterFactory:
    """Factory for creating protocol-specific adapters."""
    @classmethod
    def get_adapter(cls, protocol: Protocol) -> ProtocolAdapter:
        """Get or create an adapter for the specified protocol."""
