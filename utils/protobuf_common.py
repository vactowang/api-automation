
from google.protobuf import json_format as _json_format
from data.sdk_proto import sdkerrorbatch_pb2
from data.configExtension_proto import configExtension_pb2


def generate_pb2_message(pb_message=sdkerrorbatch_pb2.SDKErrorBatch(), json_message=None):

    pb_message = pb_message
    pb_message = _json_format.Parse(json_message, pb_message, ignore_unknown_fields=False)
    return pb_message


def generate_pb2_metrics_message(pb_message=sdkerrorbatch_pb2.MetricBatch(), json_message=None):

    pb_message = pb_message
    pb_message = _json_format.Parse(json_message, pb_message, ignore_unknown_fields=False)
    return pb_message


def pb_serialize_to_string(pb_message):
    pb_serialize_string = pb_message.SerializeToString()
    return pb_serialize_string


# def pb_prase_from_str(pb_message=configExtension_pb2.ConfigExtension(), data=None):
#     # pb_message.ParseFromString(pb_serialize_string)
#     # pb_message_json = _json_format.MessageToJson(pb_message, preserving_proto_field_name=True, sort_keys=True, indent=4)
#     pb_message.ParseFromString(data)
#     pb_message_json = _json_format.MessageToJson(pb_message, preserving_proto_field_name=True, sort_keys=True, indent=4)
#     return pb_message_json
#
#
# if __name__ == '__main__':
#     print(pb_prase_from_str(data=b'Cj4SPAojUmVhbF9UaW1lX0Fkc18yMDIyX0RlY19BbmRyb2lkXzEyMDcSE1JlYWxUaW1lQWRzX05vQ2FjaGUYARIONDUuMTE3LjEwMC4xNTMiACrgAQoHYW5kcm9pZBIDNy4zGgdTYW1zdW5nIghTUEgtTDcyMCqRAU1vemlsbGEvNS4wIChMaW51eDsgQW5kcm9pZCA0LjQuMjsgU1BILUw3MjAgQnVpbGQvS09UNDlIKSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBWZXJzaW9uLzQuMCBDaHJvbWUvMzAuMC4wLjAgTW9iaWxlIFNhZmFyaS81MzcuMzYwgAw4gBBaAGIGCgRXSUZJagYKBFdJRklyCQkAAAAAAADwP3oGCICAmIcPMgA='))
