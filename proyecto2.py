# Universidsad Metropolitana
# Departamento de Ingeniería de Sistemas
# Modelación de Sistemas en Redes
# Prof. Rafael Matienzo

# Proyecto 2 - Ruta Crítica.

# Grupo E.
# Integrantes: 
#   - Miguel Jaimes
#   - Valeria Madio
#   - Gilberto Pucciarelli 
#   - Vito Tatoli
#   - Luis Torres


opcional = {
    "A": [0,[],2,0,0,0,0,False,[],"Quitar cerámicas"],
    "B": [1,["A"],3,0,0,0,0,False,[],"Instalar cableado"],
    "C": [2,["B","E"],1,0,0,0,0,False,[],"Instalar calentador"],
    "D": [3,["E"],3,0,0,0,0,False,[],"Instalar bomba"],
    "E": [4,["A"],2,0,0,0,0,False,[],"Instalar Tuberías"],
    "F": [5,["C","D"],2,0,0,0,0,False,[],"Instalar Jacuzzi"],
    "G": [6,["F"],2,0,0,0,0,False,[],"Pruebas y Ajustes"]
}

id_Ops={
    "A": 0,
    "B": 1,
    "C": 2,
    "D": 3,
    "E": 4,
    "F": 5,
    "G": 6
}

datos={}

ids = {}


def armar_Matriz_Ady(grafo):
    #Por cada elemento del datos se buscan los predecesores
    for key in datos:
        for pre in datos[key][1]:
            #En la fila de cada predecesor se agrega un 1 en la columna del nodo actual
            grafo[datos[pre][0]][datos[key][0]]=1
    return grafo


def primerNodo():
    for key in datos:
        #El elemento que no pesea predecesores
        if len(datos[key][1])==0:
            return key


def ultimoNodo(grafo):
    #Se busca en la matriz de adyacencia la fila que contenga solo 0's
    for i in range(0, len(grafo)):
        sum=0
        for j in range(0, len(grafo[i])):
            if grafo[i][j]==1:
                sum=sum+1
        
        if sum==0:  #El elemento que no posea destinos en la matriz de adyacencia
            return i


def forward_Pass(grafo, start, end):
    #Se aplica BFS
    print("Se aplica BFS para recorrer el grafo y modificar los valores de Early Start y Early Finish")
    queue=[]
    queue.append(start)
    datos[start][4]=datos[start][2]
    datos[start][7]=True
    print("Cola: ",queue)
    while len(queue)!=0:
        #Se verifica si tiene predecesores
        if len(datos[queue[0]][1])!=0:
            max=0
            #Se usa como Early start el Early finish mayor de sus predecesores
            for predecesor in datos[queue[0]][1] :
                if datos[predecesor][4]>max:
                    max=datos[predecesor][4]
            datos[queue[0]][3]=max
            datos[queue[0]][4]=datos[queue[0]][2]+max
        #Se saca de la cola el primer elemento
        aux=datos[queue.pop(0)][0]
        #Se buscan los sucesores del primer elemento de la cola
        for i in range(0,len(grafo[aux])) :
            if grafo[aux][i] == 1 :
                datos[ids[i]][7]=True
                queue.append(ids[i])
        print("Cola: ",queue)


def backward_Pass(grafo, start,end):
    print("Se aplica BFS para recorrer el grafo y modificar los valores de Late Start y Late Finish")
    #Se aplica BFS
    queue=[]
    queue.append(end)
    datos[end][6]=datos[end][4]
    datos[end][5]=datos[end][3]
    datos[end][7]=False
    print("Cola: ",queue)
    while len(queue)!=0:
        #Se saca el primer elemto de la cola
        aux=datos[queue.pop(0)][0]
        min=9999    #Valor muy grande para hallar min
        #Se buscan los sucesores en la matriz de adyacencia
        for i in range(0, len(grafo[aux])):
            if grafo[aux][i] ==1:
                if datos[ids[i]][5]<min:
                    #De los sucesores se guarda el late start minimo
                    min=datos[ids[i]][5]
                datos[ids[aux]][6]= min
                datos[ids[aux]][5]= min-datos[ids[aux]][2]

        #Se buscan los predecesores
        for predecesor in datos[ids[aux]][1]:
            #Se verifica si fue visitado
                queue.append(predecesor)
        print("Cola: ",queue)            


def mostrarDatos(Pass):
    print("Tabla resultante del "+Pass+ " Pass")
    print("|NODO|  ES  |  EF  |  LS  |  LF  |")
    for key in datos:
        line="| "+key+"  "
        for i in range(3,7):
            line=line+"| "
            if datos[key][i]<10:
                line=line+" "+str(datos[key][i])+"   "
            else:
                line=line+" "+str(datos[key][i]) +"  "   
        line=line+"| "
        print(line)

def mostrarMatrizAdy(grafo):
    print("   A- B- C- D- E- F- G")
    for fila in range(0,len(grafo)):
        print(ids[fila], grafo[fila])

def rutaCritica(graph, start, end):

    ady = graph.copy()
    node = end
    ruta = []
    camino = ''
    tiempo = 0
    
    print("\n\nRuta Crítica: \n")
    
    while node != start:
        for key, value in datos.items():
            if key == node:
                ruta.append(key)
                tiempo += datos[key][2]
                for i in range(len(datos[key][1])):
                    pre = datos[key][1][i]
                    holgura = datos[pre][6] - datos[pre][4]
                    if holgura == 0:
                        node = pre
    tiempo += datos[node][2]
    ruta.append(start)
    ruta.reverse()
    
    for i in range(len(ruta)):
        camino = camino + str(ruta[i])
        if i != (len(ruta) - 1):
            camino = camino + ' - '
    #print(camino)
    line=""
    for i in range(0,len(ruta)):
        line=str(i)+") Actividad: "+ruta[i]+ " | Descripcion: "+datos[ruta[i]][9]
        print(line)
    
    print("\n Tiempo que toma la ruta critica: {} \n".format(tiempo))


def holguraCaminos(start, end):

    print("\nID --- Holgura")
    for key, value in datos.items():
        holgura = datos[key][6] - datos[key][4]
        print(' {} ---    {}   '.format(key, holgura))


def wait():
    print("\n")
    print("Presione enter para continuar")
    input()

def armar_grafo_Usuario():
    diccionario=datos
    keys=ids
    num=None
    while num==None :
        user_input = input("Ingrese cantidad de actividades(>1) \n")
        try:
            num = int(user_input)
            if num<=1:
                num=None
                print("Cantidad <=1")
            else:
                print("La Cantidad ingresada es: ", num)
                print("\n")
        except ValueError:
            print("Error: Ingrese un numero\n")
            num=None

    for cantidad in range(0,num):
        nodo=[0,[],0,0,0,0,0,False,[],""]
        print("Nodo # ", cantidad)
        name=pedir_Nombre()
        while name in diccionario:
            print("Este nombre ya esta Existe, ingrese uno nuevo")
            name=pedir_Nombre()       
        duracion=pedir_Duracion()
        des=pedir_Descripcion()
        nodo[2]=duracion
        nodo[0]=cantidad
        nodo[9]=des
        diccionario[name]=nodo
        keys[cantidad]=name
        
            
    print("Ingrese nodo de Inicio")
    start=""
    while start not in diccionario:
        start=pedir_Nombre()
        if start not in diccionario:
            print("El nodo ingresado no existe")

    print("Ingrese nodo Final")
    end=pedir_Nombre()
    while end not in diccionario or end==start:
        if end not in diccionario:
            print("El nodo ingresado no existe")
        if end ==start:
            print("El nodo final debe ser diferente al inicial")
        end=pedir_Nombre()
    ordenarPrelaciones()
    pedir_Prelaciones(diccionario,start,end)

def pedir_Duracion():
    num=None
    while num==None :
        user_input = input("Ingrese tiempo de duracion (>0) \n")
        try:
            num = int(user_input)
            if num<1:
                num=None
                print("Error: Tiempo <1")
            else:
                print("El tiempo ingresado es: ", num)
        except ValueError:
            print("Error: Ingrese un numero\n")
            num=None
    print("\n")
    return num

def pedir_Nombre():
    name=None
    while name==None :
        user_input = input("Ingrese Nombre del nodo\n")
        name=user_input
        if name=="":
            print("No ingreso nada")
    print("\n")
    return name

def pedir_Descripcion():
    descripcion=None
    while descripcion==None :
        user_input = input("Ingrese Descripcion de la actividad\n")
        descripcion=user_input
        if descripcion=="":
            print("No ingreso nada")
    print("\n")
    return descripcion


def pedir_Prelaciones(diccionario,start,end):
    queue=[]
    queue.append(end)
    print("Cola:",queue)
    while len(queue)!=0:
        num=None
        while num==None :
            user_input = input("Cantidad de prelaciones que posee el nodo: ["+ queue[0]+"]\n")
            try:
                num = int(user_input)
                if num<1:
                    num=None
                    print("Cantidad de prelaciones <1")
                else:
                    print("Cantidad de prelaciones  es: ", num)
                    print("\n")
            except ValueError:
                print("Error: Ingrese un numero\n")
                num=None
        
        print("Prelaciones del nodo",queue[0])
        for x in range(0,num):
            name=verificar_prelacion(diccionario,start)
            if name!=start and (name not in queue):
                diccionario[queue[0]][1].append(name)
                if name not in diccionario[name][8]:
                    diccionario[name][8].append(queue[0])
                    
                if len(diccionario[name][1])==0:
                    queue.append(name)
            else:
                diccionario[queue[0]][1].append(name)
        queue.pop(0)
        print("Cola:",queue)


def verificar_prelacion(diccionario, start):
    name=None
    while name==None:
        name=pedir_Nombre()
        existe=False
        if name not in diccionario:
            name=None
            print("El nodo que ingreso no existe")    
    return name

def ordenarPrelaciones():
    for key in datos:
        sorted(datos[key][1], key=str.lower)


def main():  
    graph=[]
    #Llenar matriz de adyacencia con 0's
    respuesta = None
    while respuesta == None:
        try:
            respuesta = int(input(
            '''Quiere Armar el grafo manual o usar el modelo aplicado en el parcial 2
                1- Manual
                2- Modelo Ejemplo
            '''))
        except:
            print("No coloco una opción válida")
            respuesta= None
    
    if respuesta==1:
        armar_grafo_Usuario()
    else:
        for key in opcional:
            datos[key]=opcional[key]
            ids[opcional[key][0]]=key

    for key in datos:
        row=[]
        for i in range(0, len(datos)):
            row.append(0)
        graph.append(row)
    
    print("Datos Iniciales:\n")
    for key in datos:
        print(key+":",datos[key])
    print("\n")

    print("Matriz de adyacencia: \n")
    graph=armar_Matriz_Ady(graph)
    mostrarMatrizAdy(graph)
    start=primerNodo()
    end=ids[ultimoNodo(graph)]
    wait()

    print("\n")
    print("-----Forward Pass-----")
    print("Nodo de Inicio: "+start)
    print("Nodo Final: "+ end)
    print("\n")
    forward_Pass(graph, start, end)
    print("\n")
    
    mostrarDatos("Forward")
    wait()

    print("\n")
    print("-----Backward Pass-----")
    print("Nodo de Inicio: "+end)
    print("Nodo Final: "+ start)
    print("\n")
    backward_Pass(graph,start,end)
    print("\n")
    
    mostrarDatos("Backward")
    wait()

    rutaCritica(graph, start, end)
    print("\nHolguras ")
    holguraCaminos(start, end)


if __name__ == "__main__":
    main()