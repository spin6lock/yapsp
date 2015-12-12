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
    elements["name"] = word
    optional(lexer_obj, SPACE)
    number = expecting(lexer_obj, NUMBER)
    elements["id"] = number
    optional(lexer_obj, SPACE)
    expecting(lexer_obj, COLON)
    optional(lexer_obj, SPACE)
    is_star = optional(lexer_obj, STAR)
    if is_star:
        elements["array"] = True
    word = expecting(lexer_obj, WORD)
    elements["type"] = word
    return elements

def sproto_type(lexer_obj):
    element = []
    sproto_type_name = expecting(lexer_obj, WORD)
    optional(lexer_obj, SPACE)
    expecting(lexer_obj, LEFT_PARENTHESE)
    optional(lexer_obj, SPACE)
    token = lexer_obj.look_ahead()
    while token[0] != RIGHT_PARENTHESE:
        if token[0] == POINT:
            expecting(lexer_obj, POINT)
            new_sproto_type = sproto_type(lexer_obj)
            element.append(new_sproto_type)
            optional(lexer_obj, SPACE)
            token = lexer_obj.look_ahead()
        else:
            new_field = field(lexer_obj)
            element.append(new_field)
            optional(lexer_obj, SPACE)
            token = lexer_obj.look_ahead()
    expecting(lexer_obj, RIGHT_PARENTHESE)
    return {"type":"sproto_type", "name":sproto_type_name, "fields":element}

def sproto_group(lexer_obj):
    total = {"type":"group"}
    all_sproto_types = []
    token = lexer_obj.get_next_token()
    while token[0] != EOF:
        if token[0] == SPACE:
            absort_space(lexer_obj)
        elif token[0] == POINT:
            element = sproto_type(lexer_obj)
            all_sproto_types.append(element)
            optional(lexer_obj, SPACE)
            token = lexer_obj.get_next_token()
    total["type"] = all_sproto_types
    return total

