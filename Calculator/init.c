#include "hoc.h"
#include "y.tab.h"
#include <math.h>

extern double Log(), Log10(), Exp(), Sqrt(), integer();

static struct{
	char * name;
	double cval;
} constant[] = {
	"PI",	3.14159265358979323846,
	"E",	2.71828182845904523536,
	"GAMMA",0.57721566490153286060,
	"DEG", 57.29577951308232087680,
	"PHI",	1.61803398874989484820,
	0,	0
};

static struct{
	char *name;
	double (*func)();
} builtins[] = {
	"sin",	sin,
	"cos",	cos,
	"atan",	atan,
	"log",	Log,
	"log10",Log10,
	"exp",	Exp,
	"sqrt",	Sqrt,
	"int",	integer,
	"abs",	fabs,
	0,	0
};
void init(void){
	int i;
	Symbol *s;
	for (i=0; constant[i].name; i++)
		install(constant[i].name, CONST ,constant[i].cval);
	for (i=0; builtins[i].name;i++){
		s = install(builtins[i].name, BLTIN,0.0);
		s->u.ptr = builtins[i].func;
	}
}
