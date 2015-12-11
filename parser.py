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
    optional(lexer_obj, SPACE)
    word = expecting(lexer_obj, WORD)
    elements["attribute_name"] = word
    optional(lexer_obj, SPACE)
    number = expecting(lexer_obj, NUMBER)
    elements["attribute_order"] = number
    optional(lexer_obj, SPACE)
    expecting(lexer_obj, COLON)
    optional(lexer_obj, SPACE)
    is_star = optional(lexer_obj, STAR)
    if is_star:
        elements["is_array"] = True
    word = expecting(lexer_obj, WORD)
    elements["attribute_type"] = word
    return elements

def struct(lexer_obj):
    element = []
    struct_name = expecting(lexer_obj, WORD)
    optional(lexer_obj, SPACE)
    expecting(lexer_obj, LEFT_PARENTHESE)
    optional(lexer_obj, SPACE)
    token = lexer_obj.look_ahead()
    while token[0] != RIGHT_PARENTHESE:
        if token[0] == POINT:
            expecting(lexer_obj, POINT)
            new_struct = struct(lexer_obj)
            element.append(new_struct)
            optional(lexer_obj, SPACE)
            token = lexer_obj.look_ahead()
        else:
            new_field = field(lexer_obj)
            element.append(new_field)
            optional(lexer_obj, SPACE)
            token = lexer_obj.look_ahead()
    expecting(lexer_obj, RIGHT_PARENTHESE)
    return {"type":"struct", "name":struct_name, "field":element}

def sproto_file(lexer_obj):
    total = {"type":"file"}
    all_structs = []
    token = lexer_obj.get_next_token()
    while token[0] != EOF:
        if token[0] == SPACE:
            absort_space(lexer_obj)
        elif token[0] == POINT:
            element = struct(lexer_obj)
            all_structs.append(element)
            optional(lexer_obj, SPACE)
            token = lexer_obj.get_next_token()
    total["elements"] = all_structs
    return total

