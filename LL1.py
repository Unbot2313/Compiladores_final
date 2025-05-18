from first import recursiveFirst
from utils import isTerminal

# obtener la tabla y saber si es ll1
def TableLL1(productions: dict[str, list[str]], firstProductions: dict[str, set[str]], followProductions: dict[str, set[str]]) -> tuple[bool, dict[tuple[str, str], str]]:
    table: dict[tuple[str, str], str] = {}
    isLL1 = True

    # Para cada producción A → α
    for noTerminal, producciones in productions.items():
        for produccion in producciones:
            # Calcula First(α)
            firstAlpha = recursiveFirst(produccion, firstProductions)
            
            # Para cada terminal a en First(α)
            for a in firstAlpha:
                if a != 'e':  # 'e' representa epsilon
                    # Si ya existe una entrada, hay un conflicto (no es LL(1))
                    if (noTerminal, a) in table:
                        isLL1 = False
                        table[(noTerminal, a)] = "conflict"
                    else:
                        table[(noTerminal, a)] = produccion
            
            # Si e está en First(α)
            if 'e' in firstAlpha:
                # Para cada terminal b en Follow(A)
                for b in followProductions[noTerminal]:
                    # Si ya existe una entrada, hay un conflicto (no es LL(1))
                    if (noTerminal, b) in table:
                        isLL1 = False
                        table[(noTerminal, b)] = "conflict"
                    else:
                        table[(noTerminal, b)] = produccion
    
    return (isLL1, table)

def ParsingLL1(table: dict[tuple[str, str], str], simboloInicial: str, inputString: str) -> str:
    stack: list[str] = [simboloInicial, "$"]  # Inicializa la pila con el símbolo inicial y '$'
    input_symbols: list[str] = list(inputString)  # Convierte la cadena en lista
    current_input: str = input_symbols.pop(0) if input_symbols else None  # Primer símbolo

    while stack:
        top_symbol: str = stack[-1]  # Símbolo en la cima de la pila

        if top_symbol == "$":  # Fin de la pila
            if current_input == "$":  # Fin de la entrada
                return "yes"  # Aceptado
            else:
                return "no"  # Rechazado (pila vacía, pero entrada no)

        if current_input is None:
            return "no"  # Rechazado (entrada se agotó antes que la pila)

        if top_symbol == current_input:  # Terminal en la cima coincide
            stack.pop()
            current_input = input_symbols.pop(0) if input_symbols else None # Avanza en la entrada
        elif isTerminal(top_symbol):  # Terminal en la pila no coincide
            return "no"  # Rechazado
        elif (top_symbol, current_input) not in table or table[(top_symbol, current_input)] == "conflict":
            return "no"  # Rechazado (error en la tabla)
        else:  # No terminal en la cima
            production: str = table[(top_symbol, current_input)]
            stack.pop()  # Pop el no terminal
            if production != "e":  # Si no es una producción épsilon
                for symbol in reversed(production):  # Empuja la producción en reversa
                    stack.append(symbol)
    return "no"  # Si la pila se vacía antes, la cadena es rechazada
    