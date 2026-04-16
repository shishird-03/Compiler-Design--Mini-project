from lexer import tokenize
from cfg import generate_cfg
from first_follow import compute_first, compute_follow
from lalr_parser import run_lalr_parser, parse_input_string
def read_input():
    with open("input.txt") as f:
        return f.read()

program = read_input()
grammar = generate_cfg()
print("\nGENERATED CFG:\n")

for nt in grammar:
    for prod in grammar[nt]:
        print(f"{nt} -> {' '.join(prod)}")

first = compute_first(grammar)
follow = compute_follow(grammar, first, "S")

def print_first_follow_table(first, follow):
    print("\nFIRST AND FOLLOW TABLE:\n")
    print("{:<15}{:<25}{:<25}".format("Non-Terminal", "FIRST", "FOLLOW"))
    print("-" * 70)

    for nt in first:
        print("{:<15}{:<25}{:<25}".format(
            nt,
            str(list(first[nt])),
            str(list(follow[nt]))
        ))

print_first_follow_table(first, follow)
tokens = tokenize(program)
print("\nTOKENS:\n", tokens)
run_lalr_parser()
parse_input_string()