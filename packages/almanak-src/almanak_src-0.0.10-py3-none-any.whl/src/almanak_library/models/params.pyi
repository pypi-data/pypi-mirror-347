import abc
from abc import ABC, abstractmethod
from pydantic import BaseModel
from src.almanak_library.enums import ActionType as ActionType, SwapSide as SwapSide
from typing import Any

class Params(BaseModel, ABC, metaclass=abc.ABCMeta):
    type: ActionType
    context: dict[str, Any]
    @abstractmethod
    def validate(self) -> None: ...
    def model_dump(self) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Params: ...

class TransferParams(Params):
    type: ActionType
    from_address: str
    to_address: str
    amount: int
    nonce_counter: int | None
    def must_not_be_empty(cls, v): ...
    def validate(self) -> None: ...

class WrapParams(Params):
    type: ActionType
    from_address: str
    amount: int
    def must_not_be_empty(cls, v): ...
    def validate(self) -> None: ...

class UnwrapParams(Params):
    type: ActionType
    from_address: str
    token_address: str
    amount: int
    def must_not_be_empty(cls, v): ...
    def validate(self) -> None: ...

class ApproveParams(Params):
    type: ActionType
    token_address: str
    spender_address: str
    from_address: str
    amount: int | None
    def must_not_be_empty(cls, v): ...
    def validate(self) -> None: ...

class SwapParams(Params):
    type: ActionType
    tokenIn: str
    tokenOut: str
    recipient: str
    amount: int
    side: SwapSide | None
    fee: int | None
    slippage: float | None
    amountOutMinimum: int | None
    amountInMaximum: int | None
    transfer_eth_in: bool | None
    sqrtPriceLimitX96: int | None
    def must_not_be_empty(cls, v): ...
    def must_be_positive(cls, v): ...
    def validate(self) -> None: ...
    def model_dump(self, *args, **kwargs): ...

class OpenPositionParams(Params):
    type: ActionType
    token0: str
    token1: str
    fee: int
    price_lower: float
    price_upper: float
    amount0_desired: int
    amount1_desired: int
    recipient: str
    amount0_min: int | None
    amount1_min: int | None
    slippage: float | None
    def must_not_be_empty(cls, v): ...
    def must_be_positive(cls, v): ...
    def amount_desired_must_be_non_negative(cls, v): ...
    def validate(self) -> None: ...

class ClosePositionParams(Params):
    type: ActionType
    position_id: int
    recipient: str
    token0: str
    token1: str
    amount0_min: int | None
    amount1_min: int | None
    slippage: float | None
    pool_address: str | None
    def must_not_be_empty(cls, v): ...
    def validate(self) -> None: ...

class UpdateTotalAssetsParams(Params):
    type: ActionType
    vault_address: str
    valuator_address: str
    new_total_assets: int
    pending_deposits: int
    def must_not_be_empty(cls, v): ...
    def validate(self) -> None: ...

class SettleDepositParams(Params):
    type: ActionType
    vault_address: str
    safe_address: str
    total_assets: int
    def must_not_be_empty(cls, v): ...
    def validate(self) -> None: ...

class SettleRedeemParams(Params):
    type: ActionType
    vault_address: str
    safe_address: str
    total_assets: int
    def must_not_be_empty(cls, v): ...
    def validate(self) -> None: ...
