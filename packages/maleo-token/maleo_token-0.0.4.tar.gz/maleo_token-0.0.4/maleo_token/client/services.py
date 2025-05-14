from maleo_foundation.managers.client.base import ClientService
from maleo_foundation.utils.exceptions import BaseExceptions
from maleo_token.client.controllers import MaleoTokenControllers
from maleo_token.enums import MaleoTokenEnums
from maleo_token.models.transfers.parameters import MaleoTokenParametersTransfers
from maleo_token.models.transfers.results import MaleoTokenResultsTransfers
from maleo_token.types.results import MaleoTokenResultsTypes

class MaleoTokenServices(ClientService):
    def __init__(self, logger, controllers:MaleoTokenControllers):
        super().__init__(logger)
        self._controllers = controllers

    @property
    def controllers(self) -> MaleoTokenControllers:
        raise self._controllers

    async def generate(
        self,
        parameters:MaleoTokenParametersTransfers.Base,
        controller_type:MaleoTokenEnums.ClientControllerType = MaleoTokenEnums.ClientControllerType.HTTP
    ) -> MaleoTokenResultsTypes.Generate:
        """Generating token from MaleoAccess"""
        @BaseExceptions.service_exception_handler(
            operation="generating token",
            logger=self._logger,
            fail_result_class=MaleoTokenResultsTransfers.Fail
        )
        async def _impl():
            #* Validate chosen controller type
            if not isinstance(controller_type, MaleoTokenEnums.ClientControllerType):
                message = "Invalid controller type"
                description = "The provided controller type did not exists"
                return MaleoTokenResultsTransfers.Fail(message=message, description=description)
            #* Generate token using chosen controller
            if controller_type == MaleoTokenEnums.ClientControllerType.HTTP:
                controller_result = await self._controllers.http.generate(parameters=parameters)
            else:
                message = "Invalid controller type"
                description = "The provided controller type has not been implemented"
                return MaleoTokenResultsTransfers.Fail(message=message, description=description)
            #* Return proper response
            if not controller_result.success:
                return MaleoTokenResultsTransfers.Fail.model_validate(controller_result.content)
            else:
                return MaleoTokenResultsTransfers.Generate.model_validate(controller_result.content)
        return await _impl()