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