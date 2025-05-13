from envoy.config.core.v3 import base_pb2 as _base_pb2
from envoy.extensions.transport_sockets.tls.v3 import secret_pb2 as _secret_pb2
from xds.annotations.v3 import status_pb2 as _status_pb2
from udpa.annotations import status_pb2 as _status_pb2_1
from validate import validate_pb2 as _validate_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Config(_message.Message):
    __slots__ = ("unsafe_unencrypted_testing_mode", "server_id", "expected_server_id_length", "nonce_length_bytes", "encryption_parameters")
    UNSAFE_UNENCRYPTED_TESTING_MODE_FIELD_NUMBER: _ClassVar[int]
    SERVER_ID_FIELD_NUMBER: _ClassVar[int]
    EXPECTED_SERVER_ID_LENGTH_FIELD_NUMBER: _ClassVar[int]
    NONCE_LENGTH_BYTES_FIELD_NUMBER: _ClassVar[int]
    ENCRYPTION_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    unsafe_unencrypted_testing_mode: bool
    server_id: _base_pb2.DataSource
    expected_server_id_length: int
    nonce_length_bytes: int
    encryption_parameters: _secret_pb2.SdsSecretConfig
    def __init__(self, unsafe_unencrypted_testing_mode: bool = ..., server_id: _Optional[_Union[_base_pb2.DataSource, _Mapping]] = ..., expected_server_id_length: _Optional[int] = ..., nonce_length_bytes: _Optional[int] = ..., encryption_parameters: _Optional[_Union[_secret_pb2.SdsSecretConfig, _Mapping]] = ...) -> None: ...
