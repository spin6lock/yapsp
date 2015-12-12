import pprint
from lexer import Lexer
from parser import sproto_group

with open("sproto_example.sproto", "r") as fin:
    content = fin.read()

lexer_obj = Lexer(content)
all_structs = sproto_group(lexer_obj)
pprint.pprint(all_structs)
