from __future__ import annotations
from maleo_foundation.models.transfers.results.service.general import BaseServiceGeneralResultsTransfers
from maleo_token.models.transfers.general import TokenTransfers

class MaleoTokenResultsTransfers:
    class Fail(BaseServiceGeneralResultsTransfers.Fail): pass

    class Generate(BaseServiceGeneralResultsTransfers.SingleData):
        data:TokenTransfers