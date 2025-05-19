initialState: str = "S"

from productions import getProductions
from first import getFirst
from follow import getFollowProductions
from LL1 import TableLL1, ParsingLL1
from SLR1 import buildSLR1Table, ParsingSLR1
        
def main():
    listPosibbleProductions: set[str] = {"A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"}
    Productions: dict[str, list[str]] = getProductions(listPosibbleProductions)
    if(Productions == None):
        return

    # get first productions
    FirstProductions: dict[str, set[str]] = getFirst(Productions)

    # get follow productions
    FollowProductions: dict[str, set[str]] = getFollowProductions(Productions, FirstProductions)

    # Verificar si la gramática es LL(1) y obtener la tabla
    IsLL1, tableLL1 = TableLL1(Productions, FirstProductions, FollowProductions)
    
    # Verificar si la gramática es SLR(1) y obtener la tabla
    IsSLR1, tableSLR1 = buildSLR1Table(Productions, initialState, FollowProductions)
    
    # Informar al usuario sobre los tipos de gramática
    if IsLL1 and IsSLR1:
        print("La gramática es LL(1) y SLR(1)")
    elif IsLL1:
        print("La gramática es LL(1) pero no es SLR(1)")
    elif IsSLR1:
        print("La gramática es SLR(1) pero no es LL(1)")
    else:
        print("La gramática no es ni LL(1) ni SLR(1)")
    
    # Preguntar qué parser usar si al menos uno está disponible
    if IsLL1 or IsSLR1:
        print("\nSeleccione qué parser desea utilizar:")
        if IsLL1:
            print("1. Parser LL(1)")
        if IsSLR1:
            print("2. Parser SLR(1)")
        
        choice = input("Ingrese el número del parser deseado: ")
        
        if choice == "1" and IsLL1:
            print("Ha seleccionado el parser LL(1)")
            print("Ingresa exit para salir")
            while True:
                inputString = input("Ingrese una cadena a analizar con LL(1): ")
                if inputString.lower() == "exit":
                    break
                result = ParsingLL1(tableLL1, Productions, inputString)
                print(result)
        elif choice == "2" and IsSLR1:
            print("Ha seleccionado el parser SLR(1)")
            print("Ingresa exit para salir")
            while True:
                inputString = input("Ingrese una cadena a analizar con SLR(1): ")
                if inputString.lower() == "exit":
                    break
                result = ParsingSLR1(tableSLR1, Productions, inputString)
                print(result)

        else:
            print("Selección inválida o el parser seleccionado no está disponible para esta gramática")
    else:
        print("No hay parsers disponibles para esta gramática debido a los conflictos")

main()