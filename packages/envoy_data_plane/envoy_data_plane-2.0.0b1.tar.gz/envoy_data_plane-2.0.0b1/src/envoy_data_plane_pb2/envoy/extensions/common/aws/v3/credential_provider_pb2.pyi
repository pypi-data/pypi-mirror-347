from envoy.config.core.v3 import base_pb2 as _base_pb2
from udpa.annotations import sensitive_pb2 as _sensitive_pb2
from udpa.annotations import status_pb2 as _status_pb2
from validate import validate_pb2 as _validate_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AwsCredentialProvider(_message.Message):
    __slots__ = ("assume_role_with_web_identity_provider", "inline_credential", "credentials_file_provider", "custom_credential_provider_chain")
    ASSUME_ROLE_WITH_WEB_IDENTITY_PROVIDER_FIELD_NUMBER: _ClassVar[int]
    INLINE_CREDENTIAL_FIELD_NUMBER: _ClassVar[int]
    CREDENTIALS_FILE_PROVIDER_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_CREDENTIAL_PROVIDER_CHAIN_FIELD_NUMBER: _ClassVar[int]
    assume_role_with_web_identity_provider: AssumeRoleWithWebIdentityCredentialProvider
    inline_credential: InlineCredentialProvider
    credentials_file_provider: CredentialsFileCredentialProvider
    custom_credential_provider_chain: bool
    def __init__(self, assume_role_with_web_identity_provider: _Optional[_Union[AssumeRoleWithWebIdentityCredentialProvider, _Mapping]] = ..., inline_credential: _Optional[_Union[InlineCredentialProvider, _Mapping]] = ..., credentials_file_provider: _Optional[_Union[CredentialsFileCredentialProvider, _Mapping]] = ..., custom_credential_provider_chain: bool = ...) -> None: ...

class InlineCredentialProvider(_message.Message):
    __slots__ = ("access_key_id", "secret_access_key", "session_token")
    ACCESS_KEY_ID_FIELD_NUMBER: _ClassVar[int]
    SECRET_ACCESS_KEY_FIELD_NUMBER: _ClassVar[int]
    SESSION_TOKEN_FIELD_NUMBER: _ClassVar[int]
    access_key_id: str
    secret_access_key: str
    session_token: str
    def __init__(self, access_key_id: _Optional[str] = ..., secret_access_key: _Optional[str] = ..., session_token: _Optional[str] = ...) -> None: ...

class AssumeRoleWithWebIdentityCredentialProvider(_message.Message):
    __slots__ = ("web_identity_token_data_source", "role_arn", "role_session_name")
    WEB_IDENTITY_TOKEN_DATA_SOURCE_FIELD_NUMBER: _ClassVar[int]
    ROLE_ARN_FIELD_NUMBER: _ClassVar[int]
    ROLE_SESSION_NAME_FIELD_NUMBER: _ClassVar[int]
    web_identity_token_data_source: _base_pb2.DataSource
    role_arn: str
    role_session_name: str
    def __init__(self, web_identity_token_data_source: _Optional[_Union[_base_pb2.DataSource, _Mapping]] = ..., role_arn: _Optional[str] = ..., role_session_name: _Optional[str] = ...) -> None: ...

class CredentialsFileCredentialProvider(_message.Message):
    __slots__ = ("credentials_data_source", "profile")
    CREDENTIALS_DATA_SOURCE_FIELD_NUMBER: _ClassVar[int]
    PROFILE_FIELD_NUMBER: _ClassVar[int]
    credentials_data_source: _base_pb2.DataSource
    profile: str
    def __init__(self, credentials_data_source: _Optional[_Union[_base_pb2.DataSource, _Mapping]] = ..., profile: _Optional[str] = ...) -> None: ...
