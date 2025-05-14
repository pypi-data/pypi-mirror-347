from maleo_foundation.managers.client.base import ClientHTTPController
from maleo_foundation.models.transfers.results.client.controllers.http import BaseClientHTTPControllerResults
from maleo_token.models.transfers.parameters import MaleoTokenParametersTransfers

class MaleoTokenHTTPController(ClientHTTPController):
    async def generate(self, parameters:MaleoTokenParametersTransfers.Base) -> BaseClientHTTPControllerResults:
        """Generate token from MaleoAccess"""
        async with self._manager.get_client() as client:
            #* Define URL
            url = f"{self._manager.url.api}/v1/authentication/token"

            #* Declare body
            json = parameters.model_dump()

            #* Declare headers
            headers = {
                "Content-Type": "application/json"
            }

            #* Send request and wait for response
            response = await client.post(url=url, json=json, headers=headers)
            return BaseClientHTTPControllerResults(response=response)