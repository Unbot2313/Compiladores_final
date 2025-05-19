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
    stack: list[str] = [simboloInicial, "$"]
    input_symbols: list[str] = list(inputString) + ["$"]
    current_input: str = input_symbols.pop(0) if input_symbols else "$"

    while stack:
        top_symbol: str = stack[0]
        
        if top_symbol == "$":
            if current_input == "$":
                return "yes"
            else:
                return "no"

        if top_symbol == current_input:
            stack.pop(0)
            current_input = input_symbols.pop(0) if input_symbols else "$"
        elif isTerminal(top_symbol):
            return "no"
        elif (top_symbol, current_input) not in table or table[(top_symbol, current_input)] == "conflict":
            return "no"
        else:
            production: str = table[(top_symbol, current_input)]
            stack.pop(0)
            
            if production != "e":
                for i in range(len(production)-1, -1, -1):
                    stack.insert(0, production[i])
    
    return "no"