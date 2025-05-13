from typing import Union
from maleo_metadata.models.transfers.results.general.gender import MaleoMetadataGenderGeneralResultsTransfers

class MaleoMetadataGenderClientResultsTypes:
    GetMultiple = Union[
        MaleoMetadataGenderGeneralResultsTransfers.Fail,
        MaleoMetadataGenderGeneralResultsTransfers.NoData,
        MaleoMetadataGenderGeneralResultsTransfers.MultipleData
    ]

    GetSingle = Union[
        MaleoMetadataGenderGeneralResultsTransfers.Fail,
        MaleoMetadataGenderGeneralResultsTransfers.SingleData
    ]