# =========================================
# MINI COMPILER – FINAL VERSION (AST ADDED)
# =========================================

KEYWORDS = {"int", "float", "if", "else", "while", "for", "return", "void"}

# =========================================
# TABLE PRINT
# =========================================
def print_table(tokens):
    COL_WIDTH = 42
    print("\n+-------------+------------------------------------------+")
    print("| TOKEN NAME  | TOKEN VALUES                             |")
    print("+-------------+------------------------------------------+")

    for name, values in tokens.items():
        values = sorted(values)
        if not values:
            print(f"| {name:<11} | {'':<42} |")
            continue

        line = ""
        first = True
        for v in values:
            if len(line) + len(v) + 2 > COL_WIDTH:
                print(f"| {name:<11} | {line:<42} |" if first else f"| {'':<11} | {line:<42} |")
                first = False
                line = v
            else:
                line = v if not line else line + ", " + v

        print(f"| {name:<11} | {line:<42} |" if first else f"| {'':<11} | {line:<42} |")

    print("+-------------+------------------------------------------+")


# =========================================
# 1️⃣ TOKENIZER
# =========================================
def run_tokenizer():
    tokens = {
        "KEYWORD": set(),
        "IDENTIFIER": set(),
        "INTEGER": set(),
        "FLOAT": set(),
        "OPERATOR": set(),
        "SEPARATOR": set()
    }

    print("\nEnter source code (type 'end' to finish):")

    while True:
        line = input()
        if line.strip() == "end":
            break

        i = 0
        while i < len(line):
            ch = line[i]

            if ch.isspace():
                i += 1

            elif ch.isalpha() or ch == "_":
                start = i
                while i < len(line) and (line[i].isalnum() or line[i] == "_"):
                    i += 1
                word = line[start:i]
                if word in KEYWORDS:
                    tokens["KEYWORD"].add(word)
                else:
                    tokens["IDENTIFIER"].add(word)

            elif ch.isdigit():
                start = i
                dot = 0
                while i < len(line) and (line[i].isdigit() or line[i] == "."):
                    if line[i] == ".":
                        dot += 1
                    i += 1
                num = line[start:i]
                tokens["FLOAT" if dot else "INTEGER"].add(num)

            elif line[i:i+2] in ("==", ">=", "<=", "&&", "||"):
                tokens["OPERATOR"].add(line[i:i+2])
                i += 2

            elif ch in "=+-*/<>":
                tokens["OPERATOR"].add(ch)
                i += 1

            elif ch in ";(),{}[]":
                tokens["SEPARATOR"].add(ch)
                i += 1
            else:
                i += 1

    print_table(tokens)


# =========================================
# AST NODE
# =========================================
class ASTNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# =========================================
# INFIX → POSTFIX
# =========================================
def infix_to_postfix(expr):
    prec = {'+':1, '-':1, '*':2, '/':2}
    stack, postfix = [], []

    for ch in expr:
        if ch.isalnum():
            postfix.append(ch)
        elif ch == '(':
            stack.append(ch)
        elif ch == ')':
            while stack and stack[-1] != '(':
                postfix.append(stack.pop())
            stack.pop()
        elif ch in prec:
            while stack and stack[-1] in prec and prec[stack[-1]] >= prec[ch]:
                postfix.append(stack.pop())
            stack.append(ch)

    while stack:
        postfix.append(stack.pop())

    return postfix


# =========================================
# POSTFIX → AST
# =========================================
def build_ast(postfix):
    st = []
    for tok in postfix:
        if tok.isalnum():
            st.append(ASTNode(tok))
        else:
            r = st.pop()
            l = st.pop()
            st.append(ASTNode(tok, l, r))
    return st[0]


# =========================================
# PRINT AST (CLEAN TREE)
# =========================================
def print_ast(node, prefix="", is_left=True):
    if node:
        print(prefix + ("├── " if is_left else "└── ") + node.val)
        new_prefix = prefix + ("│   " if is_left else "    ")
        print_ast(node.left, new_prefix, True)
        print_ast(node.right, new_prefix, False)


# =========================================
# 2️⃣ SYNTAX TREE (AST)
# =========================================
def run_syntax_tree():
    stmt = input("\nEnter expression (example: a=(f*b)*d/g): ").replace(" ", "")
    if "=" not in stmt:
        print("Invalid input!")
        return

    lhs, expr = stmt.split("=")
    postfix = infix_to_postfix(expr)
    ast = build_ast(postfix)

    print("\nSYNTAX TREE (AST):")
    print("=")
    print_ast(ASTNode(lhs), "", True)
    print_ast(ast, "", False)


# =========================================
# 3️⃣ THREE ADDRESS CODE
# =========================================
def run_three_address_code():
    stmt = input("\nEnter expression (example: a=b+c*(d-e)): ").replace(" ", "")
    if "=" not in stmt:
        print("Invalid input!")
        return

    lhs, expr = stmt.split("=")
    postfix = infix_to_postfix(expr)

    print("\nTHREE ADDRESS CODE:")
    st, temp = [], 1
    for tok in postfix:
        if tok.isalnum():
            st.append(tok)
        else:
            r = st.pop()
            l = st.pop()
            t = f"T{temp}"
            temp += 1
            print(f"{t} = {l} {tok} {r}")
            st.append(t)

    print(f"{lhs} = {st.pop()}")


# =========================================
# MAIN MENU
# =========================================
while True:
    print("\n====== MINI COMPILER MENU ======")
    print("1. Tokenizer")
    print("2. Syntax Tree (AST)")
    print("3. Three Address Code Generator")
    print("4. Exit")

    ch = input("Enter your choice: ")

    if ch == "1":
        run_tokenizer()
    elif ch == "2":
        run_syntax_tree()
    elif ch == "3":
        run_three_address_code()
    elif ch == "4":
        print("Exiting...")
        break
    else:
        print("Invalid choice!")
