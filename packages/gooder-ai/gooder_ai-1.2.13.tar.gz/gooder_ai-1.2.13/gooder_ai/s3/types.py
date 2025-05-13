from typing import TypedDict, Literal, Union
from botocore.client import BaseClient
from pandas import DataFrame
from gooder_ai.auth.types import AuthenticateReturn


class UploadParams(TypedDict):
    s3_client: BaseClient  # Ref: https://stackoverflow.com/a/68006865
    identity_id: str
    file_name: str
    mode: Literal["public", "protected", "private"]
    bucket_name: str
    data: Union[DataFrame, dict]


class UploadFileParams(TypedDict):
    credentials: AuthenticateReturn

    data: DataFrame
    file_name: str
    config: dict
    mode: Literal["public", "protected", "private"]
    bucket_name: str

    upload_data_to_gooder: bool
    upload_config_to_gooder: bool
