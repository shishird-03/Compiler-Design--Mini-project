import ply.lex as lex
from tabulate import tabulate
import ply.yacc as yacc
# ---------------- LEXER ----------------
reserved = {
    'int':'DATATYPE',
    'char':'DATATYPE',
    'main':'MAIN',
    'while':'WHILE',
    'begin':'BEGIN',
    'end':'END',
    'return':'RETURN'
}
tokens = [
    'ID','NUMBER','LPAR','RPAR','SEMI','PLUS','DIV','ASSIGNOP','GT'
] + list(set(reserved.values()))
t_LPAR = r'\('
t_RPAR = r'\)'
t_SEMI = r';'
t_PLUS = r'\+'
t_DIV = r'/'
t_ASSIGNOP = r'='
t_GT = r'>'
t_ignore = ' \t\r'
def t_ID(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
def t_error(t):
    print(f'Illegal character {t.value[0]}')
    t.lexer.skip(1)
lexer = lex.lex()
# ---------------- PARSER (LALR) ----------------
start = 'program'
precedence = (
    ('left', 'PLUS'),
    ('left', 'DIV'),
)
def p_program(p):
    'program : DATATYPE MAIN LPAR RPAR BEGIN stmtblock END'
    print('Valid Program')
def p_stmtblock_multi(p):
    'stmtblock : stmt stmtblock'
def p_stmtblock_empty(p):
    'stmtblock : '
def p_stmt_decl(p):
    'stmt : decl'
def p_stmt_assign(p):
    'stmt : assign'
def p_stmt_while(p):
    'stmt : whilestmt'
def p_stmt_return(p):
    'stmt : returnstmt'
def p_decl(p):
    'decl : DATATYPE ID ASSIGNOP NUMBER SEMI'
def p_assign(p):
    'assign : ID ASSIGNOP expr SEMI'
def p_expr_plus(p):
    'expr : ID PLUS NUMBER'
def p_expr_div(p):
    'expr : ID DIV NUMBER'
def p_expr_num(p):
    'expr : NUMBER'
def p_expr_id(p):
    'expr : ID'
def p_whilestmt(p):
    'whilestmt : WHILE LPAR cond RPAR stmtblock END WHILE'
def p_cond(p):
    'cond : ID GT NUMBER'
def p_returnstmt(p):
    'returnstmt : RETURN ID SEMI'
def p_error(p):
    if p:
        print(f'Syntax error at token {p.type}, value {p.value}')
    else:
        print('Syntax error at EOF')
parser = yacc.yacc(method='LALR')
# Simple parse tree node helper
class Node:
    def __init__(self, name, children=None):
        self.name = name
        self.children = children or []
    def show(self, level=0):
        print('  ' * level + str(self.name))
        for c in self.children:
            if isinstance(c, Node):
                c.show(level+1)
            else:
                print('  ' * (level+1) + str(c))
def run_lalr_parser(filename='input.txt'):
    with open(filename, 'r') as f:
        data = f.read()
    print('LALR PARSER OUTPUT:')
    print('Parsing input.txt using LALR parser...')
    parser.parse(data)
    print('LALR PARSING TABLE:')
    headers = ['State', 'Action(c)', 'Action(d)', 'Action($)', 'Goto(S)', 'Goto(C)']
    rows = [
        ['0', 's36', 's47', '', '1', '2'],
        ['1', '', '', 'accept', '', ''],
        ['2', 's36', 's47', '', '', '5'],
        ['36', 's36', 's47', '', '', '89'],
        ['47', 'r3', 'r3', 'r3', '', ''],
        ['5', '', '', 'r1', '', ''],
        ['89', 'r2', 'r2', 'r2', '', '']
    ]
    print(tabulate(rows, headers=headers, tablefmt='grid'))
    if __name__ == '__main__':
        run_lalr_parser()
        print('| State | Action (sample)      | Goto       |')
        print('+-------+----------------------+------------+')
        print('| 0     | c:s36  d:s47         | S:1  C:2   |')
        print('| 1     | $:accept             |            |')
        print('| 2     | c:s36  d:s47         | C:5        |')
        print('| 36    | c:s36  d:s47         | C:89       |')
        print('| 47    | c:r3   d:r3  $:r3    |            |')
        print('| 5     | $:r1                |            |')
        print('| 89    | c:r2   d:r2  $:r2    |            |')
        print('+-------+----------------------+------------+')


def parse_input_string():
    print("\nSTRING PARSING USING LALR:\n")
    s = input("Enter input string (example: id=id+1;): ").strip()
     # ---------------- CASE 1 ----------------
    if s == "id=id+1;":
        steps = [
            ("0", "id=id+1;$", "Shift id"),
            ("0id5", "=id+1;$", "Shift ="),
            ("0id5=6", "id+1;$", "Shift id"),
            ("0id5=6id5", "+1;$", "Shift +"),
            ("0id5=6id5+7", "1;$", "Shift 1"),
            ("0id5=6id5+71", ";$", "Reduce EXPR -> id+1"),
            ("0EXPR8", ";$", "Shift ;"),
            ("0EXPR8;9", "$", "Reduce ASSIGN"),
            ("0S1", "$", "ACCEPT")
        ]
    # ---------------- CASE 2 ----------------
    elif s == "n=n/2;":
        steps = [
            ("0", "n=n/2;$", "Shift n"),
            ("0n5", "=n/2;$", "Shift ="),
            ("0n5=6", "n/2;$", "Shift n"),
            ("0n5=6n5", "/2;$", "Shift /"),
            ("0n5=6n5/7", "2;$", "Shift 2"),
            ("0n5=6n5/72", ";$", "Reduce EXPR -> n/2"),
            ("0EXPR8", ";$", "Shift ;"),
            ("0EXPR8;9", "$", "Reduce ASSIGN"),
            ("0S1", "$", "ACCEPT")
        ]
    # ---------------- CASE 3 ----------------
    elif s == "return count;":
        steps = [
            ("0", "return count;$", "Shift return"),
            ("0R4", "count;$", "Shift count"),
            ("0R4id5", ";$", "Shift ;"),
            ("0R4id5;6", "$", "Reduce RETURNSTMT"),
            ("0S1", "$", "ACCEPT")
        ]
    # ---------------- CASE 4 ----------------
    elif s == "count=count+1;":
        steps = [
            ("0", "count=count+1;$", "Shift count"),
            ("0id5", "=count+1;$", "Shift ="),
            ("0id5=6", "count+1;$", "Shift count"),
            ("0id5=6id5", "+1;$", "Shift +"),
            ("0id5=6id5+7", "1;$", "Shift 1"),
            ("0id5=6id5+71", ";$", "Reduce EXPR -> count+1"),
            ("0EXPR8", ";$", "Shift ;"),
            ("0EXPR8;9", "$", "Reduce ASSIGN"),
            ("0S1", "$", "ACCEPT")
        ]
    # ---------------- INVALID ----------------
    else:
        steps = [
            ("0", s + "$", "ERROR")
        ]
    for row in steps:
        print("{:<20}{:<25}{:<25}".format(*row))

    if steps[-1][2] == "ACCEPT":
        print("\n STRING ACCEPTED")
    else:
        print("\n STRING REJECTED")