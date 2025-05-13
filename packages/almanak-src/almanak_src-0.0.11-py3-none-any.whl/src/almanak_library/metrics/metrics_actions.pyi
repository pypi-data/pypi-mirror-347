from _typeshed import Incomplete
from enum import Enum
from sqlmodel import SQLModel
from src.almanak_library.metrics.engine import get_metrics_engine as get_metrics_engine
from src.utils.config import Config as Config
from src.utils.logger import get_logger as get_logger
from src.utils.proxy_validator import IS_SQL_PROXY as IS_SQL_PROXY, USE_SQL_PROXY as USE_SQL_PROXY
from src.utils.utils import get_db_connection_string as get_db_connection_string

logger: Incomplete
METRICS_DB_CONNECTION_STRING: Incomplete
ENABLE_DEBUG: bool
IS_AGENT_DEPLOYMENT: Incomplete

def default_agent_id(): ...
def default_user_id(): ...

class MetricActionType(Enum):
    GAS = 'GAS'
    FEES = 'FEES'
    WRAP = 'WRAP'
    UNWRAP = 'UNWRAP'
    APPROVE = 'APPROVE'
    SWAP = 'SWAP'
    OPEN_POSITION = 'OPEN_POSITION'
    CLOSE_POSITION = 'CLOSE_POSITION'

class MetricsActionTable(SQLModel, table=True):
    __tablename__: str
    id: int
    time: str
    block_number: int | None
    metric_type: str
    strategy_id: str
    action_id: str
    bundle_id: str
    wallet_address: str
    details: dict
    agent_id: str | None
    user_id: str | None
    __table_args__: Incomplete

class MetricsActionHandler:
    engine: Incomplete
    def __init__(self, db_connection_string) -> None: ...
    def create_tables(self) -> None: ...
    def add_metric(self, metric: MetricsActionTable) -> None: ...
    def get_metrics_action(self, user_id: str | None = None, agent_id: str | None = None, strategy_id: str | None = None, metric_type: MetricActionType | None = None, wallet_address: str | None = None): ...
    def metric_exists(self, metric_type: str, action_id: str) -> bool: ...
