--- This is a custom programming language parser written in Python using the PLY (Python Lex-Yacc) library. ---

What does it do?
This script:

- Defines a grammar and lexer for a simplified programming language.

- Parses code snippets written in that language to check for syntax correctness and to produce an Abstract Syntax Tree (AST)-like structure.


Components Breakdown:
1. Lexical Analysis (lex)
- This section tokenizes the input string — it breaks source code into tokens such as:

- Keywords (if, else, for, switch, def, etc.)

- Operators (+, -, ==, =, etc.)

- Punctuation ({, }, ;, etc.)

- Identifiers, numbers, strings, booleans


2. Parsing Rules (yacc)
- These rules define how tokens combine to form valid statements and blocks. This is the "grammar" of the language.


3. AST Generation
- Each rule returns a tuple or list describing the parsed structure.


What Can It Parse?
It currently supports:

- if-else conditions

- for loops with range

- switch-case-break blocks


Use Case
This is useful for:

- Building a custom interpreted language

- Teaching compiler construction or interpreters

- Understanding parsing techniques with Python



- Function definitions and returns

- Arithmetic and logical expressions

- Variable assignments

- Function calls
