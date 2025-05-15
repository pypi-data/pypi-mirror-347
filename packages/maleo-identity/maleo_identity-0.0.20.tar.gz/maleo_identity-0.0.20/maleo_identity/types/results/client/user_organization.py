from typing import Union
from maleo_identity.models.transfers.results.general.user_organization import MaleoIdentityUserOrganizationGeneralResultsTransfers

class MaleoIdentityUserOrganizationClientResultsTypes:
    GetMultiple = Union[
        MaleoIdentityUserOrganizationGeneralResultsTransfers.Fail,
        MaleoIdentityUserOrganizationGeneralResultsTransfers.NoData,
        MaleoIdentityUserOrganizationGeneralResultsTransfers.MultipleData
    ]

    GetSingle = Union[
        MaleoIdentityUserOrganizationGeneralResultsTransfers.Fail,
        MaleoIdentityUserOrganizationGeneralResultsTransfers.SingleData
    ]

    Create = Union[
        MaleoIdentityUserOrganizationGeneralResultsTransfers.Fail,
        MaleoIdentityUserOrganizationGeneralResultsTransfers.SingleData
    ]