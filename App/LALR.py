#!python3
from Node import Node
from Lexer import Lexer
from Token import Token
from copy import deepcopy
from LR1 import LR1
epsilon = '\u03B5'

class LALR:
    #Constructor
    def __init__(self, rules, stringLex):
        self.rules = rules              #List<Node>
        self.terminals = set([])        #Set<String>
        self.noTerminals = set([])      #Set<String>
        self.table = []                 #List<List>
        self.tableLR1 = []              #List<List>
        self.analysisTable = []         #List<List>
        self.itemSets = []              #List<List<Node>>
        self.index = {}                 #Dictionary
        self.rulesDictionary = {}       #Dictionary
        self.stringLex = stringLex      #Lexer

    #Parameters: Nothing
    #Return: Nothing
    #Note: Fill set of no terminals symbols
    def setNoTerminals(self):
        for i in range(0, len(self.rules)):
            self.noTerminals.add(self.rules[i].getSymbol()) 
            
    #Parameters: Nothing
    #Return: Nothing 
    #Note: Fill set of terminal symbols
    def setTerminals(self):
        for i in range(0, len(self.rules)):
            next = self.rules[i].getNext()
            while(next != None):
                st = next.getSymbol()
                if st not in self.noTerminals:
                    self.terminals.add(st)
                next = next.getNext()
        if("epsilon" in self.terminals):
            self.terminals.remove("epsilon")

    #Parameters: Nothing 
    #Return: List<List>
    #Note: Rule Relations Table
    def getTable(self):
        return self.table

    #Parameters: Nothing 
    #Return: List<List>
    #Note: Analysis Table
    def getAnalysisTable(self):
        return self.analysisTable

    #Parameters: LR1
    #Return: Nothing
    #Note: Fill LALR Table
    def initializeTable(self, lr1):
        self.tableLR1 = lr1.getTable()
        self.table.append(self.tableLR1[0])

        for i in range(1, len(self.tableLR1)):
            for j in range(1, len(self.tableLR1[i])):
                self.index[self.tableLR1[0][j]] = j
                if(self.tableLR1[i][j] != 0):
                    r = self.tableLR1[i][j]
                    if(r[0] != 'd'):
                        self.tableLR1[i][j] = 0

    #Parameters: Set<List<Node>>
    #Return: Boolean
    def exists(self, s1):
        #Iterate the item sets
        for s2 in self.itemSets:
            cont1 = 0
            cont2 = 0
            for r1, r2 in zip(s1, s2[1]):
                #If a rule matches, increment cont2
                if(r1.equals(r2) == True):
                    cont2 += 1
                cont1 += 1
            #If both conts are the same, it means that item set s1 was already calculated (exists)
            if(cont1 == cont2):
                for r1, r2 in zip(s1, s2[1]):
                    #Merge LR1 symbols
                    r2.setLR1Symbols(r2.getLR1Symbols().union(r1.getLR1Symbols()))
                return s2[0]
        #If both conts never matched, it's a new item set
        return -1

    #Parameters: Nothing
    #Return: Nothing
    #Note: Create a dictionary
    def initializeCounter(self):
        i = 0
        for rule in self.rules:
            rule.setCounter(i)
            self.rulesDictionary[i] = rule
            i += 1

    #Parameters: Nothing
    #Return: Nothing
    #Note: Generate the states for the displacements on the relations table
    def isLALR(self):
        self.setNoTerminals()
        self.setTerminals()
        #Do LR(1) first
        lr1 = LR1(self.rules, None)
        if(lr1.isLR1() == False):
            return False

        self.initializeTable(lr1)
        self.initializeCounter()
        cont = 0
        cont2 = 0

        #Table LALR
        self.table[0][0] = " "

        for s in lr1.getItemSets(): 
            #Verify is set already exists in list
            check = self.exists(s)
            if(check != -1):
                for i in range(1, len(self.table)):
                    if(self.table[i][0] == check):
                        self.table[i][0] = [check, cont2]
            else:
                self.table.append([0] * len(self.tableLR1[0])) #Include $ and extended grammar
                self.table[cont + 1][0] = cont2
                self.itemSets.append((cont2, s))
                cont += 1
            cont2 += 1

        cont = 0
        for s in self.itemSets:
            #print("\n" + "S" + str(cont))
            for rule in s[1]:
                #rule.displayItems()
                #print(str(rule.getLR1Symbols()))
                #Adding Rules 
                next = rule.getNext()
                while(next != None):
                    if(next.getPointAfter() or next.getSymbol() == "epsilon"):
                        for symbol in rule.getLR1Symbols():
                            ruleTable = []  #Add a pair: [r, cont]
                            if(self.rules[0].getCounter() == rule.getCounter()):
                                ruleTable.insert(0, 0)
                                ruleTable.insert(1, "accept")
                            else:
                                ruleTable.insert(0, "r")
                                ruleTable.insert(1, rule.getCounter())
                            
                            # Check if there is an error
                            if(self.table[cont + 1][self.index[symbol]] != 0):
                                return False
                            else:
                                self.table[cont + 1][self.index[symbol]] = ruleTable
                                
                    next = next.getNext()
            cont += 1

        #Add displacements for formatted states
        for i in range(1, len(self.table)):
            state = self.table[i][0]
            if type(state) is list:
                state = state[0]
                
            for j in range(1, len(self.tableLR1)):
                if(self.tableLR1[j][0] == state):
                    for k in range(1, len(self.tableLR1[j])):
                        if(self.tableLR1[j][k] != 0):
                            self.table[i][k] = self.tableLR1[j][k]

        del lr1
        return True

    #Parameters: Nothing
    #Return: Nothing
    #Note: Generate the initial table of the analysis
    def initAnalysisTable(self):
        self.analysisTable.append([0] * 3)
        self.analysisTable[0][0] = "Stack"
        self.analysisTable[0][1] = "String"
        self.analysisTable[0][2] = "Action"

    #Parameters: List
    #Return: String
    def convertToString(self, l):
        s = ""
        for i in range(0, len(l)):
            s = s + str(l[i])
        return s

    #Parameters: Nothing
    #Return: Nothing
    #Note: Show table of LALR
    def displayTable(self, op):
        if op == 0:
            print("\nTABLA RELACION DE REGLAS")
            for i in self.table:
                print(i)
        else:
            print("\nTABLA ANALISIS LALR")
            for i in self.analysisTable:
                print(i)

    #Parameters: Nothing
    #Return: Integer
    #Note: Get the correct index of the searched state
    def findRowState(self, state):
        for i in range(1, len(self.table)):
            s = self.table[i][0]
            if type(s) is list:
                if(state == s[0] or state == s[1]):
                    return i
            else:
                if(s == state):
                    return i

    #Parameters: string
    #Return: True if the string allow to the grammar, false in other case
    def analyze(self, c):
        self.initAnalysisTable()
        p = []
        srt = []
        p.append(self.rules[0].getCounter())

        #Convert to list
        for i in range(0, len(c)):
            srt.append(c[i])
        srt.append("$")

        #Get tokens, begin and end for pops
        token = self.stringLex.getToken()
        begin = self.stringLex.getStatus().getBeginLexPos()
        end = self.stringLex.getStatus().getEndLexPos()

        while p:
            #There are no symbols to analyze    
            if len(srt) == 0:
                return False
            values = []             #Aux to generate front table
            lastP = p[len(p) - 1]   #Top of the stack
            strAnalysis = srt[0]    #Symbol to analyze
            
            #Get Coordinates to the first action
            x = self.findRowState(lastP)

            #Check tokens through string lexer
            if strAnalysis in self.terminals or strAnalysis == "$":
                y = self.index[strAnalysis]
            elif(token == Token.NUM and "num" in self.terminals):
                y = self.index["num"]
                strAnalysis = "num"
            elif(token == Token.ARROW and "FLECHA" in self.terminals):
                y = self.index["FLECHA"]
                strAnalysis = "FLECHA"
            elif(token == Token.SEMICOLON and "PC" in self.terminals):
                y = self.index["PC"]
                strAnalysis = "PC"
            elif(token == Token.OR and "OR" in self.terminals):
                y = self.index["OR"]
                strAnalysis = "OR"
            elif(token == Token.CONCAT and "AND" in self.terminals):
                y = self.index["AND"]
                strAnalysis = "AND"
            elif(token == Token.COMMA and "coma" in self.terminals):
                y = self.index["coma"]
                strAnalysis = "coma"
            elif(token == Token.SYMBOL):
                if("SIMBOLO" in self.terminals):
                    y = self.index["SIMBOLO"]
                    strAnalysis = "SIMBOLO"
                elif("id" in self.terminals and self.stringLex.getLexem() == "id"):
                    y = self.index["id"]
                    strAnalysis = "id"
                elif("sin" in self.terminals and self.stringLex.getLexem() == "sin"):
                    y = self.index["sin"]
                    strAnalysis = "sin"
                else:
                    break
            else:
                break

            #Get action from table of LALR
            action = self.table[x][y]

            if(action == 0):
                return False

            #Front table
            values.append(self.convertToString(p))
            values.append(self.convertToString(srt))
            values.append(self.convertToString(action))
            self.analysisTable.append(values)
            
            #Its a displacement
            if action[0] == "d":
                p.append(strAnalysis)   #Add symbol to the Stack
                p.append(action[1])     #Add number of displacement to the Stack
                #srt.pop(0)              
                #Delete symbol from the string to analyze - using lexer
                if(token != Token.ERROR and len(strAnalysis) > 1):
                    times = end - begin
                    for i in range(0, times + 1):
                        srt.pop(0)
                else:
                    srt.pop(0)
                token = self.stringLex.getToken()
                begin = self.stringLex.getStatus().getBeginLexPos()
                end = self.stringLex.getStatus().getEndLexPos()

            #Is a reduction
            elif action[0] == "r":              
                if action[1] in self.rulesDictionary:   #Verify rule number exist on rulesDictionary                    
                    toPop = self.rulesDictionary[action[1]].size() * 2  #Get rule to calculate number of symbols
                    
                    #Delete from stack the number of symbols calculated
                    while(toPop):
                        if len(p) > 0:
                            p.pop()
                        else:
                            return False
                        toPop -= 1

                    #Get Coordinates to the second action
                    if len(p) > 0:
                        x = self.findRowState(p[len(p) - 1]) #Calculated coordinate X
                    else:
                        return False

                    if self.rulesDictionary[action[1]].getSymbol() in self.index:
                        y = self.index[self.rulesDictionary[action[1]].getSymbol()] #Calculate coordinate Y
                    else:
                        return False

                    #Get second action
                    secondAction = self.table[x][y]
                    if(secondAction != 0):
                        if secondAction[0] == "d":
                            #Add to the Stack
                            p.append(self.rulesDictionary[action[1]].getSymbol())
                            p.append(secondAction[1])
                    else:
                        return False
                #Rule doesnt exist rulesDictionary
                else:
                    return False

            #Its an accepted
            elif action[0] == 0:
                return True
            
            #Error
            else:
                return False
        return False