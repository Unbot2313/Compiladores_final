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
        return set()

    if production == "e":
        return {"e"}
    
    terminal, position = isNoTerminal(production)

    if not terminal:
        return {production[position]}

    # contruye el set basado en las producciones del no terminal
    first_set = set()
    for prod in Productions[production[0]]:
        if prod:
            result = recursiveFirst(prod, Productions)
            first_set = first_set.union(result)
    
    return first_set