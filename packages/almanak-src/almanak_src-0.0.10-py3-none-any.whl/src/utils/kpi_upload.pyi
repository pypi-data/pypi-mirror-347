from _typeshed import Incomplete
from enum import Enum as Enum
from pydantic import BaseModel
from src.utils.config import Config as Config

IS_AGENT_DEPLOYMENT: Incomplete
KPIS_FILENAME: str
storage_client: Incomplete

class AgentKpis(BaseModel):
    ROI: float | None
    APY: float | None
    timestamp: str
    extra: dict | None

def upload_kpis(agent_kpis: AgentKpis, strategy_id: str | None = None):
    """
    If strategy id is None, the kpi is per the global agent and not per strategy
    """
def upload_kpi_to_storage_gcs(agent_kpis: AgentKpis, strategy_id: str): ...
def upload_kpi_to_storage_local(agent_kpis: AgentKpis, strategy_id: str): ...
