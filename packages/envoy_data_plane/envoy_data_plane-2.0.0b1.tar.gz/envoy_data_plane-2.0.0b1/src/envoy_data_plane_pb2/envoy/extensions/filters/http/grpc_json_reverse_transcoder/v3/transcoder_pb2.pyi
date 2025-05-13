from google.protobuf import wrappers_pb2 as _wrappers_pb2
from udpa.annotations import status_pb2 as _status_pb2
from validate import validate_pb2 as _validate_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GrpcJsonReverseTranscoder(_message.Message):
    __slots__ = ("descriptor_path", "descriptor_binary", "max_request_body_size", "max_response_body_size", "api_version_header")
    DESCRIPTOR_PATH_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTOR_BINARY_FIELD_NUMBER: _ClassVar[int]
    MAX_REQUEST_BODY_SIZE_FIELD_NUMBER: _ClassVar[int]
    MAX_RESPONSE_BODY_SIZE_FIELD_NUMBER: _ClassVar[int]
    API_VERSION_HEADER_FIELD_NUMBER: _ClassVar[int]
    descriptor_path: str
    descriptor_binary: bytes
    max_request_body_size: _wrappers_pb2.UInt32Value
    max_response_body_size: _wrappers_pb2.UInt32Value
    api_version_header: str
    def __init__(self, descriptor_path: _Optional[str] = ..., descriptor_binary: _Optional[bytes] = ..., max_request_body_size: _Optional[_Union[_wrappers_pb2.UInt32Value, _Mapping]] = ..., max_response_body_size: _Optional[_Union[_wrappers_pb2.UInt32Value, _Mapping]] = ..., api_version_header: _Optional[str] = ...) -> None: ...
