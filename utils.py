# funcion auxiliar para determinar si es o no termiankl
def isNoTerminal(produccion: str) -> bool:
    if not produccion:  # Si el string está vacío
        return False
    primera = produccion[0]
    return primera.isupper()