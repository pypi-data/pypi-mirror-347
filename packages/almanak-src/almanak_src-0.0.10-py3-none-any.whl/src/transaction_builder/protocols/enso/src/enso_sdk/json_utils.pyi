import json
from .models import Network as Network, Protocol as Protocol, StandardAction as StandardAction, Token as Token, TokenMetadata as TokenMetadata

class EnsoJSONEncoder(json.JSONEncoder):
    """
    Custom JSON encoder for Enso SDK classes.

    This encoder handles serialization of custom classes like Network, Protocol, etc.
    that are not natively JSON serializable.
    """
    def default(self, obj): ...
