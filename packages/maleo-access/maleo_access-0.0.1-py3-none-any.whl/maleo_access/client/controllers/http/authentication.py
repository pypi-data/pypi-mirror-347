from maleo_foundation.managers.client.maleo import MaleoClientHTTPController
from maleo_foundation.models.transfers.results.client.controllers.http import BaseClientHTTPControllerResults
from maleo_access.models.transfers.parameters.general.authentication import MaleoAccessAuthenticationGeneralParametersTransfers

class MaleoAccessAuthenticationHTTPController(MaleoClientHTTPController):
    async def generate_token(self, parameters:MaleoAccessAuthenticationGeneralParametersTransfers.Base) -> BaseClientHTTPControllerResults:
        """Generate token from MaleoAccess"""
        async with self._manager.get_client() as client:
            #* Define URL
            url = f"{self._manager.url.api}/v1/authentication/"

            #* Declare body
            json = parameters.model_dump()

            #* Declare headers
            headers = {
                "Content-Type": "application/json"
            }

            #* Send request and wait for response
            response = await client.post(url=url, json=json, headers=headers)
            return BaseClientHTTPControllerResults(response=response)