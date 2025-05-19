# funcion auxiliar para determinar si es o no termiankl
def isNoTerminal(produccion: str) -> (bool, int):
    if not produccion:  # Si el string está vacío
        return False

    # evitar problemas con cadenas vacias
    # ejm: la cadena "eA" == "A" pero sin eso devolveria que es un no terminal
    # siendo "e" la cadena vacia
    value = -1
    for i in range(0, len(produccion)):
        if produccion[i] != "e":
            value = i
            break
            
    primera = produccion[value]
    return (primera.isupper(), value)
            
def isTerminal(produccion: str) -> bool:
    if produccion.islower() or produccion == "e" or produccion == "$":
        return True
    return False


# literalmente devuelve las posiciones de todos los no terminales en un array sirve para el follow function
def returnAllPositionsOfNoTerminals(Production: str) -> list[int]:
    positions: list[int] = list()
    for i in range(0, len(Production)):
        if Production == "e":
            return []
        # revisa si es terminal
        IsNotTerminal, _ = isNoTerminal(Production[i])
        if IsNotTerminal:
            positions.append(i)

    return positions

def has_left_recursion(productions: dict[str, list[str]]) -> bool:
    for non_terminal, prods in productions.items():
        for prod in prods:
            if prod.startswith(non_terminal):
                return True
    return False

def eliminate_left_recursion_sin_espacios(productions: dict[str, list[str]]) -> dict[str, list[str]]:
    """
    Elimina la recursión izquierda y devuelve producciones sin espacios.
    """
    new_productions = {}
    non_terminals = list(productions.keys())

    for i, A in enumerate(non_terminals):
        current_prods = productions[A]
        new_prods = []
        for prod in current_prods:
            first_symbol = prod.split()[0] if prod else ""
            if first_symbol in non_terminals[:i]:
                for sub_prod in new_productions[first_symbol]:
                    new_prod = sub_prod + "".join(prod.split()[1:]) # Concatenar sin espacios
                    new_prods.append(new_prod.strip())
            else:
                new_prods.append(prod.replace(" ", "")) # Eliminar espacios directamente
        productions[A] = new_prods

        recursive_prods = []
        non_recursive_prods = []

        for prod in productions[A]:
            if prod.startswith(A):
                recursive_prods.append(prod[len(A):])
            else:
                non_recursive_prods.append(prod)

        if not recursive_prods:
            new_productions[A] = productions[A]
        else:
            new_A = A + "'"
            new_productions[A] = [f"{prod}{new_A}" if prod else new_A for prod in non_recursive_prods]
            new_productions[new_A] = [f"{prod}{new_A}" for prod in recursive_prods]
            new_productions[new_A].append("ε")

    return new_productions