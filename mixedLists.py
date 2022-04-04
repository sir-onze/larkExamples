!pip install lark
from lark import Discard
from lark import Lark,Token
from lark.tree import pydot__tree_to_png
from lark import Transformer

class MyTransformer(Transformer):
    def __init__(self):
        self.output = {}
        self.comprimento = 0
        self.soma = 0

    def start(self, items):
        return (items[0]+"\n\t"+str(items[1])+"\n"+items[2])

    def elementos(self, elementos):
        self.output["soma"] = self.soma
        self.output["comprimento"] = self.comprimento
        self.output["lista"] = elementos
        return self.output

    def NUMERO(self,numero):
        self.soma += int(numero)
        self.comprimento += 1
        numero = int(numero) # Can remove it out if the int type is not needed
        return numero

    def PALAVRA(self,palavra):
        self.comprimento +=1
        palavra = str(palavra) # Can remove it out if the int type is not needed
        return palavra 

    def PE(self,abre):
        return "Open"

    def PD(self,fecha):
        return "Close"

    def VIR(self,op):
        return Discard # Allows to ignore and discard a terminal or non Terminal rule


""" 
  Simple CFG to represent python list of numbers and characters
  Example :
    [1,2,list,3,mixed]
"""
grammar = '''
start: PE elementos PD
elementos : (NUMERO|PALAVRA) (VIR (NUMERO|PALAVRA))*
NUMERO:"0".."9"+
PALAVRA:("A".."Z"|"a".."z")+
PE:"["
PD:"]"
VIR:","

%import common.WS
%ignore WS
'''

frase = "[a,1,2,3,a,4]"
p = Lark(grammar)
parse_tree = p.parse(frase)

data = MyTransformer().transform(parse_tree)
print(data)
