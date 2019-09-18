#!python3
class Token:
	END = 0
	PLUS = 10
	MINUS = 20
	PROD = 30
	DIV = 40
	PAR_L = 50
	PAR_R = 60
	NUM = 70
	POW = 80
	SIN = 90
	COS = 100
	TAN = 110
	EXP = 120
	LN = 130
	LOG = 140
	VAR = 150

	SYMBOL_LOWER = 160
	SYMBOL_UPPER = 170
	RANGELOWER = 180
	RANGEUPPER = 190
	RANGENUM = 200
	JOIN = 210
	CONCAT = 220
	POSCLO = 230
	POINT = 240
	OPTIONAL = 250
	KLEEN = 260
	EQUALS = 270

	ERROR = 1000