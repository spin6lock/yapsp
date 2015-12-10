import pprint
import re
word = re.compile("([.*]?\w+)")
number = re.compile("\d+")
space = re.compile("\s+")

SPACE = "SPACE"
WORD = "WORD"
NUMBER = "NUMBER"
LEFT_PARENTHESE = "LEFT_PARENTHESE"
RIGHT_PARENTHESE = "RIGHT_PARENTHESE" 
POINT = "POINT"
STAR = "STAR"
SPACE = "SPACE"
COLON = "COLON"
EOF = "EOF"
BREAK = "BREAK"

with open("array_type.sproto", "r") as fin:
    content = fin.read()

def lexer(content):
    i=0
    length=len(content)
    #import ipdb; ipdb.set_trace()
    while i<length:
        char = content[i]
        if char.isalpha():
            match=word.search(content[i:])
            pos = match.end()
            i = i + pos
            #print "WORD", match.group(0)
            yield [WORD, match.group(0)]
        elif char == ".":
            i = i + 1
            yield [POINT]
        elif char == "*":
            i = i + 1
            yield [STAR]
        elif char.isdigit():
            match = number.search(content[i:])
            pos = match.end()
            i = i + pos
            #print "NUMBER", match.group(0)
            yield [NUMBER, match.group(0)]
        elif char == "{":
            i = i + 1
            #print "LEFT_PARENTHESE"
            yield [LEFT_PARENTHESE]
        elif char == "}":
            i = i + 1
            #print "RIGHT_PARENTHESE"
            yield [RIGHT_PARENTHESE]
        elif char.isspace():
            match = space.search(content[i:])
            pos = match.end()
            i = i + pos
            #print SPACE
            yield [SPACE]
        elif char == ":":
            i = i + 1
            #print COLON
            yield [COLON]
        else:
            print BREAK
            print content[i:]
            break

class Lexer(object):
    def __init__(self, token_seq):
        self.stash = []
        self.token_seq = token_seq

    def get_next_token(self):
        if len(self.stash) > 0:
            token = self.stash.pop(0)
            return token
        else:
            try:
                token = self.token_seq.next()
            except StopIteration:
                token = [EOF]
            return token

    def look_ahead(self):
        if len(self.stash) > 0:
            token = self.stash[0]
            return token
        else:
            token = self.get_next_token()
            self.stash.append(token)
            return token

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
        new_field = field(lexer_obj)
        element.append(new_field)
        optional(lexer_obj, SPACE)
        token = lexer_obj.look_ahead()
    expecting(lexer_obj, RIGHT_PARENTHESE)
    return {"name":struct_name, "field":element}

def sproto_file(lexer_obj):
    all_structs = []
    token = lexer_obj.get_next_token()
    while token[0] != EOF:
        if token[0] == SPACE:
            absort_space(lexer_obj)
        elif token[0] == POINT:
            element = struct(lexer_obj)
            all_structs.append(element)
            optional(lexer_obj, SPACE)
            token = lexer_obj.look_ahead()
    return all_structs

f = lexer(content)
lexer_obj = Lexer(f)
all_structs = sproto_file(lexer_obj)
pprint.pprint(all_structs)
