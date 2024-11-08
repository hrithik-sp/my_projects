import ply.lex as lex
import ply.yacc as yacc

# Tokens
tokens = (
    'IF', 'ELSE', 'FOR', 'IN', 'RANGE',
    'SWITCH', 'CASE', 'BREAK', 'DEF', 'GT',
    'LT', 'EQ', 'COMMA', 'RETURN', 'LPAREN',
    'RPAREN', 'LBRACE', 'RBRACE', 'COLON',
    'SEMICOLON', 'EQUALS', 'NUMBER', 'STRING',
    'BOOLEAN', 'INCREMENT', 'IDENTIFIER',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE'
)

# Reserved words
reserved = {
    'if': 'IF', 'else': 'ELSE', 'for': 'FOR',
    'in': 'IN', 'range': 'RANGE', 'switch': 'SWITCH', 'case': 'CASE',
    'return': 'RETURN', 'true': 'BOOLEAN', 'false': 'BOOLEAN',
    'break': 'BREAK', 'def': 'DEF'
}

# Lexer definitions
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COLON = r':'
t_GT = r'>'
t_COMMA = r','
t_EQUALS = r'='
t_STRING = r'\"[^"]*\"'
t_INCREMENT = r'\+\+'
t_LT = r'<'
t_EQ = r'=='
t_SEMICOLON = r';'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_error(t):
    print(f"Illegal character: '{t.value[0]}' at line {t.lexer.lineno}")
    t.lexer.skip(1)

# Precedence rules for operators
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'GT', 'LT', 'EQ'),
)

# Parsing rules
def p_program(p):
    '''program : statement_list'''
    p[0] = p[1]

def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_statement(p):
    '''statement : if_statement
                | for_statement
                | switch_statement
                | function_def
                | assignment_statement
                | return_statement
                | function_call
                | block'''
    p[0] = p[1]

def p_if_statement(p):
    '''if_statement : IF LPAREN condition RPAREN block
                    | IF LPAREN condition RPAREN block ELSE block'''
    if len(p) == 6:
        p[0] = ('if', p[3], p[5], None)
    else:
        p[0] = ('if', p[3], p[5], p[7])

def p_for_statement(p):
    '''for_statement : FOR IDENTIFIER IN RANGE LPAREN NUMBER RPAREN block'''
    p[0] = ('for', p[2], ('range', p[6]), p[8])

def p_switch_statement(p):
    '''switch_statement : SWITCH LPAREN expression RPAREN LBRACE case_list RBRACE'''
    p[0] = ('switch', p[3], p[6])

def p_case_list(p):
    '''case_list : case
                | case_list case'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_case(p):
    '''case : CASE expression COLON statement_list BREAK SEMICOLON'''
    p[0] = ('case', p[2], p[4])

def p_function_def(p):
    '''function_def : DEF IDENTIFIER LPAREN RPAREN COLON statement'''
    p[0] = ('function_def', p[2], [], p[6])

def p_return_statement(p):
    '''return_statement : RETURN expression SEMICOLON'''
    p[0] = ('return', p[2])

def p_block(p):
    '''block : LBRACE statement_list RBRACE
            | LBRACE RBRACE'''
    if len(p) == 4:
        p[0] = ('block', p[2])
    else:
        p[0] = ('block', [])

def p_function_call(p):
    '''function_call : IDENTIFIER LPAREN argument_list RPAREN SEMICOLON'''
    p[0] = ('function_call', p[1], p[3])

def p_argument_list(p):
    '''argument_list : expression
                    | expression COMMA argument_list
                    | empty'''
    if len(p) == 2:
        if p[1] is None:
            p[0] = []
        else:
            p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_condition(p):
    '''condition : expression GT expression
                | expression LT expression
                | expression EQ expression'''
    p[0] = ('condition', p[2], p[1], p[3])

def p_assignment_statement(p):
    '''assignment_statement : IDENTIFIER EQUALS expression SEMICOLON'''
    p[0] = ('assignment', p[1], p[3])

def p_expression(p):
    '''expression : IDENTIFIER
                | NUMBER
                | STRING
                | BOOLEAN
                | expression PLUS expression
                | expression MINUS expression
                | expression TIMES expression
                | expression DIVIDE expression'''
    if len(p) == 2:
        p[0] = ('expression', p[1])
    else:
        p[0] = ('expression', p[2], p[1], p[3])

def p_empty(p):
    'empty :'
    p[0] = []

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}' (line {p.lexer.lineno})")
    else:
        print("Syntax error at EOF")

# Build lexer and parser
lexer = lex.lex()
parser = yacc.yacc()

# Test cases with arithmetic expression included
test_cases = [
    """for i in range(10){ 
    break; 
    } 
    """,
    """if (x < y) { 
    something(); 
    } else { 
    something_else(); 
    }""",
    """switch (x) { 
    case 1:  
    something();  
    break; 
    case 2:  
    something_else();  
    break; 
    }""",
    """def function(): 
    return 0;""",
    """x = 5 + 3 * (10 - 4);"""
]

# Parser test function
def test_parser():
    for test in test_cases:
        print(f"\nParsing:\n{test}")
        try:
            result = parser.parse(test)
            print("Parse successful!")
        except Exception as e:
            print(f"Parse failed: {str(e)}")

# Main execution
if __name__ == "__main__":
    test_parser()
