from _typeshed import Incomplete
from ast import parse as parse
from pprint import pprint as pprint
from src.almanak_library.custom_exceptions import SimulationError as SimulationError
from src.almanak_library.enums import ActionType as ActionType, Chain as Chain, CoSigners as CoSigners, ExecutionStatus as ExecutionStatus, Network as Network, Protocol as Protocol
from src.almanak_library.init_sdk import get_protocol_sdk as get_protocol_sdk
from src.almanak_library.models.action import Action as Action
from src.almanak_library.models.action_bundle import ActionBundle as ActionBundle
from src.almanak_library.models.sdk import ISDK as ISDK
from src.almanak_library.models.transaction import Transaction as Transaction
from src.transaction_builder.adapters.adapter_factory import ProtocolAdapterFactory as ProtocolAdapterFactory
from src.utils.config import Config as Config
from src.utils.utils import get_logger as get_logger, get_web3_by_network_and_chain as get_web3_by_network_and_chain
from web3 import Web3 as Web3

IS_AGENT_DEPLOYMENT: Incomplete
logger: Incomplete

class TransactionManager:
    chain_protocol_dict: Incomplete
    chain_network_dict: Incomplete
    GAS_BUFFER: float
    ARBITRUM_ALCHEMY_GAS_BUFFER: float
    BASE_GAS_BUFFER: float
    def __init__(self) -> None: ...
    def build_transactions_from_action_bundle(self, action_bundle: ActionBundle, block_identifier: Incomplete | None = None) -> ActionBundle:
        """
        this function executes multiple actions in a single bundle.
        It uses simulate execution bundle to build the transactions, estimate the gas,
        so that the transactions that depends on a previous one can be simulated.

        # NOTE: actions within the bundle should have the same network and chain.
        """
    def parse_alchemy_result(self, results) -> None:
        """
        Parses the Alchemy simulation results to extract and log error details.

        This function handles its own exceptions to prevent them from propagating
        and stopping the program execution.

        Parameters:
        - results (list): The list of simulation results from Alchemy.
        """
