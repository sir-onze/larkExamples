from lark import Lark,Token
from lark.tree import pydot__tree_to_png

""" 
  Simple CFG to represent python if conditions
  Example :
    if(x<1):
"""
grammar = '''
start: "if" "(" expr ")" ":"
expr : (LETRA|NUMERO) OP (LETRA|NUMERO)
OP: ">" | "<" | "=="
LETRA:("A".."Z"|"a".."z")+
NOME: ("A".."Z"|"a".."z")+
NUMERO:"0".."9"+
PONTO:"."
%import common.WS
%ignore WS
'''
frase = "if(x>0):"
p = Lark(grammar)

# Parsing input phrase
parse_tree = p.parse(frase)
print(parse_tree.pretty())

# Visualizing tree structure
for token in parse_tree.children:
  print (token)

## Retrieve all tokens

all_tokens = parse_tree.scan_values(lambda v: isinstance(v, Token))

r = ""
for token in all_tokens:
    print(token,token.type) 
    r+=token

print(r)
