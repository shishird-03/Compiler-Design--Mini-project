def compute_first(grammar):
    first = {nt: set() for nt in grammar}
    changed = True
    while changed:
        changed = False

        for nt in grammar:

            for production in grammar[nt]:

                for symbol in production:

                    if symbol == "Îµ":

                        if "Îµ" not in first[nt]:

                            first[nt].add("Îµ")

                            changed = True

                        break
                    elif symbol not in grammar:

                        if symbol not in first[nt]:

                            first[nt].add(symbol)

                            changed = True
                        break
                    else:

                        before = len(first[nt])

                        first[nt].update(first[symbol] - {"Îµ"})

                        if "Îµ" not in first[symbol]:

                            break

                        if len(first[nt]) > before:

                            changed = True
    return first

def compute_follow(grammar, first, start_symbol):

    follow = {nt: set() for nt in grammar}

    follow[start_symbol].add("$")

    changed = True

    while changed:

        changed = False

        for lhs in grammar:

            for production in grammar[lhs]:

                trailer = follow[lhs].copy()

                for symbol in reversed(production):

                    if symbol in grammar:

                        before = len(follow[symbol])

                        follow[symbol].update(trailer)

                        if "Îµ" in first[symbol]:

                            trailer = trailer.union(first[symbol] - {"Îµ"})

                        else:

                            trailer = first[symbol]

                        if len(follow[symbol]) > before:

                            changed = True

                    else:

                        trailer = {symbol}

    return follow
