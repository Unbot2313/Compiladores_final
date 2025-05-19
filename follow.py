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

def isTerminal(symbol: str, productions: dict[str, list[str]]) -> bool:
    """Determina si un símbolo es terminal"""
    return symbol not in productions

def computeFollow(productions: dict[str, list[str]], firstSets: dict[str, set[str]]) -> dict[str, set[str]]:
    followSets = {nt: set() for nt in productions}
    startSymbol = next(iter(productions))
    followSets[startSymbol].add('$')  # S' tiene $

    changed = True
    while changed:
        changed = False
        for nt in productions:
            for prod in productions[nt]:
                for i, symbol in enumerate(prod):
                    if symbol in productions:  # Es no terminal
                        # Caso 1: A → αBβ => Follow(B) += First(β)
                        if i + 1 < len(prod):
                            nextSymbol = prod[i + 1]
                            if isTerminal(nextSymbol, productions):
                                # Si el siguiente símbolo es terminal, lo añadimos directamente
                                if nextSymbol not in followSets[symbol]:
                                    followSets[symbol].add(nextSymbol)
                                    changed = True
                            else:
                                # Si es no terminal, añadimos su First (excepto ε)
                                for s in firstSets[nextSymbol]:
                                    if s != 'ε' and s not in followSets[symbol]:
                                        followSets[symbol].add(s)
                                        changed = True
                        # Caso 2: A → αB o A → αBβ donde β =>* ε => Follow(B) += Follow(A)
                        if i + 1 >= len(prod) or all(
                            s in productions and 'ε' in productions[s] 
                            for s in prod[i + 1:]
                        ):
                            for s in followSets[nt]:
                                if s not in followSets[symbol]:
                                    followSets[symbol].add(s)
                                    changed = True
    return followSets