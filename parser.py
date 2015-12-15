#encoding:utf8
from constants import *

def absort_space(lexer_obj):
    token = lexer_obj.look_ahead()
    while token[0] == SPACE:
        lexer_obj.get_next_token()
        token = lexer_obj.look_ahead()

def expecting(lexer_obj, expect_token_type):
    token = lexer_obj.get_next_token()
    token_type = token[0]
    if token_type == expect_token_type:
        return token
    else:
        raise Exception("expecting {}, got {} instead".format(expect_token_type, token_type))

def optional(lexer_obj, expect_token_type):
    token = lexer_obj.look_ahead()
    token_type = token[0]
    if token_type == expect_token_type:
        return [lexer_obj.get_next_token()]
    return None

def field(lexer_obj):
    elements = {}
    word = expecting(lexer_obj, WORD)
    elements["name"] = word
    number = expecting(lexer_obj, NUMBER)
    elements["id"] = number
    expecting(lexer_obj, COLON)
    is_star = optional(lexer_obj, STAR)
    if is_star:
        elements["array"] = True
    word = expecting(lexer_obj, WORD)
    elements["type"] = word
    return elements

def struct(lexer_obj):
    element = []
    expecting(lexer_obj, LEFT_PARENTHESE)
    token = lexer_obj.look_ahead()
    while token[0] != RIGHT_PARENTHESE:
        if token[0] == POINT:
            new_sproto_type = sproto_type(lexer_obj)
            element.append(new_sproto_type)
            token = lexer_obj.look_ahead()
        else:
            new_field = field(lexer_obj)
            element.append(new_field)
            token = lexer_obj.look_ahead()
    expecting(lexer_obj, RIGHT_PARENTHESE)
    return element

def sproto_type(lexer_obj):
    expecting(lexer_obj, POINT)
    sproto_type_name = expecting(lexer_obj, WORD)
    element = struct(lexer_obj)
    return {"type":"sproto_type", "name":sproto_type_name, "fields":element}

def sproto_protocol(lexer_obj):
    result = {"type":"sproto_protocol"}
    protocol_name = expecting(lexer_obj, WORD)
    protocol_id = expecting(lexer_obj, NUMBER)
    expecting(lexer_obj, LEFT_PARENTHESE)
    token = lexer_obj.look_ahead()
    while token[0] != RIGHT_PARENTHESE:
        token = expecting(lexer_obj, WORD)
        if token[1] == "request" or token[1] == "response":
            next_token = lexer_obj.look_ahead()
            if next_token[0] == LEFT_PARENTHESE:
                packet = struct(lexer_obj)
            elif next_token[0] == WORD:
                packet = expecting(lexer_obj, WORD)
            else:
                raise Exception("expecting WORD or Struct, got {} instead".format(next_token))
            result[token[1]] = packet
        else:
            raise Exception("expecting request or response, got {} instead".format(next_token))
        token = lexer_obj.look_ahead()
    expecting(lexer_obj, RIGHT_PARENTHESE)
    result["name"] = protocol_name
    result["id"] = protocol_id
    return result

def sproto_group(lexer_obj):
    total = {"type":"group"}
    all_sproto_types = []
    protocols = []
    token = lexer_obj.look_ahead()
    while token[0] != EOF:
        if token[0] == SPACE:
            absort_space(lexer_obj)
        elif token[0] == POINT:
            element = sproto_type(lexer_obj)
            all_sproto_types.append(element)
        elif token[0] == WORD:
            protocol = sproto_protocol(lexer_obj)
            protocols.append(protocol)
        token = lexer_obj.look_ahead()
    total["type"] = all_sproto_types
    total["protocol"] = protocols
    return total

