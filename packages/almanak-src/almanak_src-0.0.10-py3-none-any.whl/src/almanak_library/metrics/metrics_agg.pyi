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
IS_AGENT_DEPLOYMENT: Incomplete

def default_agent_id(): ...
def default_user_id(): ...

class MetricAggType(Enum):
    INITIALIZATION = 'INITIALIZATION'
    TEARDOWN = 'TEARDOWN'
    STRATEGY_BALANCE = 'STRATEGY_BALANCE'
    WALLET_BALANCE = 'WALLET_BALANCE'
    SNAPSHOT = 'SNAPSHOT'
    REBALANCE_TRIGGER = 'REBALANCE_TRIGGER'
    POSITION_UPDATE = 'POSITION_UPDATE'
    APY_SNAPSHOT = 'APY_SNAPSHOT'

class MetricsAggTable(SQLModel, table=True):
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

class MetricsAggHandler:
    engine: Incomplete
    def __init__(self, db_connection_string) -> None: ...
    def create_tables(self) -> None: ...
    def add_metric(self, metric: MetricsAggTable) -> None: ...
    def get_metrics_agg(self, user_id: str | None = None, agent_id: str | None = None, strategy_id: str | None = None, metric_type: MetricAggType | str | None = None, wallet_address: str | None = None): ...
