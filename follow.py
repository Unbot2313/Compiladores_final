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

    for clave, valor in NormalProductions.items():
        for value in valor:
            allPositionsOfNoTerminals: list[int] = returnAllPositionsOfNoTerminals(value)
            for i in allPositionsOfNoTerminals:
                position = i + 1
                NoTerminalSymbol = value[i]
                SegundaParte: str = value[position:]
                # Segunda opción
                newSet = SecondOption(SegundaParte, NormalProductions)
                FollowProductions[NoTerminalSymbol] = FollowProductions[NoTerminalSymbol].union(newSet)
                # Tercera opción
                if position == len(value):  # Caso A → αB
                    FollowProductions[NoTerminalSymbol] = FollowProductions[NoTerminalSymbol].union(FollowProductions[clave])
                else:  # Caso A → αBβ
                    Beta = value[position:]
                    FirstBeta = recursiveFirst(Beta, NormalProductions)
                    if "e" in FirstBeta:
                        FollowProductions[NoTerminalSymbol] = FollowProductions[NoTerminalSymbol].union(FollowProductions[clave])
    
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

def thirdOption(value: str, clave: str, FollowProductions: dict[str, set[str]], NormalProductions: dict[str, list[str]]) -> dict[str, set[str]]:
    """
    Implementa la tercera regla de FOLLOW:
    Si A → αB o A → αBβ con ε ∈ FIRST(β), entonces FOLLOW(A) ⊆ FOLLOW(B).
    """
    allPositionsOfNoTerminals: list[int] = returnAllPositionsOfNoTerminals(value)
    for i in allPositionsOfNoTerminals:
        position = i + 1
        NoTerminalSymbol = value[i]

        if position == len(value):  # Caso A → αB (B es el último símbolo)
            FollowProductions[NoTerminalSymbol] = FollowProductions[NoTerminalSymbol].union(FollowProductions[clave])
        else:  # Caso A → αBβ
            Beta = value[position:]
            FirstBeta = recursiveFirst(Beta, NormalProductions)
            if "e" in FirstBeta:
                FirstBeta.remove("e")
                FollowProductions[NoTerminalSymbol] = FollowProductions[NoTerminalSymbol].union(FollowProductions[clave])
            FollowProductions[NoTerminalSymbol] = FollowProductions[NoTerminalSymbol].union(FirstBeta)
    return FollowProductions
