#include "hoc.h"
#include "y.tab.h"
#include<stdio.h>
#define NSTACK 256
static Datum stack[NSTACK];
static Datum *stackp;

#define NPROG 2000
Inst prog[NPROG];
Inst *progp;
Inst *pc;
extern double Pow();

void initcode()
{
    stackp=stack;
    progp=prog;
}
void push(Datum d)
{
    if(stackp>=&stack[NSTACK])
    {
        execerror("Full stack",(char*)0);
    }
    *stackp++=d;
}
Datum pop()
{
    if(stackp<=stack)
    {
        execerror("Empty Stack",(char*)0);
    }
    return *--stackp;
}
Inst *code(Inst f)
{
    Inst *oprogp=progp;
    if(progp>=&prog[NPROG])
    {
        execerror("Program too big",(char*)0);
    }
    *progp++=f;
    return oprogp;
}
void execute(Inst *p)
{
    for(pc=p;*pc!=STOP;)
    {
        (*(*pc++))();
    }
}
void constpush()
{
    Datum d;
    d.val=((Symbol*)*pc++)->u.val;
    push(d);
}
void varpush()
{
    
    Datum d;
    d.sym=(Symbol*)(*pc++);
    push(d);
}
void add()
{
    Datum d1,d2;
    d2=pop();
    d1=pop();
    d1.val+=d2.val;
    push(d1);
}
void sub()
{
    Datum d1,d2;
    d2=pop();
    d1=pop();
    d1.val-=d2.val;
    push(d1);
}
void mul()
{
    Datum d1,d2;
    d2=pop();
    d1=pop();
    d1.val*=d2.val;
    push(d1);
}
void divd()
{
    Datum d1,d2;
    d2=pop();
    d1=pop();
    if(d2.val==0.0)
    {
        execerror("Divizion by 0",0);
    }
    d1.val/=d2.val;
    push(d1);
}
void negate()
{
    Datum d1;
    d1=pop();
    d1.val=-d1.val;
    push(d1);
}

void power()
{
    Datum d1,d2;
    d2=pop();
    d1=pop();
    d1.val=Pow(d1.val,d2.val);
    push(d1);
}
void mod()
{
    Datum d1,d2;
    d2=pop();
    d1=pop();
    d1.val=(double)((int)d1.val%(int)d2.val);
    push(d1);
}
void eval()
{
    Datum d;
    d=pop();
    if(d.sym->type==UNDEF)
    {
        execerror("Variable no define ",d.sym->name);
    }
    d.val=d.sym->u.val;
    push(d);
}
void assign()
{
    Datum d1,d2;
    d1=pop();
    d2=pop();
    if(d1.sym->type != VAR && d1.sym->type!=UNDEF)
    {
        execerror("Assigment to non-variable",d1.sym->name);
    }
    d1.sym->u.val=d2.val;
    d1.sym->type=VAR;
    push(d2);
}
void print()
{
    Datum d;
    d=pop();
    printf("\t%.8g\n",d.val);
}

void bltin()
{
    Datum d;
    d=pop();
    d.val=(*(double (*)())(*pc++))(d.val);
    push(d);
}
void gt()
{
    Datum d1,d2;
    d2=pop();
    d1=pop();
    d1.val=(double)(d1.val>d2.val);
    push(d1);
}
void lt()
{
    Datum d1,d2;
    d2=pop();
    d1=pop();
    d1.val=(double)(d1.val<d2.val);
    push(d1);
}
void eq()
{
    Datum d1,d2;
    d2=pop();
    d1=pop();
    d1.val=(double)(d1.val==d2.val);
    push(d1);
}
void ne()
{
    Datum d1,d2;
    d2=pop();
    d1=pop();
    d1.val=(double)(d1.val!=d2.val);
    push(d1);
}
void and()
{
    Datum d1,d2;
    d2=pop();
    d1=pop();
    d1.val=(double)(d1.val&&d2.val);
    push(d1);
}
void or()
{
    Datum d1,d2;
    d2=pop();
    d1=pop();
    d1.val=(double)(d1.val||d2.val);
    push(d1);
}
void not()
{
    Datum d1;
    d1=pop();
    d1.val=(double)(!d1.val);
    push(d1);
}
void ge()
{
    Datum d1,d2;
    d2=pop();
    d1=pop();
    d1.val=(double)(d1.val>=d2.val);
    push(d1);
}
void le()
{
    Datum d1,d2;
    d2=pop();
    d1=pop();
    d1.val=(double)(d1.val<=d2.val);
    push(d1);
}

void whilecode()
{
    Datum d;
    Inst *savepc=pc;
    execute(savepc+2);
    d=pop();
    while(d.val)
    {
        execute(*((Inst **)(savepc)));
        execute(savepc+2);
        d=pop();
    }
    pc=*((Inst **)(savepc+1));
}
void ifcode()
{
    Datum d;
    Inst *savepc=pc;
    execute(savepc+3);
    d=pop();
    if(d.val)
    {
        execute(*((Inst **)(savepc)));
    }
    else if(*((Inst **)(savepc+1)))
    {
        execute(*((Inst **)(savepc+1)));
    }
    pc=*((Inst **)(savepc+2));
}
void switchcode()
{
    Inst *savepc=pc;
    Datum d;
    execute(savepc+2);
    pc++;
}

void casecode(){
    Datum d1,d2;

    Inst *savepc=pc;
    execute(savepc+2);
    d1=pop();
    d2=pop();
    push(d2);

    float v1,v2;
    v1=(char)d1.val;
    v2=(char)d2.val;
    printf("\nD1 %lf", d1.val);
    printf("\nD2 %lf", d2.val);

    printf("\nV1 %f", v1);
    printf("\nV2 %f", v2);

    if( v1 == v2 )
    {
        printf("\nEntre");
        execute(savepc+5);
    }
    else
    {
        push(d2);
        pc=*((Inst **)(savepc));
    }
    
}