from fastapi import status
from maleo_foundation.managers.client.base import ClientService
from maleo_foundation.utils.exceptions import BaseExceptions
from maleo_identity.client.controllers import MaleoIdentityUserControllers
from maleo_identity.enums.general import MaleoIdentityGeneralEnums
from maleo_identity.models.transfers.parameters.general.user import MaleoIdentityUserGeneralParametersTransfers
from maleo_identity.models.transfers.parameters.general.user_organization import MaleoIdentityUserOrganizationGeneralParametersTransfers
from maleo_identity.models.transfers.parameters.general.user_system_role import MaleoIdentityUserSystemRoleGeneralParametersTransfers
from maleo_identity.models.transfers.parameters.client.user import MaleoIdentityUserClientParametersTransfers
from maleo_identity.models.transfers.parameters.client.user_organization import MaleoIdentityUserOrganizationClientParametersTransfers
from maleo_identity.models.transfers.parameters.client.user_system_role import MaleoIdentityUserSystemRoleClientParametersTransfers
from maleo_identity.models.transfers.results.general.user import MaleoIdentityUserGeneralResultsTransfers
from maleo_identity.models.transfers.results.general.user_organization import MaleoIdentityUserOrganizationGeneralResultsTransfers
from maleo_identity.models.transfers.results.general.user_system_role import MaleoIdentityUserSystemRoleGeneralResultsTransfers
from maleo_identity.types.results.client.user import MaleoIdentityUserClientResultsTypes
from maleo_identity.types.results.client.user_organization import MaleoIdentityUserOrganizationClientResultsTypes
from maleo_identity.types.results.client.user_system_role import MaleoIdentityUserSystemRoleClientResultsTypes

class MaleoIdentityUserClientService(ClientService):
    def __init__(self, logger, controllers:MaleoIdentityUserControllers):
        super().__init__(logger)
        self._controllers = controllers

    @property
    def controllers(self) -> MaleoIdentityUserControllers:
        raise self._controllers

    async def get_users(
        self,
        parameters:MaleoIdentityUserClientParametersTransfers.GetMultiple,
        controller_type:MaleoIdentityGeneralEnums.ClientControllerType = MaleoIdentityGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoIdentityUserClientResultsTypes.GetMultiple:
        """Retrieve users from MaleoIdentity"""
        @BaseExceptions.service_exception_handler(
            operation="retrieving users",
            logger=self._logger,
            fail_result_class=MaleoIdentityUserGeneralResultsTransfers.Fail
        )
        async def _impl():
            #* Validate chosen controller type
            if not isinstance(controller_type, MaleoIdentityGeneralEnums.ClientControllerType):
                message = "Invalid controller type"
                description = "The provided controller type did not exists"
                return MaleoIdentityUserGeneralResultsTransfers.Fail(message=message, description=description)
            #* Retrieve users using chosen controller
            if controller_type == MaleoIdentityGeneralEnums.ClientControllerType.HTTP:
                controller_result = await self._controllers.http.get_users(parameters=parameters)
            else:
                message = "Invalid controller type"
                description = "The provided controller type has not been implemented"
                return MaleoIdentityUserGeneralResultsTransfers.Fail(message=message, description=description)
            #* Return proper response
            if not controller_result.success:
                return MaleoIdentityUserGeneralResultsTransfers.Fail.model_validate(controller_result.content)
            else:
                if controller_result.content["data"] is None:
                    return MaleoIdentityUserGeneralResultsTransfers.NoData.model_validate(controller_result.content)
                else:
                    return MaleoIdentityUserGeneralResultsTransfers.MultipleData.model_validate(controller_result.content)
        return await _impl()

    async def get_user(
        self,
        parameters:MaleoIdentityUserGeneralParametersTransfers.GetSingle,
        controller_type:MaleoIdentityGeneralEnums.ClientControllerType = MaleoIdentityGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoIdentityUserClientResultsTypes.GetSingle:
        """Retrieve user from MaleoIdentity"""
        @BaseExceptions.service_exception_handler(
            operation="retrieving user",
            logger=self._logger,
            fail_result_class=MaleoIdentityUserGeneralResultsTransfers.Fail
        )
        async def _impl():
            #* Validate chosen controller type
            if not isinstance(controller_type, MaleoIdentityGeneralEnums.ClientControllerType):
                message = "Invalid controller type"
                description = "The provided controller type did not exists"
                return MaleoIdentityUserGeneralResultsTransfers.Fail(message=message, description=description)
            #* Retrieve user using chosen controller
            if controller_type == MaleoIdentityGeneralEnums.ClientControllerType.HTTP:
                controller_result = await self._controllers.http.get_user(parameters=parameters)
            else:
                message = "Invalid controller type"
                description = "The provided controller type has not been implemented"
                return MaleoIdentityUserGeneralResultsTransfers.Fail(message=message, description=description)
            #* Return proper response
            if not controller_result.success:
                return MaleoIdentityUserGeneralResultsTransfers.Fail.model_validate(controller_result.content)
            else:
                return MaleoIdentityUserGeneralResultsTransfers.SingleData.model_validate(controller_result.content)
        return await _impl()

    async def create(
        self,
        parameters:MaleoIdentityUserGeneralParametersTransfers.Create,
        controller_type:MaleoIdentityGeneralEnums.ClientControllerType = MaleoIdentityGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoIdentityUserClientResultsTypes.CreateOrUpdate:
        """Create a new user in MaleoIdentity"""
        @BaseExceptions.service_exception_handler(
            operation="creating a new user",
            logger=self._logger,
            fail_result_class=MaleoIdentityUserGeneralResultsTransfers.Fail
        )
        async def _impl():
            #* Validate chosen controller type
            if not isinstance(controller_type, MaleoIdentityGeneralEnums.ClientControllerType):
                message = "Invalid controller type"
                description = "The provided controller type did not exists"
                return MaleoIdentityUserGeneralResultsTransfers.Fail(message=message, description=description)
            #* Create a new user using chosen controller
            if controller_type == MaleoIdentityGeneralEnums.ClientControllerType.HTTP:
                controller_result = await self._controllers.http.create(parameters=parameters)
            else:
                message = "Invalid controller type"
                description = "The provided controller type has not been implemented"
                return MaleoIdentityUserGeneralResultsTransfers.Fail(message=message, description=description)
            #* Return proper response
            if not controller_result.success:
                return MaleoIdentityUserGeneralResultsTransfers.Fail.model_validate(controller_result.content)
            else:
                return MaleoIdentityUserGeneralResultsTransfers.SingleData.model_validate(controller_result.content)
        return await _impl()

    async def update(
        self,
        parameters:MaleoIdentityUserGeneralParametersTransfers.Update,
        controller_type:MaleoIdentityGeneralEnums.ClientControllerType = MaleoIdentityGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoIdentityUserClientResultsTypes.CreateOrUpdate:
        """Update user's data in MaleoIdentity"""
        @BaseExceptions.service_exception_handler(
            operation="updating user's data",
            logger=self._logger,
            fail_result_class=MaleoIdentityUserGeneralResultsTransfers.Fail
        )
        async def _impl():
            #* Validate chosen controller type
            if not isinstance(controller_type, MaleoIdentityGeneralEnums.ClientControllerType):
                message = "Invalid controller type"
                description = "The provided controller type did not exists"
                return MaleoIdentityUserGeneralResultsTransfers.Fail(message=message, description=description)
            #* Update user's data using chosen controller
            if controller_type == MaleoIdentityGeneralEnums.ClientControllerType.HTTP:
                controller_result = await self._controllers.http.update(parameters=parameters)
            else:
                message = "Invalid controller type"
                description = "The provided controller type has not been implemented"
                return MaleoIdentityUserGeneralResultsTransfers.Fail(message=message, description=description)
            #* Return proper response
            if not controller_result.success:
                return MaleoIdentityUserGeneralResultsTransfers.Fail.model_validate(controller_result.content)
            else:
                return MaleoIdentityUserGeneralResultsTransfers.SingleData.model_validate(controller_result.content)
        return await _impl()

    async def get_password(
        self,
        parameters:MaleoIdentityUserGeneralParametersTransfers.GetSinglePassword,
        controller_type:MaleoIdentityGeneralEnums.ClientControllerType = MaleoIdentityGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoIdentityUserClientResultsTypes.GetSinglePassword:
        """Retrieve user's password from MaleoIdentity"""
        @BaseExceptions.service_exception_handler(
            operation="retrieving user's password",
            logger=self._logger,
            fail_result_class=MaleoIdentityUserGeneralResultsTransfers.Fail
        )
        async def _impl():
            #* Validate chosen controller type
            if not isinstance(controller_type, MaleoIdentityGeneralEnums.ClientControllerType):
                message = "Invalid controller type"
                description = "The provided controller type did not exists"
                return MaleoIdentityUserGeneralResultsTransfers.Fail(message=message, description=description)
            #* Retrieve user using chosen controller
            if controller_type == MaleoIdentityGeneralEnums.ClientControllerType.HTTP:
                controller_result = await self._controllers.http.get_password(parameters=parameters)
            else:
                message = "Invalid controller type"
                description = "The provided controller type has not been implemented"
                return MaleoIdentityUserGeneralResultsTransfers.Fail(message=message, description=description)
            #* Return proper response
            if not controller_result.success:
                return MaleoIdentityUserGeneralResultsTransfers.Fail.model_validate(controller_result.content)
            else:
                return MaleoIdentityUserGeneralResultsTransfers.SinglePassword.model_validate(controller_result.content)
        return await _impl()

    async def get_user_organizations(
        self,
        parameters:MaleoIdentityUserOrganizationClientParametersTransfers.GetMultipleFromUser,
        controller_type:MaleoIdentityGeneralEnums.ClientControllerType = MaleoIdentityGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoIdentityUserOrganizationClientResultsTypes.GetMultiple:
        """Retrieve user's organizations from MaleoIdentity"""
        @BaseExceptions.service_exception_handler(
            operation="retrieving user's organizations",
            logger=self._logger,
            fail_result_class=MaleoIdentityUserOrganizationGeneralResultsTransfers.Fail
        )
        async def _impl():
            #* Validate chosen controller type
            if not isinstance(controller_type, MaleoIdentityGeneralEnums.ClientControllerType):
                message = "Invalid controller type"
                description = "The provided controller type did not exists"
                return MaleoIdentityUserOrganizationGeneralResultsTransfers.Fail(message=message, description=description)
            #* Retrieve users using chosen controller
            if controller_type == MaleoIdentityGeneralEnums.ClientControllerType.HTTP:
                controller_result = await self._controllers.http.get_user_organizations(parameters=parameters)
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

    async def get_user_organization(
        self,
        parameters:MaleoIdentityUserOrganizationGeneralParametersTransfers.GetSingle,
        controller_type:MaleoIdentityGeneralEnums.ClientControllerType = MaleoIdentityGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoIdentityUserOrganizationClientResultsTypes.GetSingle:
        """Retrieve user's organization from MaleoIdentity"""
        @BaseExceptions.service_exception_handler(
            operation="retrieving user's organization",
            logger=self._logger,
            fail_result_class=MaleoIdentityUserOrganizationGeneralResultsTransfers.Fail
        )
        async def _impl():
            #* Validate chosen controller type
            if not isinstance(controller_type, MaleoIdentityGeneralEnums.ClientControllerType):
                message = "Invalid controller type"
                description = "The provided controller type did not exists"
                return MaleoIdentityUserOrganizationGeneralResultsTransfers.Fail(message=message, description=description)
            #* Retrieve user using chosen controller
            if controller_type == MaleoIdentityGeneralEnums.ClientControllerType.HTTP:
                controller_result = await self._controllers.http.get_user_organization(parameters=parameters)
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

    async def get_user_system_roles(
        self,
        parameters:MaleoIdentityUserSystemRoleClientParametersTransfers.GetMultipleFromUser,
        controller_type:MaleoIdentityGeneralEnums.ClientControllerType = MaleoIdentityGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoIdentityUserSystemRoleClientResultsTypes.GetMultiple:
        """Retrieve user's system roles from MaleoIdentity"""
        @BaseExceptions.service_exception_handler(
            operation="retrieving user's system roles",
            logger=self._logger,
            fail_result_class=MaleoIdentityUserSystemRoleGeneralResultsTransfers.Fail
        )
        async def _impl():
            #* Validate chosen controller type
            if not isinstance(controller_type, MaleoIdentityGeneralEnums.ClientControllerType):
                message = "Invalid controller type"
                description = "The provided controller type did not exists"
                return MaleoIdentityUserSystemRoleGeneralResultsTransfers.Fail(message=message, description=description)
            #* Retrieve users using chosen controller
            if controller_type == MaleoIdentityGeneralEnums.ClientControllerType.HTTP:
                controller_result = await self._controllers.http.get_user_system_roles(parameters=parameters)
            else:
                message = "Invalid controller type"
                description = "The provided controller type has not been implemented"
                return MaleoIdentityUserSystemRoleGeneralResultsTransfers.Fail(message=message, description=description)
            #* Return proper response
            if not controller_result.success:
                return MaleoIdentityUserSystemRoleGeneralResultsTransfers.Fail.model_validate(controller_result.content)
            else:
                if controller_result.content["data"] is None:
                    return MaleoIdentityUserSystemRoleGeneralResultsTransfers.NoData.model_validate(controller_result.content)
                else:
                    return MaleoIdentityUserSystemRoleGeneralResultsTransfers.MultipleData.model_validate(controller_result.content)
        return await _impl()

    async def get_user_system_role(
        self,
        parameters:MaleoIdentityUserSystemRoleGeneralParametersTransfers.GetSingle,
        controller_type:MaleoIdentityGeneralEnums.ClientControllerType = MaleoIdentityGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoIdentityUserSystemRoleClientResultsTypes.GetSingle:
        """Retrieve user's system role from MaleoIdentity"""
        @BaseExceptions.service_exception_handler(
            operation="retrieving user's system role",
            logger=self._logger,
            fail_result_class=MaleoIdentityUserSystemRoleGeneralResultsTransfers.Fail
        )
        async def _impl():
            #* Validate chosen controller type
            if not isinstance(controller_type, MaleoIdentityGeneralEnums.ClientControllerType):
                message = "Invalid controller type"
                description = "The provided controller type did not exists"
                return MaleoIdentityUserSystemRoleGeneralResultsTransfers.Fail(message=message, description=description)
            #* Retrieve user using chosen controller
            if controller_type == MaleoIdentityGeneralEnums.ClientControllerType.HTTP:
                controller_result = await self._controllers.http.get_user_system_role(parameters=parameters)
            else:
                message = "Invalid controller type"
                description = "The provided controller type has not been implemented"
                return MaleoIdentityUserSystemRoleGeneralResultsTransfers.Fail(message=message, description=description)
            #* Return proper response
            if not controller_result.success:
                return MaleoIdentityUserSystemRoleGeneralResultsTransfers.Fail.model_validate(controller_result.content)
            else:
                return MaleoIdentityUserSystemRoleGeneralResultsTransfers.SingleData.model_validate(controller_result.content)
        return await _impl()