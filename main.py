import pprint
from lexer import Lexer
from parser import sproto_file

with open("array_type.sproto", "r") as fin:
    content = fin.read()

lexer_obj = Lexer(content)
all_structs = sproto_file(lexer_obj)
pprint.pprint(all_structs)
