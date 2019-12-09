#!python3
from Node import Node
from Lexer import Lexer
from Token import Token
from copy import deepcopy
epsilon = '\u03B5'

class LR1:
    #Constructor
    def __init__(self, rules, stringLex):
        self.rules = rules              #List<Node>
        #self.auxListItem = []           #List<List<Node>>
        self.table = []                 #List<List>
        self.analysisTable = []         #List<List>
        self.terminals = set([])        #Set<String>
        self.noTerminals = set([])      #Set<String>
        self.itemSets = []              #List<(List<Node>, Set<String>)>
        self.visitedRules = set([])     #Set<List<Node>>
        self.index = {}                 #Dictionary
        self.visited = set()            #Set<String>
        self.rulesDictionary = {}       #Dictionary Rules
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

    #Parameters: Nothing
    #Return: Nothing
    #Note: Fill LR(1) Table
    def initializeTable(self):
        nt = list(self.noTerminals)
        t = list(self.terminals)
        
        nt.sort()
        t.sort()
        t.append("$")
        self.table.append([0] * (len(t) + len(nt) + 1))

        j = 1
        for i in range(0, len(t)):
            self.index[t[i]] = j
            self.table[0][j] = t[i]
            j += 1

        for i in range(0, len(nt)):
            self.index[nt[i]] = j
            self.table[0][j] = nt[i]
            j += 1

    #Parameters: Symbol
    #Return: List<Node>
    def searchRule(self, symbol):
        listRules = []
        for rule in self.rules:
            if(rule.getSymbol() == symbol):
                listRules.append(rule)  
        return listRules

    #Parameters: Symbol, Set<List<Node>>
    #Return: List<String>
    def getSymbolItems(self, state):
        symbolItems = set([])
        for rule in state:
            next = rule.getNext()
            while(next != None):
                if(next.getPointBefore() and next.getSymbol() != "epsilon"):
                    symbolItems.add(next.getSymbol())
                next = next.getNext()
        l = list(symbolItems)
        l.sort()
        return l

    #Parameters: Set<List<Node>>
    #Return: Boolean
    def exists(self, s1):
        #Iterate the item sets
        i = 0
        for s2 in self.itemSets:
            cont1 = 0
            cont2 = 0
            for r1, r2 in zip(s1, s2):
                #If a rule matches, increment cont2
                if(r1.equals(r2) == True and r1.getLR1Symbols() == r2.getLR1Symbols()):
                    cont2 += 1
                cont1 += 1
            #If both conts are the same, it means that item set s1 was already calculated (exists)
            if(cont1 == cont2):
                return i
            i += 1
        #If both conts never matched, it's a new item set
        return -1

    #Parametes: List<Node>
    #Return: Set<List<Node>>
    def itemClosure(self, s):
    	symbols = set([])
    	for rule in s:
	        #self.auxListItem.append(rule)
	        next = rule.getNext()
	        while(next != None):
	            if(next.getPointBefore()):
	                if(next.getSymbol() in self.noTerminals):
	                	n = next.getNext()

	                	if(n != None):
	                		symbols = self.first(n.getSymbol())
		                else:
		                	symbols = rule.getLR1Symbols()

	                	nextRules = self.searchRule(next.getSymbol())
	                	for r in nextRules:
	                		belongs = False
	                		for r1 in s:
	                			if(r.equals(r1) == True):
	                				r1.setLR1Symbols(symbols.union(r1.getLR1Symbols()))
	                				belongs = True
	                				break

	                		if(belongs == False):
		                		r.getNext().setPointBefore(True)
		                		r.setLR1Symbols(symbols.union(r.getLR1Symbols()))
		                		s.append(deepcopy(r))
	            next = next.getNext()
    	return s

    #Parametes: Set<Node>, String
    #Return: Set<Node>
    def move(self, state, symbol):
        l = []
        for rule in state:
            next = rule.getNext()
            while(next != None):
                if(next.getSymbol() == symbol and next.getPointBefore() == True):
                    next.setPointBefore(False)
                    n = next.getNext()
                    if(n != None):
                        n.setPointBefore(True)
                    else:
                        next.setPointAfter(True)

                    l.append(rule)
                next = next.getNext()
        return l

    #Parametes: Set<Node>, String
    #Return: Set<Node>
    def goTo(self, state, symbol):
        return self.itemClosure(self.move(state, symbol))

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
    def isLR1(self):
        self.setNoTerminals()
        self.setTerminals()
        self.initializeTable()
        self.initializeCounter()
        firstRule = self.rules[0]
        firstRule.setLR1Symbols(set(["$"]))
        firstRule.getNext().setPointBefore(True)

        S0 = self.itemClosure([firstRule])
        queue = [S0]    #Queue<Set>
        self.itemSets.append(S0)    #List<List<Node>>
        cont = 1

        print("")
        print("S0")
        for rule in S0:
            rule.displayItems()
            print(str(rule.getLR1Symbols()))

        #Table LR(1)
        self.table.append([0] * (len(self.terminals) + len(self.noTerminals) + 2)) #Include $ and extended grammar
        self.table[0][0] = " "
        i = 0

        while queue:
            Si = queue.pop(0)   #Get first enter
            symbolItems = self.getSymbolItems(Si)
            #Iterate over the item symbols
            for symbol in symbolItems:
                self.visitedRules = set([])
                aux = self.goTo(deepcopy(Si), symbol)

                #Set is empty, do nothing
                if(aux == set()):
                    continue
    
                pair = []
                pair.insert(0, "d") #Insert a pair in the list 
                
                #Verify is set already exists in list
                check = self.exists(aux) #Verify is set already exists in list
                                
                if(check != -1):
                    pair.insert(1, check)
                    # Check if there is an error
                    if(self.table[i + 1][self.index[symbol]] != 0):
                        if(symbol != "$"):
                            return False
                        else:
                            continue
                    else:
                        self.table[i + 1][self.index[symbol]] = pair
                    continue

                self.table.append([0] * (len(self.terminals) + len(self.noTerminals) + 2)) #Include $ and extended grammar
                self.table[cont + 1][0] = cont
                pair.insert(1, cont)
                self.table[i + 1][self.index[symbol]] = pair
                
                queue.append(aux)           #Add new set to the end of the queue
                self.itemSets.append(aux)   #Add the new set to the list

                print("\n" + "S" + str(cont))
                for rule in aux:
                    rule.displayItems()
                    print(str(rule.getLR1Symbols()))
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
                                    if(symbol != "$"):
                                        return False
                                    else:
                                        continue
                                else:
                                    self.table[cont + 1][self.index[symbol]] = ruleTable
                                    
                        next = next.getNext()
                cont += 1
            i += 1
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
    #Note: Show table of LR1
    def displayTable(self, op):
        if op == 0:
            print("\nTABLA RELACION DE REGLAS")
            for i in self.table:
                print(i)
        else:
            print("\nTABLA ANALISIS LR(1)")
            for i in self.analysisTable:
                print(i)

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
            x = lastP + 1

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

            #Get action from table of LR1
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
                        x = p[len(p) - 1] + 1  #Calculated coordinate X
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

    #Parameters: Terminals or No terminals symbols
    #Return: Set of terminals or Epsilon
    def first(self, symbol):
        c = set()   #Set<>
        self.visited.add(symbol)
        if symbol in self.terminals:
            c.add(symbol)
        else:
            for j in range(0, len(self.rules)):
                if symbol == self.rules[j].getSymbol():
                    if self.rules[j].getNext().getSymbol() not in self.visited:
                        c = c.union(self.first(self.rules[j].getNext().getSymbol()))
        return c