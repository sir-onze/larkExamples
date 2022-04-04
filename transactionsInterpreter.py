from lark import Discard
from lark import Lark,Token
from lark.tree import pydot__tree_to_png
from lark.visitors import Interpreter

"""  
  Interpreter class to apply semantic actions to each non terminal and terminal productions.
  We calculate the total ammount and count of debts and credit operation. Also list the name of the accounts and some naive date validation.
""" 
class InterpreterA(Interpreter):
    def __init__(self):
        self.totalDebito = 0
        self.nDebito = 0
        self.totalCredito = 0
        self.nCrebito = 0
        self.contasDeb = []
        self.dataAtual = 0
        self.erro = []

    def transacoes(self, tree):
        r =self.visit(tree.children[1])
        return ( self.totalDebito,self.nDebito,self.totalCredito,self.nCrebito,self.contasDeb,self.erro)

    def movimentos(self, tree):
        for elemento in tree.children:
          self.visit(elemento)

    def move(self, tree):
        # Visit children to get all tokens
        r = self.visit_children(tree)
        if(r[2]=='CREDITO'):
          self.totalCredito += int(r[3][0])
        if(r[2]=='DEBITO'):
          self.totalDebito += int(r[3][0])
          self.contasDeb.append(str(r[1][0]))
        dataAtual = int(r[0][0])
        data = self.validaDatas(self.dataAtual,dataAtual)
        if not data:
          self.erro.append((dataAtual,str(r[1][0]))) # imprime a data em Erro, que está fora da ordem
        else:
          self.dataAtual = dataAtual
      
    def sinal_debito(self, tree):
      token = self.visit_children(tree)
      self.nDebito += 1
      return (str(token[0]))
    
    def sinal_credito(self, tree):
      self.nCrebito += 1
      token = self.visit_children(tree)
      return (str(token[0]))

    def validaDatas(self,dataAtual,dataProx):
      r = True
      if dataAtual > dataProx:
        r = False
      return r
  
  
    
# GIC
grammar = '''
transacoes: BTASK movimentos ETASK
movimentos: move "."  (move ".")*
move : data ";" contadest ";" sinal ";" quant ";" ordenante ";" descr 
contadest : ID
sinal : CREDITO -> sinal_credito
      | DEBITO -> sinal_debito
quant : INT
ordenante : ID
descr : ESCAPED_STRING
data : INT
BTASK :"-#"
ETASK :"#-"
ID : ("A".."Z"|"a".."z"|"0".."9")+
DEBITO : "DEBITO"
CREDITO : "CREDITO"

%import common.WS
%import common.ESCAPED_STRING
%import common.WORD
%import common.INT
%ignore WS
'''

frase = """-# 20220321 ; pt12345 ; CREDITO ; 50 ; pt9876 ; "entrada de dinheirinho".
              20200321 ; pt12345 ; DEBITO; 10 ; pt9876 ; "entrada de dinheirinho2".
              20220621 ; pt15545 ; CREDITO ; 10 ; pt9876 ; "saida de dinheirinho".
              20210721 ; pt1445 ; DEBITO; 40 ; pt1176 ; "entrada de dinheirinho2". #-"""
p = Lark(grammar,start="transacoes")
parse_tree = p.parse(frase)
data = InterpreterA().visit(parse_tree)
print(data)
