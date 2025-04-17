
# funcion para obtener las producciones tipada
def getProductions(listPosibbleProductions: set[str]) -> dict[str, list[str]]:
    numProductions: int = int(input("Ingresa el numero de producciones: "))
    if(numProductions <= 0):
        print("El numero de producciones debe ser mayor a 0")
        return
    
    mapProductions: dict[str, list[str]] = {}

    for i in range(numProductions):
        # tratar el string y obtenerlo
        production: str = input("Ingresa la produccion: ")
        production = production.replace("->", "")
        production = production.split(" ")
        
        # Revisar si la primera produccion es S
        if(i == 0 and production[0] != "S"):
            print("la primera produccion debe ser S")
            return None

        if production[0].islower():
            # Revisar si no es mauscula
            print("El no terminal no puede ser minuscula")
            return None
            
        NonTerminal: str = production[0]
        listPosibbleProductions.remove(NonTerminal)
        
        # uso de [2:] ya que el elemento 1 es el espacio que quedo tras cambiar el -> por un espacio y el 0 es el no terminal
        mapProductions[NonTerminal] = production[2:]  
            
    return mapProductions