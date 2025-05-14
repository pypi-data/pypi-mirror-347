from colav_protobuf_utils.deserialization import deserialize_protobuf
from colav_protobuf_utils.serialization import serialize_protobuf
from colav_protobuf_utils import ProtoType
from colav_protobuf.examples import unsafe_set

def test_mission_request_validation():
    deserialized_proto = deserialize_protobuf(
        serialize_protobuf(unsafe_set),
        ProtoType.UNSAFE_SET
    )

    assert deserialized_proto.mission_tag == unsafe_set.mission_tag, "mission_tag assertion failed"
    assert deserialized_proto.stamp.sec == unsafe_set.stamp.sec
    assert deserialized_proto.stamp.nanosec == unsafe_set.stamp.nanosec
    

# def test_mission_request_validation_edge_case_0_timestamp():
#     test_mission_request_update = mission_request
#     test_mission_request_update.stamp.sec = int(0)
#     test_mission_request_update.stamp.nanosec = int(0)
#     deserialized_proto = deserialize_protobuf(
#         serialize_protobuf(test_mission_request_update),
#         ProtoType.MISSION_REQUEST
#     )
#     assert deserialized_proto.stamp.sec == test_mission_request_update.stamp.sec
#     assert deserialized_proto.stamp.nanosec == test_mission_request_update.stamp.nanosec
