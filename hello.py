initialState: str = "S"

from productions import getProductions
from first import getFirst
from follow import getFollowProductions
from LL1 import TableLL1, ParsingLL1
        
def main():
    listPosibbleProductions: set[str] = {"A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"}
    Productions: dict[str, list[str]] = getProductions(listPosibbleProductions)
    if(Productions == None):
        return
    print(Productions)

    # get first productions
    FirstProductions: dict[str, set[str]] = getFirst(Productions)
    print(FirstProductions)

    # get follow productions
    FollowProductions: dict[str, set[str]] = getFollowProductions(Productions, FirstProductions)
    print(FollowProductions)

    # saber si es ll1 y la tabla
    IsLL1, tableLL1 = TableLL1(Productions, FirstProductions, FollowProductions)
    if IsLL1:
        print("es LL(1)")
        print("ingresa una cadena a analizar con LL1")
        inputString = input()
        print(ParsingLL1(tableLL1, initialState, inputString))

    else:
        # si no es LL1 la tabla no sirve porque tiene conflictos
        tableLL1 = {}
        print("no es LL(1)")
    

main()