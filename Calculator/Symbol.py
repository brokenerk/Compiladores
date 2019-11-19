#!python3

from hoc_h import Symbol,Symbols

def lookup(s):
    print("Entre a buscar")
    print("KEYS")
    print(Symbols.keys())

    for Key in Symbols.keys():
        print('{}: val:{} type:{}, func:{}'.format( Key,Symbols[Key].getVal(),Symbols[Key].getType(),Symbols[Key].getFunc() ))

    if s in Symbols.keys():
        if Symbols[s].getType() == "VAR":
            return 1
        elif Symbols[s].getType() == "CONST":
            return 2
    else:
        return 0

def install(s,t,d):
    print("entre a instalar")
    sym = Symbol(s,t,d,None,None)
    return sym

