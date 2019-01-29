
class Lista():
    def __init__(self, stationList):
        self.lista = []
        self.coste = []
        #La inicializamos de esta forma para poder controlar perfectamente la lista de costes y tenerla ordenada 
        for i in range(len(stationList)+1):
            self.coste.append(0)

    def Add_tupla(self,lista,coste=0):
            seguridad = 0
            auxiliar1 = []
            lista_fin = []
            for i in range(len(lista)):
                auxiliar1.append(lista[i])
            lista_fin.append(coste)
            lista_fin.append(auxiliar1)
            if(RemoveCycles(lista) == False):
                seguridad = EliminarCaminosRedundantes(lista_fin,self.lista,self.coste)
                if(seguridad == 2):
                    self.lista.append(lista_fin)
                    return False
                elif(seguridad == 1):
                    return False
                elif(seguridad == 0):
                    self.lista.append(lista_fin)
                    return True
                
        

    def Borrar(self):
        self.lista = self.lista[1:]

    
    def Add_coste(self,valor, posicion):
        coste = self.coste[posicion]
        coste+=valor
        self.coste.insert(posicion, coste)

    
    def Reordenar(self):
        self.lista.sort()

    def DevolverCabeza(self):
        aux = self.lista[0]
        aux = aux[1]
        return aux

    def Devolver_Valor_Camino(self):
        aux = self.lista[0]
        aux = aux[0]
        return aux
            

    def __str__(self):
        return str(self.lista)

    def ListaVacia(self):
        if(len(self.lista) <=0):
            return True
        else:
            return False

    def GetCoste(self):
        return self.coste

    def GetLista(self):
        return self.lista
    
    def SetLista(self, lista):
        self.lista = lista[:]




def RemoveCycles(lista):
    count = 0
    for i in range(len(lista)):
        aux = lista[i]
        count = 0
        for j in range(len(lista)):
            if(aux ==lista[j]):
                count+=1
            if(count>1):
                return True
    return False

def EliminarCaminosRedundantes(lista_hijos, lista_nodos, lista_costParcial):
    #Devolveremos... 0 -> No han habido coincidencias, 1-> Han habido coincidencias pero los nuevos hijos se quedan fuera, 2-> Han habido coincidencias pero los nuevos hijos entran
    aux = lista_hijos[1] #Guardamos la lista en aux temporalmente
    coste_it = lista_hijos[0] #En coste_it = coste de la iteracion guardamos el valor recien calculado
    for i in range(len(lista_nodos)): #Vamos iterando sobre lista_nodos
        tabla_aux = lista_nodos[i] #Guardamos la iteracion en la que estemos
        tabla_aux = tabla_aux[1] #Definitivamente guardamos solamente la lista de nodos que es lo que realmente interesa para poder comparar
        if(tabla_aux[len(tabla_aux)-1] == aux[len(aux)-1]): #Si los ultimos elementos son iguales comprobamos (Comprobar si solo puede ser en los ultimos elementos)
            if(lista_costParcial[tabla_aux[len(tabla_aux)-1]] > coste_it): #Si el coste de la tabla es mayor debemos intercambiar éste en la tabla y eliminar este camino parcialmente no optimo
                tabla_aux.pop(i) #Eliminamos la posición que interese
                lista_costParcial.insert(aux[len(aux)-1],coste_it) #Cambiamos el elemento en la TPC
                return 2 #Si eliminamos devolvemos True
            else:
                return 1
    return 0
                
            
        
    
    
    
    
