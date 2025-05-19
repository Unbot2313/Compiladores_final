from utils import isNoTerminal

def getFirst(Productions: dict[str, list[str]]) -> dict[str, set[str]]:
    """
    Calcula el conjunto FIRST para cada no terminal en la gramática.
    """
    firstDict = {key: set() for key in Productions}
    
    # Bandera para verificar si hubo cambios en alguna iteración
    changed = True
    
    # Iterar hasta que no haya cambios
    while changed:
        changed = False
        
        # Para cada producción en la gramática
        for nonTerminal, productions in Productions.items():
            for production in productions:
                # Obtener el FIRST de esta producción particular
                first_set = getFirstOfProduction(production, Productions, firstDict)
                
                # Si agregar este conjunto a FIRST(nonTerminal) cambia algo
                if not first_set.issubset(firstDict[nonTerminal]):
                    firstDict[nonTerminal] = firstDict[nonTerminal].union(first_set)
                    changed = True
    return firstDict

def getFirstOfProduction(production: str, Productions: dict[str, list[str]], firstDict: dict[str, set[str]]) -> set[str]:
    """
    Calcula el conjunto FIRST para una producción específica.
    """
    # Caso base: cadena vacía
    if not production or production == "e":
        return {"e"}
    
    first_set = set()
    
    # Si el primer símbolo es terminal
    if not production[0].isupper() and production[0] != "e":
        return {production[0]}
    
    # Si el primer símbolo es no terminal
    i = 0
    add_epsilon = True
    
    while i < len(production) and add_epsilon:
        symbol = production[i]
        
        # Si el símbolo actual es terminal
        if not symbol.isupper():
            first_set.add(symbol)
            add_epsilon = False
            break
            
        # Si el símbolo actual es no terminal
        if symbol in Productions:
            # Añadir todos los elementos de FIRST(symbol) excepto épsilon
            current_first = firstDict.get(symbol, set())
            first_set = first_set.union(current_first - {"e"})
            
            # Si épsilon no está en FIRST(symbol), no seguimos analizando
            if "e" not in current_first:
                add_epsilon = False
                break
        
        i += 1
    
    # Si todos los símbolos pueden derivar en épsilon, añadir épsilon al resultado
    if add_epsilon:
        first_set.add("e")
            
    return first_set

def getFirstOfNonTerminal(nonTerminal: str, productions: list[str], Productions: dict[str, list[str]]) -> (str, set[str]):
    """
    Calcula el conjunto FIRST para un no terminal específico.
    """
    first_set = set()
    
    for production in productions:
        # Recursivamente calcula el FIRST de cada producción
        current_first = recursiveFirst(production, Productions)
        first_set = first_set.union(current_first)
        
    return (nonTerminal, first_set)

def recursiveFirst(production: str, Productions: dict[str, list[str]]) -> set[str]:
    """
    Calcula recursivamente el conjunto FIRST para una producción.
    Esta función es un enfoque recursivo alternativo.
    """
    # Caso base: cadena vacía
    if not production or production == "e":
        return {"e"}
    
    # Si el primer símbolo es terminal
    if not production[0].isupper() and production[0] != "e":
        return {production[0]}
    
    first_set = set()
    symbol = production[0]
    
    if symbol in Productions:
        all_derive_epsilon = True
        
        for prod in Productions[symbol]:
            # Obtener FIRST del símbolo actual
            symbol_first = recursiveFirst(prod, Productions)
            
            # Añadir todos excepto epsilon
            first_set = first_set.union(symbol_first - {"e"})
            
            # Verificar si este símbolo puede derivar en épsilon
            if "e" not in symbol_first:
                all_derive_epsilon = False
        
        # Si el primer símbolo puede derivar en épsilon, necesitamos FIRST del resto
        if all_derive_epsilon and len(production) > 1:
            rest_first = recursiveFirst(production[1:], Productions)
            first_set = first_set.union(rest_first)
            
        # Si todos los símbolos de la producción pueden derivar en épsilon
        elif all_derive_epsilon:
            first_set.add("e")
    
    return first_set