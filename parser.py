import logging
from lark import Lark, logger, Transformer

logger.setLevel(logging.WARN)

preqs_parser = Lark(r"""
    ?start: "Prerequisite(s): " value

    ?value:  course
        |   altern
        |   joint
    
    
    
    course: DEPARTMENT SPACE NUMBER LETTER?
    altern: value " or " value
    joint: value " and " value

    %import common.ESCAPED_STRING
    %import common.NUMBER
    %import common.LETTER
    %import common.WORD
    %import common.WS
    
    SEMICOLON: ";"
    DEPARTMENT: /[A-Z]{2,5}/
    SPACE: " "
    COMMA: ","

    %ignore SEMICOLON
    %ignore WS
    %ignore COMMA


""", start="start")


class TreeToPreqs(Transformer):
    def course(self, s):
        return "".join(s)

    def altern(self, a):
        res = ["OR"]
        res.extend(a)
        return res

    def joint(self, j):
        res = ["AND"]
        res.extend(j)
        return res
    
    

text = "Prerequisite(s): CSE 12"
print(text)
print(preqs_parser.parse(text).pretty())
print(TreeToPreqs().transform(preqs_parser.parse(text)))


text2 = "Prerequisite(s): CSE 12 and CSE 4"
print(text2)
print(preqs_parser.parse(text2).pretty())
print(TreeToPreqs().transform(preqs_parser.parse(text2)))

text3 = "Prerequisite(s): CSE 12; and CSE 101, or CSE 15 and CSE 15L;"
print(text3)
print(preqs_parser.parse(text3).pretty())
print(TreeToPreqs().transform(preqs_parser.parse(text3)))


'''
text4 = "Prerequisite(s): CSE 12; and CSE 101, or CSE 15 and CSE 15L; or equivalent"
print(text4)
print(preqs_parser.parse(text4).pretty())

text5 = "Prerequisite(s): CSE 101. Enrollment is restricted to juniors and seniors"
print(text5)
print(preqs_parser.parse(text5).pretty())
'''
