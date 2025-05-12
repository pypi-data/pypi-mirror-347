import abc
import uuid
from _typeshed import Incomplete
from abc import ABC
from pydantic import BaseModel
from src.almanak_library.enums import ActionType as ActionType, SwapSide as SwapSide
from typing import Any

class Receipt(BaseModel, ABC, metaclass=abc.ABCMeta):
    type: ActionType
    action_id: uuid.UUID
    bundle_id: uuid.UUID | None
    tx_hash: str
    tx_cost: int
    gas_used: int
    block_number: int
    model_config: Incomplete
    def model_dump(self, exclude: set[str] = ...) -> dict[str, Any]: ...
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Receipt: ...

class WrapReceipt(Receipt):
    type: ActionType
    action_id: uuid.UUID
    bundle_id: uuid.UUID | None
    tx_hash: str
    tx_cost: int
    gas_used: int
    block_number: int
    amount: int

class UnwrapReceipt(Receipt):
    type: ActionType
    action_id: uuid.UUID
    bundle_id: uuid.UUID | None
    tx_hash: str
    tx_cost: int
    gas_used: int
    block_number: int
    amount: int

class ApproveReceipt(Receipt):
    type: ActionType
    action_id: uuid.UUID
    bundle_id: uuid.UUID | None
    tx_hash: str
    tx_cost: int
    gas_used: int
    block_number: int

class OpenPositionReceipt(Receipt):
    type: ActionType
    action_id: uuid.UUID
    bundle_id: uuid.UUID | None
    tx_hash: str
    tx_cost: int
    gas_used: int
    block_number: int
    token0_symbol: str
    token1_symbol: str
    amount0: int
    amount1: int
    position_id: int
    bound_tick_lower: int
    bound_tick_upper: int
    bound_price_lower: float
    bound_price_upper: float
    pool_tick: int | None
    pool_spot_rate: float | None

class SwapReceipt(Receipt):
    type: ActionType
    action_id: uuid.UUID
    bundle_id: uuid.UUID | None
    tx_hash: str
    tx_cost: int
    gas_used: int
    block_number: int
    side: SwapSide | None
    tokenIn_symbol: str
    tokenOut_symbol: str
    amountIn: int
    amountOut: int | None
    def model_dump(self, *args, **kwargs): ...

class ClosePositionReceipt(Receipt):
    type: ActionType
    action_id: uuid.UUID
    bundle_id: uuid.UUID | None
    tx_hash: str
    tx_cost: int
    gas_used: int
    block_number: int
    position_id: int
    token0_symbol: str
    token1_symbol: str
    amount0: int
    amount1: int
    liquidity0: int
    liquidity1: int
    fees0: int
    fees1: int
    pool_tick: int | None
    pool_spot_rate: float | None

class SettleDepositReceipt(Receipt):
    type: ActionType
    action_id: uuid.UUID
    bundle_id: uuid.UUID | None
    tx_hash: str
    tx_cost: int
    gas_used: int
    block_number: int
    vault_address: str
    total_assets: int
    deposit_assets: int
    deposit_shares_minted: int
    deposit_total_supply: int | None
    deposit_total_assets: int | None
    redeem_assets_withdrawn: int
    redeem_shares_burned: int
    redeem_total_supply: int | None
    redeem_total_assets: int | None
    protocol_fee_shares_minted: int
    strategist_fee_shares_minted: int
    old_high_water_mark: int | None
    new_high_water_mark: int | None

class SettleRedeemReceipt(Receipt):
    type: ActionType
    action_id: uuid.UUID
    bundle_id: uuid.UUID | None
    tx_hash: str
    tx_cost: int
    gas_used: int
    block_number: int
    vault_address: str
    total_assets: int
    redeem_assets_withdrawn: int
    redeem_shares_burned: int
    redeem_total_supply: int | None
    redeem_total_assets: int | None
    protocol_fee_shares_minted: int
    strategist_fee_shares_minted: int
    old_high_water_mark: int | None
    new_high_water_mark: int | None

class UpdateTotalAssetsReceipt(Receipt):
    type: ActionType
    action_id: uuid.UUID
    bundle_id: uuid.UUID | None
    tx_hash: str
    tx_cost: int
    gas_used: int
    block_number: int
    vault_address: str
    valuator_address: str
    total_assets: int
