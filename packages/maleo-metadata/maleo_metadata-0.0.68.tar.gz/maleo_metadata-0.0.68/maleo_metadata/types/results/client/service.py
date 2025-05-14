from typing import Union
from maleo_metadata.models.transfers.results.general.service import MaleoMetadataServiceGeneralResultsTransfers

class MaleoMetadataServiceClientResultsTypes:
    GetMultiple = Union[
        MaleoMetadataServiceGeneralResultsTransfers.Fail,
        MaleoMetadataServiceGeneralResultsTransfers.NoData,
        MaleoMetadataServiceGeneralResultsTransfers.MultipleData
    ]

    GetSingle = Union[
        MaleoMetadataServiceGeneralResultsTransfers.Fail,
        MaleoMetadataServiceGeneralResultsTransfers.SingleData
    ]