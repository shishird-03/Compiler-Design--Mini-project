def generate_cfg():

    grammar = {

    "S":[[
        "DATATYPE","FUNC","LPAR","RPAR",
        "BEGIN","STMTBLOCK","END"
    ]],

    "FUNC":[["MAIN"]],

    "STMTBLOCK":[
        ["STMT","STMTBLOCK"],
        ["Îµ"]
    ],

    "STMT":[
        ["DECL"],
        ["ASSIGN"],
        ["WHILESTMT"],
        ["RETURNSTMT"]
    ],

    "DECL":[
        ["DATATYPE","ID","ASSIGNOP","NUMBER","SEMI"]
    ],

    "ASSIGN":[
        ["ID","ASSIGNOP","EXPR","SEMI"]
    ],

    "EXPR":[
        ["ID","PLUS","NUMBER"],
        ["ID","DIV","NUMBER"],
        ["NUMBER"],
        ["ID"]
    ],
    "WHILESTMT":[[
        "WHILE","LPAR","COND","RPAR",
        "STMTBLOCK",
        "END","WHILE"
    ]],

    "COND":[
        ["ID","GT","NUMBER"]
    ],

    "RETURNSTMT":[
        ["RETURN","ID","SEMI"]
    ]

    }

    return grammar
