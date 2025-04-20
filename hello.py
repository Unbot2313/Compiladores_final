initialState: str = "S"

from productions import getProductions
from first import getFirst
from follow import getFollowProductions
        
def main():
    listPosibbleProductions: set[str] = {"A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"}
    Productions: dict[str, list[str]] = getProductions(listPosibbleProductions)
    if(Productions == None):
        return
    print(Productions)
    FirstProductions: dict[str, set[str]] = getFirst(Productions)
    print(FirstProductions)
    FollowProductions: dict[str, set[str]] = getFollowProductions(Productions, FirstProductions)
    print(FollowProductions)

main()