#encoding:utf8
import collections

def rearrange_type_order(ast):
    types = ast["type"]
    new_types = {}
    for sproto_type in types:
        name = sproto_type["name"]
        new_types[name] = sproto_type
    ast["type"] = new_types

def remove_token_info(ast):
    for k, v in ast.iteritems():
        if type(v) == dict:

def annotation(ast):
    #type check
    remove_token_info(ast)
    rearrange_type_order(ast)
