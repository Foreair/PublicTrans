# _________________________________________________________________________________________
# Intel.ligencia Artificial 
# Grau en Enginyeria Informatica
# Curs 2013 - 2014
# Universitat Autonoma de Barcelona
# _________________________________________________________________________________________

from MapaMetro import *
from math import *
from Lista import *


# AstarAlgirthm: main function. It is the connection between the GUI and the AStar search code.
#       INPUTS:
#           - stationList: list de objetos de statioList of a city. (- id, name, line, x, y -)
#           - connections: Dictionary set of possible connections between the stations. 
#           - coord_origin: list of two values referring to the origin coordinates
#           - coord_destination: list of two values referring to the destination coordinates 
#           - typePreference: Value to indicate the preference selected: 0 - minimum Distance | 1- minimum Stops | 2- minimum Time | 3 - minimum Connections
#           - timeConnections: Dictionary including the time of connections between two different lines in a certain station 
#           - timeStation: Dictionary including the time of connections between two different stations.
#       OUTPUTS:
#           - time: required time to make the route#           - distance: total distance made in the route
#           - connections: total connections between different lines in the route
#           - stopStations: total stops made in the route
#           - expandedNodes: total expanded nodes to get the optimal path
#           - expandedList:  list of the expanded nodes to get the optimal path
#           - idCamins: List of the Station IDs of the optimal Path
#           - min_distance_origin: the distance of the origin_coordinates to the closest station 
#           - min_distance_destination: the distance of the destination_coordinates to the closest station
def AstarAlgorithm(stationList, connections,coord_origin,coord_destination,typePreference, timeConnections, timeStation):
        lista_heu = [] #Lista donde guardaremos todas las heuristicas desde cualquier punto al destino elegido por el usuario
        lista_aux = []
        lista_exp = []
        
        expandedNodes = 1 #Lo inicializamos a 1 ya que el origen no lo vamos a sumar en ningun momento ya lo ponemos aqui
        lista_nodos_expandidos = []
        x_ori, y_ori = coord_origin
        x_dest, y_dest = coord_destination
        time = 0
        transbordos_total = 0
        distancia_total = 0

        #Si las estaciones son las mismas lanzamos error (Cambiarlo si queremos)
        if(x_ori == x_dest and y_ori == y_dest):
            raise ValueError
        nombre_ori, id_ori, linea_ori, nombre_dest, id_dest, linea_dest = BuscarOriDest(x_ori,y_ori,x_dest,y_dest, stationList)
        """-------------------------Una vez realizado este bucle ya tendremos nuestro origen y destino-----------------------"""
        #Aqui calculamos la tabla de heuristicas y la tabla de costes viene dada en el diccionario por lo tanto ya podemos aplicar A*
#        for i in range(len(stationList)+1):
        for i in stationList:
            if(typePreference == '0'):      #Minimum Distance
                    lista_heu.append(DistEuclidea(i.Get_x(), i.Get_y(), x_dest, y_dest))
            elif(typePreference == '1'):    #Minimum Stops
                    lista_heu.append(0)
            elif(typePreference == '2'):    #Minimum Time
                    lista_heu.append(h_tiempo(i.Get_x(), i.Get_y(), x_dest, y_dest))
            elif(typePreference == '3'):    #Minimum Connections
                    lista_heu.append(0)
#                j = -1
#                if(j!=-1):
#                        lista_heu.append(h_tiempo(stationList[j].Get_x(), stationList[i].Get_y(), x_dest, y_dest))
#                else:
#                        lista_heu.append(0)
#                j+=1
                
        lista_nodos_expandidos.append(id_ori)
        lista = Lista(stationList) #Usamos la clase creada anteriormente para poder usar sus funciones 
        lista_aux.append(id_ori)
        lista.Add_tupla(lista_aux) #Anyadimos el nodo padre a la lista con un coste de 0 ya que es desde donde comenzamos
        cap = lista.DevolverCabeza()
        
        while((cap[len(cap)-1] != id_dest) and (lista.ListaVacia() == False)):
                """print lista, '\n', '\n'
                print lista.GetCoste(), '\n', '\n'"""
                lista_exp = Expandir(connections,cap)
                lista.Borrar()
                for i in range(len(lista_exp)):
                    aux = cap[:] #Hacemos una copia del cap
                    aux.append(lista_exp[i]) #A esa copia le añadimos uno de los hijos
#                    aux.append(list(lista_exp)) #A esa copia le añadimos uno de los hijos

                    #print cap[len(cap)-1], '\n'
                    coste,heuristica, trans = CalcularCostesHeuristicas(lista_heu, timeStation,timeConnections, cap[len(cap)-1], lista_exp[i], lista, lista.GetCoste()) #Calcula los costes y las heuristicas
                    transbordos_total +=trans
                    coste_auxiliar = coste
                    if(lista.Add_tupla(aux,heuristica)==True): #Hay que controlar que no se metan valores en la tabla sin tener sentido
                            expandedNodes+=1
                            lista.Add_coste(coste,cap[len(cap)-1])#lista_exp[i]
                            lista_nodos_expandidos.append(lista_exp[i])
                    lista.Reordenar()
                cap = lista.DevolverCabeza()
        idCamins = lista.DevolverCabeza()
        #idCamins.reverse()
        #Asociamos la tabla de costes a la variable tabla_costes
        tabla_costes = lista.GetCoste()
        for i in range(len(idCamins)):
                #Recorremos toda la tabla y vamos sumando los valores correspondientes para poder devolverlos
                time += tabla_costes[idCamins[i]]
        min_distance_origin = connections[id_ori].keys()
        min_distance_destination = connections [id_dest].keys()
        for i in range(len(idCamins)//2):
                aux = stationList[idCamins[i]]
                aux1 = stationList[idCamins[i+1]]
                x1_aux = aux.Get_x()
                y1_aux = aux.Get_y()
                x2_aux = aux1.Get_x()
                y2_aux = aux1.Get_y()
                distancia_total+=DistEuclidea(x1_aux, x2_aux,y1_aux, y2_aux)
        stopStations = len(idCamins)
        idCamins.reverse()
        nodos_hijos = idCamins[:]
        idCamins.reverse()
        return time, distancia_total, transbordos_total, stopStations, expandedNodes,nodos_hijos, idCamins, min_distance_origin, min_distance_destination, len(idCamins)
#Funciones Get_id, Get_name, Get_x, Get_y, Get_line
 
###############################################################################################################################################

def BuscarOriDest(x_ori,y_ori,x_dest,y_dest, stationList):
    #Recorremos toda la lista de estaciones
        for i in range(len(stationList)):
                #Miramos si las x y las y coinciden y por lo tanto hemos encontrado nuestra estación origen 
                if((x_ori == ((stationList[i]).Get_x()))and((y_ori == ((stationList[i]).Get_y())))):
                        nombre_ori = ((stationList[i]).Get_name())
                        id_ori = ((stationList[i]).Get_id())
                        linea_ori = ((stationList[i]).Get_line())
                #Miramos si las x y las y coinciden y por lo tanto hemos encontrado nuestra estación destino
                if((x_dest == ((stationList[i]).Get_x()))and((y_dest == ((stationList[i]).Get_y())))):
                        nombre_dest = ((stationList[i]).Get_name())
                        id_dest = ((stationList[i]).Get_id())
                        linea_dest = ((stationList[i]).Get_line())
        return nombre_ori, id_ori, linea_ori, nombre_dest, id_dest, linea_dest

#Funcion de la heuristica. 
def h_tiempo(x1, y1, x2, y2):
        velocidad = 100
        heu = DistEuclidea(x1,x2,y1,y2) 
        heu = heu/velocidad
        return heu

#Heruistic. Determines minimum number of stops in trajectory.   
def h_paradas(x1, y1, x2, y2):
    heu = DistEuclidea(x1,x2,y1,y2)
    

def Expandir(conexiones, cabeza):
#    hijos = conexiones[cabeza[len(cabeza)-1]].keys()
    hijos2 = list(conexiones[cabeza[len(cabeza)-1]].keys())
    return hijos2

#Calcula la suma f(h) + g(h) pasandole el nodo origen y destino de esos puntos en concreto 
def CalcularCostesHeuristicas(heuristicas, tiempos_conexiones, tiempos_transbordos, id_ori, id_dest, lista, Costes):    
    transbordos = 0
    auxiliar_con = tiempos_conexiones[id_ori]
#    if(tiempos_transbordos.has_key(id_ori)):
#            auxiliar_tra = tiempos_transbordos[id_ori]
#    aux = auxiliar_con.has_key(id_dest)
    if(id_ori in tiempos_transbordos):
        auxiliar_tra = tiempos_transbordos[id_ori]
#    aux = auxiliar_con.has_key(id_dest)
    aux = id_dest in auxiliar_con
    if(aux == True):
            auxiliar = auxiliar_con[id_dest]
    elif(aux == False):
            auxiliar = auxiliar_tra[id_dest]
            transbordos += 1
    auxiliar+= Costes[id_dest]
    auxiliar1=auxiliar + heuristicas[id_dest]
    return auxiliar, auxiliar1, transbordos
#auxiliar1 contiene f(h)+g(h) mientras que auxiliar solo lleva el valor del coste


def DistEuclidea(x1,x2,y1,y2):
        return sqrt((x1-x2)**2+(y1-y2)**2)


