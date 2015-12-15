#encoding:utf8
import struct

def pack_bytes(strs):
    return struct.pack("<is", len(strs), strs)

def pack_value(val):
    new = (val + 1) * 2
    return struct.pack("<H", new)

def pack_field(field):
    pass

def pack_protocols(protocols):
    pass

def pack_type(sproto_type):
    pass

def pack_group(group):
    if group.get("type", None):
        assert(group.get("protocol", None) == None)
        return "\0\0"
    types = group["type"]
    type_names = sorted(types.keys())
    packed_types = []
    for name in type_names:
        packed_types.append(pack_type(types[name]))
    type_str = pack_bytes("".join(pack_types))
    protocol_str = None
    if group.get("protocol", None):
        protocols = group["protocol"]
        sorted(protocols, lambda a, b:return a["tag"])
