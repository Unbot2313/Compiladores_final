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


    