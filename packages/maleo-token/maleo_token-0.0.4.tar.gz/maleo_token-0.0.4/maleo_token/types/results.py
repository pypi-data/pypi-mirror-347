from typing import Union
from maleo_token.models.transfers.results import MaleoTokenResultsTransfers

class MaleoTokenResultsTypes:
    Generate = Union[
        MaleoTokenResultsTransfers.Fail,
        MaleoTokenResultsTransfers.Generate
    ]