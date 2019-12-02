#include"hoc.h"
#include<stdio.h>
#include"y.tab.h"
extern double pow();

#define NSTACK 256
static Datum stack[NSTACK];
static Datum *stackp;

#define NPROG 2000
Inst prog[NPROG], *progp, *pc;

void initcode(void){
    stackp = stack;
    progp = prog;
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
    for (pc = p; *pc->opr != STOP;)
        (*pc++).opr();
}

Datum constpush(void){
    Datum d;
    d.val=(*pc++).val;
    push(d);
    return (Datum){0};
}

Datum varpush(void){
    Datum d;
    d.sym = (*pc++).sym;
    push(d);
    return (Datum){0};
}

Datum add(void){
    Datum d1,d2;
    d2 = pop();
    d1 = pop();
    d1.val += d2.val;
    push(d1);
    return (Datum){0};
}

Datum sub(void){
    Datum d1,d2;
    d2 = pop();
    d1 = pop();
    d1.val -= d2.val;
    push(d1);
    return (Datum){0};
}

Datum divd(void){
    Datum d1,d2;
    d2 = pop();
    d1 = pop();
    if (d2.val == 0)
        execerror("Division by Zero", "");
    d1.val /= d2.val;
    push(d1);
    return (Datum){0};
}

Datum mul(void){
    Datum d1,d2;
    d2 = pop();
    d1 = pop();
    d1.val *= d2.val;
    push(d1);
    return (Datum){0};
}

Datum power(void){
    Datum d1,d2;
    d2 = pop();
    d1 = pop();
    d1.val = pow(d1.val,d2.val);
    push(d1);
    return (Datum){0};
}

Datum negate(void){
    Datum d1;
    d1 = pop();
    d1.val *= (-1);
    push(d1);
    return (Datum){0};
}

Datum eval(void){
    Datum d;
    d = pop();
    if (d.sym->type == UNDEF )
        execerror("undefined variable ", d.sym->name);
    d.val = d.sym->u.val;
    push(d);
    return (Datum){0};
}

Datum assign(void){
    Datum d1, d2;
    d1 = pop();
    d2 = pop();
    if (d1.sym->type != VAR && d1.sym->type != UNDEF && d1.sym->type != CONST )
        execerror("assignment to non-variable ", d1.sym->name);
    d1.sym->u.val = d2.val;
    d1.sym->type = VAR;
    push(d2);
    return (Datum){0};
}

Datum print(void){
    Datum d;
    d = pop();
    printf("\t%.8g\n",d.val);
    return (Datum){0};
}

Datum bltin(void){
    Datum d;
    d = pop();
    d.val = (*pc++).ptr( (d.val) );
    push(d);
    return (Datum){0};
}
