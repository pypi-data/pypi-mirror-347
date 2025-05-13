from envoy.config.core.v3 import base_pb2 as _base_pb2
from envoy.type.v3 import percent_pb2 as _percent_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import wrappers_pb2 as _wrappers_pb2
from udpa.annotations import status_pb2 as _status_pb2
from validate import validate_pb2 as _validate_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LocalityLbConfig(_message.Message):
    __slots__ = ("zone_aware_lb_config", "locality_weighted_lb_config")
    class ZoneAwareLbConfig(_message.Message):
        __slots__ = ("routing_enabled", "min_cluster_size", "fail_traffic_on_panic", "force_locality_direct_routing")
        ROUTING_ENABLED_FIELD_NUMBER: _ClassVar[int]
        MIN_CLUSTER_SIZE_FIELD_NUMBER: _ClassVar[int]
        FAIL_TRAFFIC_ON_PANIC_FIELD_NUMBER: _ClassVar[int]
        FORCE_LOCALITY_DIRECT_ROUTING_FIELD_NUMBER: _ClassVar[int]
        routing_enabled: _percent_pb2.Percent
        min_cluster_size: _wrappers_pb2.UInt64Value
        fail_traffic_on_panic: bool
        force_locality_direct_routing: bool
        def __init__(self, routing_enabled: _Optional[_Union[_percent_pb2.Percent, _Mapping]] = ..., min_cluster_size: _Optional[_Union[_wrappers_pb2.UInt64Value, _Mapping]] = ..., fail_traffic_on_panic: bool = ..., force_locality_direct_routing: bool = ...) -> None: ...
    class LocalityWeightedLbConfig(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    ZONE_AWARE_LB_CONFIG_FIELD_NUMBER: _ClassVar[int]
    LOCALITY_WEIGHTED_LB_CONFIG_FIELD_NUMBER: _ClassVar[int]
    zone_aware_lb_config: LocalityLbConfig.ZoneAwareLbConfig
    locality_weighted_lb_config: LocalityLbConfig.LocalityWeightedLbConfig
    def __init__(self, zone_aware_lb_config: _Optional[_Union[LocalityLbConfig.ZoneAwareLbConfig, _Mapping]] = ..., locality_weighted_lb_config: _Optional[_Union[LocalityLbConfig.LocalityWeightedLbConfig, _Mapping]] = ...) -> None: ...

class SlowStartConfig(_message.Message):
    __slots__ = ("slow_start_window", "aggression", "min_weight_percent")
    SLOW_START_WINDOW_FIELD_NUMBER: _ClassVar[int]
    AGGRESSION_FIELD_NUMBER: _ClassVar[int]
    MIN_WEIGHT_PERCENT_FIELD_NUMBER: _ClassVar[int]
    slow_start_window: _duration_pb2.Duration
    aggression: _base_pb2.RuntimeDouble
    min_weight_percent: _percent_pb2.Percent
    def __init__(self, slow_start_window: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., aggression: _Optional[_Union[_base_pb2.RuntimeDouble, _Mapping]] = ..., min_weight_percent: _Optional[_Union[_percent_pb2.Percent, _Mapping]] = ...) -> None: ...

class ConsistentHashingLbConfig(_message.Message):
    __slots__ = ("use_hostname_for_hashing", "hash_balance_factor")
    USE_HOSTNAME_FOR_HASHING_FIELD_NUMBER: _ClassVar[int]
    HASH_BALANCE_FACTOR_FIELD_NUMBER: _ClassVar[int]
    use_hostname_for_hashing: bool
    hash_balance_factor: _wrappers_pb2.UInt32Value
    def __init__(self, use_hostname_for_hashing: bool = ..., hash_balance_factor: _Optional[_Union[_wrappers_pb2.UInt32Value, _Mapping]] = ...) -> None: ...
