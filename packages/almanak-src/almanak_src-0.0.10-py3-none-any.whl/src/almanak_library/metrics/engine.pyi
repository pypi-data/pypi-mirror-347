from _typeshed import Incomplete
from pathlib import Path as Path
from sqlalchemy.future.engine import Engine as Engine
from src.utils.config import Config as Config
from src.utils.logger import get_logger as get_logger
from src.utils.utils import get_db_connection_string as get_db_connection_string

logger: Incomplete
METRICS_DB_CONNECTION_STRING: Incomplete

def get_metrics_engine(db_connection_string: str = ...) -> Engine: ...
