from utils import returnAllPositionsOfNoTerminals
# First de una produccion
from first import recursiveFirst

def getFollowProductions(NormalProductions: dict[str, list[str]], FirstSet: dict[str, set[str]]) -> dict[str, set[str]]:
    # Inicializar todo 
    FollowProductions: dict[str, set[str]] = dict()
    for clave, valor in NormalProductions.items():
        FollowProductions[clave] = set()

    # Primera opcion FOLLOW(S) := {%}
    for clave, valor in NormalProductions.items():
        NewSet = firstOption(clave)
        FollowProductions[clave] = FollowProductions[clave].union(NewSet)

    # Segunda opcion A -> aBC, FIRST(C) - {e} es subcojunto de FOLLOW(B)
    for clave, valor in NormalProductions.items():
        for value in valor:
            allPositionsOfNoTerminals: list[int] = returnAllPositionsOfNoTerminals(value);
            # ESTE SERIA C
            for i in allPositionsOfNoTerminals:
                # el nuevo position es para evitar problemas al partir la cadena
                position = i+1
                # PARTE CON B
                PrimeraParte: str = value[:position]
                # PARTE CON C
                SegundaParte: str = value[position:]
                newSet = SecondOption(SegundaParte, NormalProductions)

                # union con el origen
                NoTerminalSymbol = value[i]
                FollowProductions[NoTerminalSymbol] = FollowProductions[NoTerminalSymbol].union(newSet)
    
    return FollowProductions


def firstOption(Clave: str) -> set[str]:
    if Clave == "S":
        return {"$"}
    return set()

def SecondOption(SegundaParte: str, NormalProductions: dict[str, list[str]]) -> set[str]:
    #optener el first de la segundaParte
    FirstSet = recursiveFirst(SegundaParte, NormalProductions)
    # quitar la cadena vacia
    # Verificar si "e" está en el conjunto antes de eliminarlo
    if "e" in FirstSet:
        FirstSet.remove("e")
        
    # hacer union con el FOLLOW DE B (se hace en la funcion global aca solo la devuelve)
    return FirstSet
