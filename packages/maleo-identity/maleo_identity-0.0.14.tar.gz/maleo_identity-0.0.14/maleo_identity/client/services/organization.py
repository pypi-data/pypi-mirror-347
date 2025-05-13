from maleo_foundation.managers.client.base import ClientService
from maleo_foundation.utils.exceptions import BaseExceptions
from maleo_identity.client.controllers import MaleoIdentityOrganizationControllers
from maleo_identity.enums.general import MaleoIdentityGeneralEnums
from maleo_identity.models.transfers.parameters.general.organization import MaleoIdentityOrganizationGeneralParametersTransfers
from maleo_identity.models.transfers.parameters.general.user_organization import MaleoIdentityUserOrganizationGeneralParametersTransfers
from maleo_identity.models.transfers.parameters.client.organization import MaleoIdentityOrganizationClientParametersTransfers
from maleo_identity.models.transfers.parameters.client.user_organization import MaleoIdentityUserOrganizationClientParametersTransfers
from maleo_identity.models.transfers.results.general.organization import MaleoIdentityOrganizationGeneralResultsTransfers
from maleo_identity.models.transfers.results.general.user_organization import MaleoIdentityUserOrganizationGeneralResultsTransfers
from maleo_identity.types.results.client.organization import MaleoIdentityOrganizationClientResultsTypes
from maleo_identity.types.results.client.user_organization import MaleoIdentityUserOrganizationClientResultsTypes

class MaleoIdentityOrganizationClientService(ClientService):
    def __init__(self, logger, controllers:MaleoIdentityOrganizationControllers):
        super().__init__(logger)
        self._controllers = controllers

    @property
    def controllers(self) -> MaleoIdentityOrganizationControllers:
        raise self._controllers

    async def get_organizations(
        self,
        parameters:MaleoIdentityOrganizationClientParametersTransfers.GetMultiple,
        controller_type:MaleoIdentityGeneralEnums.ClientControllerType = MaleoIdentityGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoIdentityOrganizationClientResultsTypes.GetMultiple:
        """Retrieve organizations from MaleoIdentity"""
        @BaseExceptions.service_exception_handler(
            operation="retrieving organizations",
            logger=self._logger,
            fail_result_class=MaleoIdentityOrganizationGeneralResultsTransfers.Fail
        )
        async def _impl():
            #* Validate chosen controller type
            if not isinstance(controller_type, MaleoIdentityGeneralEnums.ClientControllerType):
                message = "Invalid controller type"
                description = "The provided controller type did not exists"
                return MaleoIdentityOrganizationGeneralResultsTransfers.Fail(message=message, description=description)
            #* Retrieve organizations using chosen controller
            if controller_type == MaleoIdentityGeneralEnums.ClientControllerType.HTTP:
                controller_result = await self._controllers.http.get_organizations(parameters=parameters)
            else:
                message = "Invalid controller type"
                description = "The provided controller type has not been implemented"
                return MaleoIdentityOrganizationGeneralResultsTransfers.Fail(message=message, description=description)
            #* Return proper response
            if not controller_result.success:
                return MaleoIdentityOrganizationGeneralResultsTransfers.Fail.model_validate(controller_result.content)
            else:
                if controller_result.content["data"] is None:
                    return MaleoIdentityOrganizationGeneralResultsTransfers.NoData.model_validate(controller_result.content)
                else:
                    return MaleoIdentityOrganizationGeneralResultsTransfers.MultipleData.model_validate(controller_result.content)
        return await _impl()

    async def get_organization(
        self,
        parameters:MaleoIdentityOrganizationGeneralParametersTransfers.GetSingle,
        controller_type:MaleoIdentityGeneralEnums.ClientControllerType = MaleoIdentityGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoIdentityOrganizationClientResultsTypes.GetSingle:
        """Retrieve organization from MaleoIdentity"""
        @BaseExceptions.service_exception_handler(
            operation="retrieving organization",
            logger=self._logger,
            fail_result_class=MaleoIdentityOrganizationGeneralResultsTransfers.Fail
        )
        async def _impl():
            #* Validate chosen controller type
            if not isinstance(controller_type, MaleoIdentityGeneralEnums.ClientControllerType):
                message = "Invalid controller type"
                description = "The provided controller type did not exists"
                return MaleoIdentityOrganizationGeneralResultsTransfers.Fail(message=message, description=description)
            #* Retrieve organization using chosen controller
            if controller_type == MaleoIdentityGeneralEnums.ClientControllerType.HTTP:
                controller_result = await self._controllers.http.get_organization(parameters=parameters)
            else:
                message = "Invalid controller type"
                description = "The provided controller type has not been implemented"
                return MaleoIdentityOrganizationGeneralResultsTransfers.Fail(message=message, description=description)
            #* Return proper response
            if not controller_result.success:
                return MaleoIdentityOrganizationGeneralResultsTransfers.Fail.model_validate(controller_result.content)
            else:
                return MaleoIdentityOrganizationGeneralResultsTransfers.SingleData.model_validate(controller_result.content)
        return await _impl()

    async def create(
        self,
        parameters:MaleoIdentityOrganizationGeneralParametersTransfers.Create,
        controller_type:MaleoIdentityGeneralEnums.ClientControllerType = MaleoIdentityGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoIdentityOrganizationClientResultsTypes.CreateOrUpdate:
        """Create a new organization in MaleoIdentity"""
        @BaseExceptions.service_exception_handler(
            operation="creating a new organization",
            logger=self._logger,
            fail_result_class=MaleoIdentityOrganizationGeneralResultsTransfers.Fail
        )
        async def _impl():
            #* Validate chosen controller type
            if not isinstance(controller_type, MaleoIdentityGeneralEnums.ClientControllerType):
                message = "Invalid controller type"
                description = "The provided controller type did not exists"
                return MaleoIdentityOrganizationGeneralResultsTransfers.Fail(message=message, description=description)
            #* Create a new organization using chosen controller
            if controller_type == MaleoIdentityGeneralEnums.ClientControllerType.HTTP:
                controller_result = await self._controllers.http.create(parameters=parameters)
            else:
                message = "Invalid controller type"
                description = "The provided controller type has not been implemented"
                return MaleoIdentityOrganizationGeneralResultsTransfers.Fail(message=message, description=description)
            #* Return proper response
            if not controller_result.success:
                return MaleoIdentityOrganizationGeneralResultsTransfers.Fail.model_validate(controller_result.content)
            else:
                return MaleoIdentityOrganizationGeneralResultsTransfers.SingleData.model_validate(controller_result.content)
        return await _impl()

    async def update(
        self,
        parameters:MaleoIdentityOrganizationGeneralParametersTransfers.Update,
        controller_type:MaleoIdentityGeneralEnums.ClientControllerType = MaleoIdentityGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoIdentityOrganizationClientResultsTypes.CreateOrUpdate:
        """Update organization's data in MaleoIdentity"""
        @BaseExceptions.service_exception_handler(
            operation="updating organization's data",
            logger=self._logger,
            fail_result_class=MaleoIdentityOrganizationGeneralResultsTransfers.Fail
        )
        async def _impl():
            #* Validate chosen controller type
            if not isinstance(controller_type, MaleoIdentityGeneralEnums.ClientControllerType):
                message = "Invalid controller type"
                description = "The provided controller type did not exists"
                return MaleoIdentityOrganizationGeneralResultsTransfers.Fail(message=message, description=description)
            #* Update organization's data using chosen controller
            if controller_type == MaleoIdentityGeneralEnums.ClientControllerType.HTTP:
                controller_result = await self._controllers.http.update(parameters=parameters)
            else:
                message = "Invalid controller type"
                description = "The provided controller type has not been implemented"
                return MaleoIdentityOrganizationGeneralResultsTransfers.Fail(message=message, description=description)
            #* Return proper response
            if not controller_result.success:
                return MaleoIdentityOrganizationGeneralResultsTransfers.Fail.model_validate(controller_result.content)
            else:
                return MaleoIdentityOrganizationGeneralResultsTransfers.SingleData.model_validate(controller_result.content)
        return await _impl()

    async def get_organization_users(
        self,
        parameters:MaleoIdentityUserOrganizationClientParametersTransfers.GetMultipleFromOrganization,
        controller_type:MaleoIdentityGeneralEnums.ClientControllerType = MaleoIdentityGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoIdentityUserOrganizationClientResultsTypes.GetMultiple:
        """Retrieve organization's users from MaleoIdentity"""
        @BaseExceptions.service_exception_handler(
            operation="retrieving organization's users",
            logger=self._logger,
            fail_result_class=MaleoIdentityUserOrganizationGeneralResultsTransfers.Fail
        )
        async def _impl():
            #* Validate chosen controller type
            if not isinstance(controller_type, MaleoIdentityGeneralEnums.ClientControllerType):
                message = "Invalid controller type"
                description = "The provided controller type did not exists"
                return MaleoIdentityUserOrganizationGeneralResultsTransfers.Fail(message=message, description=description)
            #* Update organization's data using chosen controller
            if controller_type == MaleoIdentityGeneralEnums.ClientControllerType.HTTP:
                controller_result = await self._controllers.http.get_organization_users(parameters=parameters)
            else:
                message = "Invalid controller type"
                description = "The provided controller type has not been implemented"
                return MaleoIdentityUserOrganizationGeneralResultsTransfers.Fail(message=message, description=description)
            #* Return proper response
            if not controller_result.success:
                return MaleoIdentityUserOrganizationGeneralResultsTransfers.Fail.model_validate(controller_result.content)
            else:
                if controller_result.content["data"] is None:
                    return MaleoIdentityUserOrganizationGeneralResultsTransfers.NoData.model_validate(controller_result.content)
                else:
                    return MaleoIdentityUserOrganizationGeneralResultsTransfers.MultipleData.model_validate(controller_result.content)
        return await _impl()

    async def get_organization_user(
        self,
        parameters:MaleoIdentityUserOrganizationGeneralParametersTransfers.GetSingle,
        controller_type:MaleoIdentityGeneralEnums.ClientControllerType = MaleoIdentityGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoIdentityUserOrganizationClientResultsTypes.GetSingle:
        """Retrieve organization's user from MaleoIdentity"""
        @BaseExceptions.service_exception_handler(
            operation="retrieving organization's user",
            logger=self._logger,
            fail_result_class=MaleoIdentityUserOrganizationGeneralResultsTransfers.Fail
        )
        async def _impl():
            #* Validate chosen controller type
            if not isinstance(controller_type, MaleoIdentityGeneralEnums.ClientControllerType):
                message = "Invalid controller type"
                description = "The provided controller type did not exists"
                return MaleoIdentityUserOrganizationGeneralResultsTransfers.Fail(message=message, description=description)
            #* Update organization's data using chosen controller
            if controller_type == MaleoIdentityGeneralEnums.ClientControllerType.HTTP:
                controller_result = await self._controllers.http.get_organization_user(parameters=parameters)
            else:
                message = "Invalid controller type"
                description = "The provided controller type has not been implemented"
                return MaleoIdentityUserOrganizationGeneralResultsTransfers.Fail(message=message, description=description)
            #* Return proper response
            if not controller_result.success:
                return MaleoIdentityUserOrganizationGeneralResultsTransfers.Fail.model_validate(controller_result.content)
            else:
                return MaleoIdentityUserOrganizationGeneralResultsTransfers.SingleData.model_validate(controller_result.content)
        return await _impl()