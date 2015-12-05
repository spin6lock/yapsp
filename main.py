import re
word = re.compile("([.*]?\w+)")
number = re.compile("\d+")
space = re.compile("\s+")

with open("sproto_example.sproto", "r") as fin:
    content = fin.read()

def lexer(content):
    i=0
    length=len(content)
    #import ipdb; ipdb.set_trace()
    while i<length:
        char = content[i]
        if char.isalpha() or char=="." or char=="*":
            match=word.search(content[i:])
            pos = match.end()
            i = i + pos
            #print "WORD", match.group(0)
            yield "WORD", match.group(0)
        elif char.isdigit():
            match = number.search(content[i:])
            pos = match.end()
            i = i + pos
            #print "NUMBER", match.group(0)
            yield "NUMBER", match.group(0)
        elif char == "{":
            i = i + 1
            #print "LEFT_PARENTHESE"
            yield "LEFT_PARENTHESE"
        elif char == "}":
            i = i + 1
            #print "RIGHT_PARENTHESE"
            yield "RIGHT_PARENTHESE"
        elif char.isspace():
            match = space.search(content[i:])
            pos = match.end()
            i = i + pos
            #print "SPACE"
            yield "SPACE"
        elif char == ":":
            i = i + 1
            #print "COLON"
            yield "COLON"
        else:
            print "BREAK"
            print content[i:]
            break

f = lexer(content)
for ret in f:
    print ret
