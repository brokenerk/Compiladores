#include"hoc.h"
#include<stdio.h>
#include"y.tab.h"
extern double pow();

#define NSTACK 256
static Datum stack[NSTACK];
static Datum *stackp;
int returning;

#define NPROG 2000
Inst prog[NPROG], *progp, *pc;

void initcode(void){
    stackp = stack;
    progp = prog;
    returning = 0;    

}

void push(Datum d){
    if(stackp >= &stack[NSTACK])
        execerror("stack overflow", (char *)0);
    *stackp++ = d;
}

Datum pop(void){
    if (stackp <= stack)
        execerror("stack underflow", (char*) 0);
    return *--stackp;
}

Inst *code(Inst f){
    Inst *oprogp = progp;
    if ( progp >= &prog[NPROG] )
        execerror("program too big",(char*)0);
    *progp++ = f ;
    return oprogp;
}

void execute(Inst *p){
    Datum d;
    for (pc = p; *pc != STOP;)
        (*(*pc++))();
}

void constpush(void){
    Datum d;
    d.val=((Symbol *)*pc++)->u.val;
    push(d);
}

void varpush(void){
    Datum d;
    d.sym = (Symbol *)(*pc++);
    push(d);
}

void add(void){
    Datum d1,d2;
    d2 = pop();
    d1 = pop();
    d1.val += d2.val;
    push(d1);
}

void sub(void){
    Datum d1,d2;
    d2 = pop();
    d1 = pop();
    d1.val -= d2.val;
    push(d1);
}

void divd(void){
    Datum d1,d2;
    d2 = pop();
    d1 = pop();
    if (d2.val == 0)
        execerror("Division by Zero", "");
    d1.val /= d2.val;
    push(d1);
}

void mul(void){
    Datum d1,d2;
    d2 = pop();
    d1 = pop();
    d1.val *= d2.val;
    push(d1);
}

void power(void){
    Datum d1,d2;
    d2 = pop();
    d1 = pop();
    d1.val = pow(d1.val,d2.val);
    push(d1);
}

void negate(void){
    Datum d1;
    d1 = pop();
    d1.val *= (-1);
    push(d1);
}

void eval(void){
    Datum d;
    d = pop();
    if (d.sym->type == UNDEF )
        execerror("undefined variable ", d.sym->name);
    d.val = d.sym->u.val;
    push(d);
}

void assign(void){
    Datum d1, d2;
    d1 = pop();
    d2 = pop();
    if (d1.sym->type != VAR && d1.sym->type != UNDEF && d1.sym->type != CONST )
        execerror("assignment to non-variable or it's a constant", d1.sym->name);
    d1.sym->u.val = d2.val;
    d1.sym->type = VAR;
    push(d2);
}

void print(void){
    Datum d;
    d = pop();
    printf("\t%.8g\n",d.val);
}

void bltin(void){
    Datum d;
    d = pop();
    d.val = (*(double(*)())(*pc++))(d.val);
    push(d);
}

void le(void){
    Datum d1,d2;
    d2 = pop();
    d1 = pop();
    d1.val = (double)(d1.val <= d2.val);
    push(d1);
}

void lt(void){
    Datum d1,d2;
    d2 = pop();
    d1 = pop();
    d1.val = (double)(d1.val < d2.val);
    push(d1);
}

void gt(void){
    Datum d1,d2;
    d2 = pop();
    d1 = pop();
    d1.val = (double)(d1.val > d2.val);
    push(d1);
}

void ge(void){
    Datum d1,d2;
    d2 = pop();
    d1 = pop();
    d1.val = (double)(d1.val >= d2.val);
    push(d1);
}

void eq(void){
    Datum d1,d2;
    d2 = pop();
    d1 = pop();
    d1.val = (double)(d1.val == d2.val);
    push(d1);
}

void ne(void){
    Datum d1,d2;
    d2 = pop();
    d1 = pop();
    d1.val = (double)(d1.val != d2.val);
    push(d1);
}

void and(void){
    Datum d1,d2;
    d2 = pop();
    d1 = pop();
    d1.val = (double)(d1.val != 0.0 && d2.val != 0.0);
    push(d1);
}

void or(void){
    Datum d1,d2;
    d2 = pop();
    d1 = pop();
    d1.val = (double)(d1.val != 0.0 || d2.val != 0.0);
    push(d1);
}

void not(void){
    Datum d1;
    d1 = pop();
    d1.val = (double)(d1.val == 0.0);
    push(d1);
}

void ifcode(void){
    Datum d;
    Inst *savepc = pc;
    execute (savepc+3);
    d=pop();
    if (d.val)
        execute( *((Inst**)(savepc)) );
    else if ( *((Inst**)(savepc+1)) )
        execute( *((Inst**)(savepc+1)) );
    pc = *((Inst**)(savepc+2));
}

void whilecode(void){
    Datum d;
    Inst *savepc = pc;
    execute(savepc+2);
    d = pop();
    while (d.val){
        execute( *((Inst**)(savepc)) );
        execute(savepc+2);
        d=pop();
    }
    pc = *((Inst**)(savepc+1));
}

void forcode(void){
    Datum d;
	Inst *savepc = pc;

	execute(savepc+4);
	pop();
	execute(*((Inst **)(savepc)));
	d = pop();
	while (d.val) {
		execute(*((Inst **)(savepc+2)));
		execute(*((Inst **)(savepc+1)));
		pop();
		execute(*((Inst **)(savepc)));
		d = pop();
	}
		pc = *((Inst **)(savepc+3));
}

void prexpr(void){
    Datum d;
    d = pop();
    printf("%.8g\n",d.val);
}