import argparse
from src.transaction_builder.protocols.enso.src.enso_sdk.client import EnsoSDK as EnsoSDK
from src.transaction_builder.protocols.enso.src.enso_sdk.exceptions import ValidationError as ValidationError

def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
def get_api_key(provided_key: str | None = None) -> str:
    """Get API key from args or environment."""
def get_supported_chains() -> list[str]:
    """Get list of supported chain names."""
def main() -> None:
    """Main entry point."""
