from lark import Lark
from lark.tree import pydot__tree_to_png
from lark import Transformer

"""  
  Transformer class to apply semantic actions to each non terminal and terminal productions.
  We calculate the sum of the list as output
""" 
class MyTransformer(Transformer):
    def start(self, items):
        output={}
        output["elementos"] = items[1]
        soma = sum(items[1])
        output["soma"] = soma
        return (output)

    def elemento(self, elemento):
        r = list(filter(lambda x: x!=',', elemento))
        return r

    def VIR(self,op):
        op = str(op)
        return op

    def NUMERO(self,numero):
        numero = int(numero)
        return numero

    def PE(self,ponto):
        ponto = str(ponto)
        return ponto

    def PD(self,ifs):
        ifs = str(ifs)
        return ifs

""" 
  CFG to a language that represents comma separated lists
  Example :
    [1,2,3,4]
"""
grammar = '''
start: PE elemento* PD
elemento : NUMERO (VIR NUMERO)*

NUMERO:"0".."9"+
PE:"["
PD:"]"
VIR:","

%import common.WS
%ignore WS
'''

frase = "[1,2,3]"
p = Lark(grammar)
# Get and pretty print of the entire tree
parse_tree = p.parse(frase)
print(parse_tree.pretty())
# Call the transformer
data = MyTransformer().transform(parse_tree)
print(data)
