/* A Bison parser, made by GNU Bison 3.0.4.  */

/* Bison interface for Yacc-like parsers in C

   Copyright (C) 1984, 1989-1990, 2000-2015 Free Software Foundation, Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

#ifndef YY_YY_Y_TAB_H_INCLUDED
# define YY_YY_Y_TAB_H_INCLUDED
/* Debug traces.  */
#ifndef YYDEBUG
# define YYDEBUG 0
#endif
#if YYDEBUG
extern int yydebug;
#endif

/* Token type.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
  enum yytokentype
  {
    NUMBER = 258,
    VAR = 259,
    BLTIN = 260,
    UNDEF = 261,
    CONST = 262,
    WHILE = 263,
    IF = 264,
    ELSE = 265,
    PRINT = 266,
    SWITCH = 267,
    CASE = 268,
    BREAK = 269,
    OR = 270,
    AND = 271,
    GT = 272,
    GE = 273,
    LT = 274,
    LE = 275,
    EQ = 276,
    NE = 277,
    UNARYMINUS = 278,
    NOT = 279
  };
#endif
/* Tokens.  */
#define NUMBER 258
#define VAR 259
#define BLTIN 260
#define UNDEF 261
#define CONST 262
#define WHILE 263
#define IF 264
#define ELSE 265
#define PRINT 266
#define SWITCH 267
#define CASE 268
#define BREAK 269
#define OR 270
#define AND 271
#define GT 272
#define GE 273
#define LT 274
#define LE 275
#define EQ 276
#define NE 277
#define UNARYMINUS 278
#define NOT 279

/* Value type.  */
#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED

union YYSTYPE
{
#line 7 "hoc.y" /* yacc.c:1909  */

Inst    *inst;
Symbol  *sym;  

#line 107 "y.tab.h" /* yacc.c:1909  */
};

typedef union YYSTYPE YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif


extern YYSTYPE yylval;

int yyparse (void);

#endif /* !YY_YY_Y_TAB_H_INCLUDED  */
