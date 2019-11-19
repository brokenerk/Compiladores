#!python3

import Symbol as s
from hoc_h import Symbols
import Math_c as function

class Const:
    def __init__(self,name,cval):
        self.name = name
        self.cval = cval

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def getCval(self):
        return self.cval

    def setCval(self, cval):
        self.cval = cval

class Func:
    def __init__(self,name,func):
        self.name = name
        self.func = func

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def getFunc(self):
        return self.func

    def setfunc(self, func):
        self.func = func

consts=[ Const('PI',3.14159265358979323846),Const('E',2.71828182845904523536)
  ,Const('GAMMA',0.57721566490153286060),Const('DEG',57.29577951308232087680)
  ,Const('PHI',1.618033988749894820) ]

builtins=[ Func("sin",function.Sin),Func("cos",function.Cos),Func("atan",function.Atan),
Func("log",function.Log),Func("log10",function.Log10),Func("exp",function.Exp),
Func("sqrt",function.Sqrt),Func("int",function.Int),Func("abs",function.Abs) ]

def init( ):
    for c in consts:
        Sym = s.install( c.getName(),'VAR',c.getCval() )
        Symbols[Sym.getName()] = Sym

    for f in builtins:
        fun = s.install( f.getName(),'BLTIN',0.0 )
        fun.setFunc( f.getFunc() )
        Symbols[fun.getName()] = fun

    return Symbols
