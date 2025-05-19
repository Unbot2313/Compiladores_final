from utils import isNoTerminal

# funciones para obtener los firts de cada Produccion
def getFirst(Productions: dict[str, list[str]]) -> dict[str, set[str]]:
    firstDict: dict[str, set[str]] = dict()
    #inicializar
    for clave, valor in Productions.items():
        firstDict[clave] = set()

    for clave, valor in Productions.items():
        clave, valor = getFirstOfNonTerminal(clave, valor, Productions)
        firstDict[clave] = firstDict[clave].union(valor)
    return firstDict

def getFirstOfNonTerminal(clave: str, listOfProductions: list[str], Productions: dict[str, list[str]]) -> (str, set[str]):
    firstList: set[str] = set()
    for production in listOfProductions:
        value_set = recursiveFirst(production, Productions)
        firstList = firstList.union(value_set)
    return (clave, firstList)

# funcion para obtener el first
def recursiveFirst(production: str, Productions: dict[str, list[str]]) -> set[str]:
    if not production:
        return {"e"}  # La cadena vacía produce la cadena vacía

    if production == "e":
        return {"e"}
    
    # Si el primer símbolo es terminal, ese es el FIRST
    first_char = production[0]
    if not first_char.isupper() and first_char != "e":
        return {first_char}
    
    # Si el primer símbolo es no terminal, calculamos su FIRST
    first_set = set()
    if first_char in Productions:
        for prod in Productions[first_char]:
            # Evitar la recursividad infinita si el primer símbolo se repite
            if prod and (prod[0] != first_char):
                result = recursiveFirst(prod, Productions)
                first_set = first_set.union(result)
            # Si la producción deriva la cadena vacía o comienza con el mismo símbolo
            elif not prod or prod == "e":
                first_set.add("e")
            elif len(prod) > 1 and prod[0] == first_char:
                # Para manejar recursión a la izquierda como en S -> S+T
                # Agregamos FIRST del resto de la producción (sin la S inicial)
                rest_first = recursiveFirst(prod[1:], Productions)
                first_set = first_set.union(rest_first)
            # En caso de recurrir en sí mismo directamente como S -> S
            elif prod == first_char:
                pass  # Evitar bucle infinito
                
        # Si hay más símbolos después del primer no terminal
        if len(production) > 1:
            # Si el FIRST del primer símbolo contiene épsilon
            if "e" in first_set:
                first_set.remove("e")
                # Añadir el FIRST del resto de la producción
                rest_first = recursiveFirst(production[1:], Productions)
                first_set = first_set.union(rest_first)
                
    return first_set