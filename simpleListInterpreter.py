from lark import Discard
from lark import Lark,Token
from lark.tree import pydot__tree_to_png
from lark.visitors import Interpreter

"""  
  Interpreter class to apply semantic actions to desired productions.
  To calculate the count and sum of elements of the numeric type in the list.
""" 
class MyInterpreter(Interpreter):
    def __init__(self):
        self.comprimento = 0
        #self.soma = 0


    def start(self, tree):
        print("On root, visiting elements")
        r =self.visit(tree.children[1])
        print("Elementos visited,returning to main")
        print(r)
        return (self.comprimento, r)

    def elementos(self, tree):
        print("visiting elementos")
        r=0
        for elemento in tree.children:
          if (elemento.data == 'elemento'):
            print("This will be visited because is elemento")
            r += self.visit(elemento)
        return r

    def elemento(self, tree):
        r = self.visit_children(tree)
        print("elemento",r)
        if(r[0].type=='NUMERO'):
          self.comprimento += 1
          return int(r[0])
        else:
          return 0

    def vir(self, tree):
      pass # ingnoring this production since is not relevant for the output

    
## Primeiro precisamos da GIC
grammar = '''
start: PE elementos PD
elementos : elemento (vir elemento)*
vir : VIR
elemento : NUMERO | PALAVRA |ASPAS
NUMERO:"0".."9"+ 
ASPAS: ESCAPED_STRING
PALAVRA:("A".."Z"|"a".."z")+
PE:"["
PD:"]"
VIR:","

%import common.WS
%import common.ESCAPED_STRING
%ignore WS
'''

frase = "[10,pala,1,2,3,a,4,outra,\"A\"]"
p = Lark(grammar)
parse_tree = p.parse(frase)

data = MyInterpreter().visit(parse_tree)
print("Count of numbers ",data[0],"Sum: ",data[1])
