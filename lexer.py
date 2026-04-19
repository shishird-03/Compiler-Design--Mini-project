import re
def tokenize(code):
    keywords = {
        "int": "DATATYPE",
        "char": "DATATYPE",
        "main": "MAIN",
        "while": "WHILE",
        "begin": "BEGIN",
        "end": "END",
        "return": "RETURN"
    }
    symbols = {
        "(": "LPAR",
        ")": "RPAR",
        ";": "SEMI",
        "+": "PLUS",
        "-": "MINUS",
        "/": "DIV",
        "=": "ASSIGNOP",
        ">": "GT"
    }
    tokens = []
    lines = code.split("\n")
    print("\nTOKENS GENERATED:\n")
    for line_no, line in enumerate(lines, start=1):
        # Updated regex to include all operators
        words = re.findall(r'\w+|[()=;+\-/>]', line)
        col = 1
        for word in words:

            if word in keywords:
                token = keywords[word]

            elif word in symbols:
                token = symbols[word]

            elif word.isdigit():
                token = "NUMBER"

            else:
                token = "ID"

            print(f"Token('{token}','{word}',{line_no},{col})")

            tokens.append(token)

            col += len(word)
    return tokens