#encoding:utf8
import re
from constants import *

word = re.compile("([.*]?\w+)")
number = re.compile("\d+")
space = re.compile("\s+")

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
    def __init__(self, content):
        token_seq = lexer(content)
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
