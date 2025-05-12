import uuid
from _typeshed import Incomplete
from decimal import Decimal as Decimal
from src.almanak_library.enums import ActionType as ActionType, ExecutionStatus as ExecutionStatus
from src.almanak_library.metrics.metrics_actions import MetricActionType as MetricActionType, MetricsActionHandler as MetricsActionHandler, MetricsActionTable as MetricsActionTable
from src.almanak_library.models.action import Action as Action
from src.almanak_library.models.action_bundle import ActionBundle as ActionBundle
from src.utils.logger import get_logger as get_logger
from src.utils.utils import get_db_connection_string as get_db_connection_string

logger: Incomplete

class MetricsLogger:
    """
    unique identifier of metrics table:
    (metric_type, strategy_id, action_id)

    """
    logger_map: Incomplete
    metrics_action_handler: Incomplete
    def __init__(self) -> None: ...
    def should_log_metrics_for_action(self, action_bundle: ActionBundle, action_id: uuid.UUID) -> bool:
        """
        TODO: Add support for partial execution within an action if an action has multiple transactions.
        """
    def log_metrics(self, action_bundle: ActionBundle): ...
    def log_tx_gas_cost(self, action: Action, strategy_id: str, wallet_address: str): ...
    def log_lp_fees(self, fees0: int, fees1: int, strategy_id: str, wallet_address: str, action_id: uuid.UUID, bundle_id: uuid.UUID, block_number: int): ...
    def log_wrap_metrics(self, strategy_id: str, action: Action): ...
    def log_unwrap_metrics(self, strategy_id: str, action: Action): ...
    def log_approve_metrics(self, strategy_id: str, action: Action): ...
    def log_swap_metrics(self, strategy_id: str, action: Action): ...
    def log_open_position_metrics(self, strategy_id: str, action: Action): ...
    def log_close_position_metrics(self, strategy_id: str, action: Action): ...
    def log_generic_metrics(self, strategy_id: str, action: Action):
        """Generic metrics logger for actions that just need basic execution details and gas tracking."""
