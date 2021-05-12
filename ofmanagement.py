def extract_of(ruta):
    ffoo={}
    with open(ruta,'r') as fichero:
        lineas=fichero.readlines()
        for linea in lineas[1:-1]:
            numeros=linea.split(" = ")
            ffoo[int(numeros[0])]=int(numeros[1][:-2])
    
    return ffoo
