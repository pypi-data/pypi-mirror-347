from _typeshed import Incomplete
from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from pydantic import BaseModel
from typing import Any

class RoutingStrategy(str, Enum):
    ENSO_WALLET = 'ensowallet'
    ROUTER = 'router'
    DELEGATE = 'delegate'

class TokenType(str, Enum):
    DEFI = 'defi'
    BASE = 'base'

class RouteParams(BaseModel):
    from_address: str
    token_in: list[str]
    token_out: list[str]
    amount_in: list[int]
    chain_id: int | str | Enum
    routing_strategy: RoutingStrategy | None
    receiver: str | None
    spender: str | None
    amount_out: list[int] | None
    min_amount_out: list[int] | None
    slippage: str | int | None
    fee: list[str] | None
    fee_receiver: str | None
    disable_rfqs: bool | None
    ignore_aggregators: list[str] | None
    ignore_standards: list[str] | None
    def set_token_decimals(self, token_address: str, decimals: int) -> None:
        """Set decimals for a token."""
    def get_token_decimals(self, token_address: str) -> int:
        """Get decimals for a token, throw error if not set."""
    def to_api_format(self) -> dict[str, Any]:
        """Convert parameters to API format with wei conversion."""
    @classmethod
    def validate_chain_id(cls, v):
        """Convert chain_id to numeric value and validate it's a supported chain."""
    @classmethod
    def validate_ethereum_address(cls, v): ...
    @classmethod
    def validate_token_address(cls, v): ...

class Network(BaseModel):
    id: int
    name: str
    is_connected: bool
    model_config: Incomplete
    def __init__(self, id: int, name: str, isConnected: bool = None, is_connected: bool = None, **kwargs) -> None: ...

class Price(BaseModel):
    decimals: int
    price: Decimal
    address: str
    symbol: str
    timestamp: int
    chain_id: int
    confidence: float | None
    model_config: Incomplete
    def __init__(self, decimals: int, price: Decimal | str, address: str, symbol: str, timestamp: int, chain_id: int, confidence: float = None, **kwargs) -> None: ...

class Transaction(BaseModel):
    data: str
    to: str
    from_address: str
    value: str
    model_config: Incomplete
    def __init__(self, data: str, to: str, value: str, **kwargs) -> None: ...

class Hop(BaseModel):
    token_in: list[str]
    token_out: list[str]
    protocol: str
    action: str
    primary: str
    internal_routes: list[str]
    model_config: Incomplete
    def __init__(self, token_in: list[str] = None, token_out: list[str] = None, protocol: str = None, action: str = None, primary: str = None, internal_routes: list[str] = None, tokenIn: list[str] = None, tokenOut: list[str] = None, internalRoutes: list[str] = None, **kwargs) -> None: ...

@dataclass
class RouteTransaction:
    gas: str
    amount_out: dict[str, Any]
    price_impact: float | None
    fee_amount: list[str]
    created_at: int
    tx: Transaction
    route: list[Hop]
    chain_id: int | None = ...
    def __init__(self, gas: str, tx: dict[str, Any] = None, route: list[dict[str, Any]] = None, amountOut: dict[str, Any] = None, priceImpact: float | None = None, feeAmount: list[str] = None, createdAt: int = None, chainId: int | None = None, amount_out: dict[str, Any] = None, price_impact: float | None = None, fee_amount: list[str] = None, created_at: int = None, chain_id: int | None = None) -> None:
        """Initialize RouteTransaction object.

        Args:
            gas: Gas estimate
            tx: Transaction details
            route: Route details
            amountOut/amount_out: Amount of output token
            priceImpact/price_impact: Price impact in basis points (1 bp = 0.01%).
                                    For example, 300 basis points = 3%.
            feeAmount/fee_amount: Fee amounts
            createdAt/created_at: Timestamp
            chainId/chain_id: Chain ID
        """
    def get_price_impact_percentage(self) -> float | None:
        """Get price impact as a percentage.

        Returns:
            Price impact as a percentage (e.g., 3.0 for 3%) or None if not available.
            Converts from basis points (1 bp = 0.01%) to percentage.
        """
    def get_human_readable_amount_out(self) -> str:
        """Convert amount_out to human readable format if SDK is in human readable mode."""

@dataclass
class WalletBalance:
    token: str
    amount: str
    decimals: int
    price: str

@dataclass
class TokenMetadata:
    symbol: str | None
    name: str | None
    logos_uri: list[str] | None

@dataclass
class Token:
    address: str
    chain_id: int
    type: TokenType
    decimals: int
    metadata: TokenMetadata | None = ...
    underlying_tokens: list['Token'] | None = ...
    protocol_slug: str | list[str] | None = ...
    project: str | None = ...
    apy: Decimal | None = ...
    primary_address: str | None = ...

class Protocol(BaseModel):
    slug: str
    name: str
    description: str | None
    url: str | None
    logos_uri: list[str] | None
    chains: list[Network]
    model_config: Incomplete
    def __init__(self, slug: str, name: str, description: str | None = None, url: str | None = None, logosUri: list[str] | None = None, logos_uri: list[str] | None = None, chains: list[dict] = None, **kwargs) -> None: ...

@dataclass
class StandardAction:
    action: str
    name: str
    function_names: list[str]
    supported_chains: list[Network]
    inputs: list[str]
    def __init__(self, action: str, name: str, functionNames: list[str] = None, function_names: list[str] = None, supported_chains: list[dict] = None, supportedChains: list[dict] = None, inputs: list[str] = None) -> None: ...

@dataclass
class Quote:
    amount_out: str
    gas: str | None = ...
    price_impact: float | None = ...
    created_at: int | None = ...
    tx: Transaction | None = ...
    route: list[Hop] | None = ...
    chain_id: int | None = ...
    def __init__(self, amountOut: str, gas: str | None = None, tx: dict[str, Any] | None = None, route: list[dict[str, Any]] | None = None, priceImpact: float | int | None = None, createdAt: int | None = None, chainId: int | None = None) -> None:
        """Initialize Quote object.

        Args:
            amountOut: Amount of output token
            gas: Gas estimate
            tx: Transaction details
            route: Route details
            priceImpact: Price impact in basis points (1 bp = 0.01%). For example, 300 basis points = 3%.
            createdAt: Timestamp
            chainId: Chain ID
        """
    def get_price_impact_percentage(self) -> float | None:
        """Get price impact as a percentage.

        Returns:
            Price impact as a percentage (e.g., 3.0 for 3%) or None if not available.
            Converts from basis points (1 bp = 0.01%) to percentage.
        """

@dataclass
class VolumeData:
    total_volume: str
    total_transactions: int
    chain_id: int
    def __init__(self, totalVolume: str | float | int, totalTransactions: int, chainId: int) -> None: ...

@dataclass
class Standard:
    protocol: Protocol
    forks: list[Protocol]
    actions: list[StandardAction]
    def __init__(self, protocol: dict, forks: list[dict], actions: list[dict]) -> None: ...
