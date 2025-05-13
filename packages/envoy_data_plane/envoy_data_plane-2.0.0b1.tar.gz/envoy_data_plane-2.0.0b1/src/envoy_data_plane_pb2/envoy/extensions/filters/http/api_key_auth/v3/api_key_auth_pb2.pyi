from xds.annotations.v3 import status_pb2 as _status_pb2
from udpa.annotations import sensitive_pb2 as _sensitive_pb2
from udpa.annotations import status_pb2 as _status_pb2_1
from validate import validate_pb2 as _validate_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ApiKeyAuth(_message.Message):
    __slots__ = ("credentials", "key_sources")
    CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    KEY_SOURCES_FIELD_NUMBER: _ClassVar[int]
    credentials: _containers.RepeatedCompositeFieldContainer[Credential]
    key_sources: _containers.RepeatedCompositeFieldContainer[KeySource]
    def __init__(self, credentials: _Optional[_Iterable[_Union[Credential, _Mapping]]] = ..., key_sources: _Optional[_Iterable[_Union[KeySource, _Mapping]]] = ...) -> None: ...

class ApiKeyAuthPerRoute(_message.Message):
    __slots__ = ("credentials", "key_sources", "allowed_clients")
    CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    KEY_SOURCES_FIELD_NUMBER: _ClassVar[int]
    ALLOWED_CLIENTS_FIELD_NUMBER: _ClassVar[int]
    credentials: _containers.RepeatedCompositeFieldContainer[Credential]
    key_sources: _containers.RepeatedCompositeFieldContainer[KeySource]
    allowed_clients: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, credentials: _Optional[_Iterable[_Union[Credential, _Mapping]]] = ..., key_sources: _Optional[_Iterable[_Union[KeySource, _Mapping]]] = ..., allowed_clients: _Optional[_Iterable[str]] = ...) -> None: ...

class Credential(_message.Message):
    __slots__ = ("key", "client")
    KEY_FIELD_NUMBER: _ClassVar[int]
    CLIENT_FIELD_NUMBER: _ClassVar[int]
    key: str
    client: str
    def __init__(self, key: _Optional[str] = ..., client: _Optional[str] = ...) -> None: ...

class KeySource(_message.Message):
    __slots__ = ("header", "query", "cookie")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    COOKIE_FIELD_NUMBER: _ClassVar[int]
    header: str
    query: str
    cookie: str
    def __init__(self, header: _Optional[str] = ..., query: _Optional[str] = ..., cookie: _Optional[str] = ...) -> None: ...
