from typing import Union
from maleo_identity.models.transfers.results.general.user import MaleoIdentityUserGeneralResultsTransfers

class MaleoIdentityUserClientResultsTypes:
    GetMultiple = Union[
        MaleoIdentityUserGeneralResultsTransfers.Fail,
        MaleoIdentityUserGeneralResultsTransfers.NoData,
        MaleoIdentityUserGeneralResultsTransfers.MultipleData
    ]

    GetSingle = Union[
        MaleoIdentityUserGeneralResultsTransfers.Fail,
        MaleoIdentityUserGeneralResultsTransfers.SingleData
    ]

    CreateOrUpdate = Union[
        MaleoIdentityUserGeneralResultsTransfers.Fail,
        MaleoIdentityUserGeneralResultsTransfers.SingleData
    ]

    GetSinglePassword = Union[
        MaleoIdentityUserGeneralResultsTransfers.Fail,
        MaleoIdentityUserGeneralResultsTransfers.SinglePassword
    ]