from typing import Union
from maleo_metadata.models.transfers.results.general.user_type import MaleoMetadataUserTypeGeneralResultsTransfers

class MaleoMetadataUserTypeClientResultsTypes:
    GetMultiple = Union[
        MaleoMetadataUserTypeGeneralResultsTransfers.Fail,
        MaleoMetadataUserTypeGeneralResultsTransfers.NoData,
        MaleoMetadataUserTypeGeneralResultsTransfers.MultipleData
    ]

    GetSingle = Union[
        MaleoMetadataUserTypeGeneralResultsTransfers.Fail,
        MaleoMetadataUserTypeGeneralResultsTransfers.SingleData
    ]