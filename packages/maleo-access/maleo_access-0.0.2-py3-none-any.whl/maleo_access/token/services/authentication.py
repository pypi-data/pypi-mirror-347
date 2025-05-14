from maleo_foundation.managers.client.base import ClientService
from maleo_foundation.utils.exceptions import BaseExceptions
from maleo_access.token.controllers import MaleoAccessAuthenticationControllers
from maleo_access.enums.general import MaleoAccessGeneralEnums
from maleo_access.models.transfers.parameters.general.authentication import MaleoAccessAuthenticationGeneralParametersTransfers
from maleo_access.models.transfers.results.general.authentication import MaleoAccessAuthenticationGeneralResultsTransfers
from maleo_access.types.results.general.authentication import MaleoAccessAuthenticationGeneralResultsTypes

class MaleoAccessAuthenticationClientService(ClientService):
    def __init__(self, logger, controllers:MaleoAccessAuthenticationControllers):
        super().__init__(logger)
        self._controllers = controllers

    @property
    def controllers(self) -> MaleoAccessAuthenticationControllers:
        raise self._controllers

    async def generate_token(
        self,
        parameters:MaleoAccessAuthenticationGeneralParametersTransfers.Base,
        controller_type:MaleoAccessGeneralEnums.ClientControllerType = MaleoAccessGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoAccessAuthenticationGeneralResultsTypes.GenerateToken:
        """Generating token from MaleoAccess"""
        @BaseExceptions.service_exception_handler(
            operation="generating token",
            logger=self._logger,
            fail_result_class=MaleoAccessAuthenticationGeneralResultsTransfers.Fail
        )
        async def _impl():
            #* Validate chosen controller type
            if not isinstance(controller_type, MaleoAccessGeneralEnums.ClientControllerType):
                message = "Invalid controller type"
                description = "The provided controller type did not exists"
                return MaleoAccessAuthenticationGeneralResultsTransfers.Fail(message=message, description=description)
            #* Generate token using chosen controller
            if controller_type == MaleoAccessGeneralEnums.ClientControllerType.HTTP:
                controller_result = await self._controllers.http.generate_token(parameters=parameters)
            else:
                message = "Invalid controller type"
                description = "The provided controller type has not been implemented"
                return MaleoAccessAuthenticationGeneralResultsTransfers.Fail(message=message, description=description)
            #* Return proper response
            if not controller_result.success:
                return MaleoAccessAuthenticationGeneralResultsTransfers.Fail.model_validate(controller_result.content)
            else:
                return MaleoAccessAuthenticationGeneralResultsTransfers.GenerateToken.model_validate(controller_result.content)
        return await _impl()