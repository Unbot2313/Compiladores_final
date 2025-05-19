from first import recursiveFirst
from utils import isTerminal
from follow import getFollowProductions

# Representación de un ítem LR(0) como una tupla (noTerminal, producción, posición del punto)
# Ejemplo: ('S', 'AB', 0) representa S -> •AB

def closure(items: list[tuple[str, str, int]], productions: dict[str, list[str]]) -> list[tuple[str, str, int]]:
    """Calcula la cerradura de un conjunto de ítems LR(0)"""
    result = items.copy()
    added = True
    
    while added:
        added = False
        for noTerminal, production, dotPosition in list(result):
            # Si el punto está al final de la producción, no hay nada que hacer
            if dotPosition >= len(production):
                continue
                
            # Símbolo después del punto
            nextSymbol = production[dotPosition]
            
            # Si el símbolo es un no terminal, agregar sus producciones
            if nextSymbol in productions:
                for prod in productions[nextSymbol]:
                    newItem = (nextSymbol, prod, 0)
                    if newItem not in result:
                        result.append(newItem)
                        added = True
    
    return result

def goto(items: list[tuple[str, str, int]], symbol: str, productions: dict[str, list[str]]) -> list[tuple[str, str, int]]:
    """Calcula el estado al que se llega desde un conjunto de ítems al leer un símbolo"""
    nextItems = []
    
    for noTerminal, production, dotPosition in items:
        # Si el punto no está al final y el símbolo después del punto coincide
        if dotPosition < len(production) and production[dotPosition] == symbol:
            nextItems.append((noTerminal, production, dotPosition + 1))
    
    # Calcular cerradura del nuevo conjunto
    return closure(nextItems, productions) if nextItems else []

def constructLR0Automaton(productions: dict[str, list[str]], startSymbol: str) -> tuple[list[list[tuple[str, str, int]]], dict[tuple[int, str], int]]:
    """Construye el autómata LR(0) para una gramática"""
    # Agregar producción inicial aumentada S' -> S
    augmentedProductions = productions.copy()
    startPrime = startSymbol + "'"
    augmentedProductions[startPrime] = [startSymbol]
    
    # Estado inicial es la cerradura de {S' -> •S}
    initialItems = closure([(startPrime, startSymbol, 0)], augmentedProductions)
    
    # Lista de estados y tabla de transiciones
    states = [initialItems]
    transitions = {}  # (estado_origen, símbolo) -> estado_destino
    
    # Procesar estados hasta que no se puedan agregar más
    stateIndex = 0
    while stateIndex < len(states):
        state = states[stateIndex]
        
        # Recolectar todos los símbolos después del punto
        symbols = set()
        for _, production, dotPosition in state:
            if dotPosition < len(production):
                symbols.add(production[dotPosition])
        
        # Para cada símbolo, calcular el estado destino
        for symbol in symbols:
            nextState = goto(state, symbol, augmentedProductions)
            if not nextState:
                continue
                
            # Verificar si el estado ya existe
            if nextState in states:
                destIndex = states.index(nextState)
            else:
                destIndex = len(states)
                states.append(nextState)
            
            # Agregar transición
            transitions[(stateIndex, symbol)] = destIndex
        
        stateIndex += 1
    
    return states, transitions

def buildSLR1Table(productions: dict[str, list[str]], startSymbol: str, followSets: dict[str, set[str]]) -> tuple[bool, dict[tuple[int, str], str]]:
    """Construye la tabla SLR(1) para una gramática"""
    # Construir autómata LR(0)
    states, transitions = constructLR0Automaton(productions, startSymbol)
    
    # Inicializar tabla Action/Goto
    table = {}
    isSLR1 = True
    
    # Estado inicial aumentado
    startPrime = startSymbol + "'"
    
    # Para cada estado
    for stateIndex, state in enumerate(states):
        # Procesar acciones de desplazamiento (shift)
        for (srcState, symbol), destState in transitions.items():
            if srcState == stateIndex:
                if isTerminal(symbol):  # Acción para terminales
                    action = f"s{destState}"  # shift y ir al estado destState
                    
                    # Verificar conflictos
                    if (stateIndex, symbol) in table and table[(stateIndex, symbol)] != action:
                        isSLR1 = False
                        table[(stateIndex, symbol)] = "conflict"
                    else:
                        table[(stateIndex, symbol)] = action
                else:  # Goto para no terminales
                    table[(stateIndex, symbol)] = str(destState)
        
        # Procesar acciones de reducción (reduce)
        for noTerminal, production, dotPosition in state:
            # Si el punto está al final de la producción, es una reducción
            if dotPosition == len(production):
                # Caso especial: aceptación
                if noTerminal == startPrime and production == startSymbol:
                    table[(stateIndex, "$")] = "accept"
                else:
                    # Encontrar el número de producción para la reducción
                    prodIndex = 0
                    for nt, prods in productions.items():
                        if nt == noTerminal:
                            if production in prods:
                                prodIndex = prods.index(production)
                            break
                            
                    # Agregar acciones de reducción para todos los símbolos en Follow(noTerminal)
                    for symbol in followSets[noTerminal]:
                        action = f"r{noTerminal}:{prodIndex}"  # reduce usando producción
                        
                        # Verificar conflictos
                        if (stateIndex, symbol) in table and table[(stateIndex, symbol)] != action:
                            isSLR1 = False
                            table[(stateIndex, symbol)] = "conflict"
                        else:
                            table[(stateIndex, symbol)] = action
    
    return isSLR1, table

def ParsingSLR1(table: dict[tuple[int, str], str], productions: dict[str, list[str]], inputString: str) -> str:
    stateStack = [0]  # Comienza en el estado 0
    symbolStack = ["$"]  # Comienza con $ en la pila de símbolos
    input_symbols = list(inputString) + ["$"]
    current_input = input_symbols[0]
    
    while True:
        currentState = stateStack[-1]
        
        if (currentState, current_input) not in table:
            return "no"
        
        action = table[(currentState, current_input)]
        
        if action == "conflict":
            return "no"
        if action == "accept":
            return "yes"
        
        if action.startswith("s"):
            nextState = int(action[1:])
            stateStack.append(nextState)
            symbolStack.append(current_input)
            input_symbols.pop(0)
            current_input = input_symbols[0] if input_symbols else "$"
        elif action.startswith("r"):
            parts = action[1:].split(":")
            noTerminal = parts[0]
            prodIndex = int(parts[1])
            production = productions[noTerminal][prodIndex]
            
            for _ in range(len(production)):
                stateStack.pop()
                symbolStack.pop()
                
            currentState = stateStack[-1]
            symbolStack.append(noTerminal)
            
            if (currentState, noTerminal) not in table:
                return "no"
                
            nextState = int(table[(currentState, noTerminal)])
            stateStack.append(nextState)
        elif action.isdigit():
            nextState = int(action)
            stateStack.append(nextState)
            symbolStack.append(current_input)
            input_symbols.pop(0)
            current_input = input_symbols[0] if input_symbols else "$"
        else:
            return "no"
    
    return "no"