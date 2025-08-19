# Clase que representa cada nodo del árbol B+
class NodoBPlus:
    def __init__(self, es_hoja=False):
        self.es_hoja = es_hoja        # True si este nodo es una hoja; False si es un nodo interno
        self.claves = []              # Lista para guardar las claves ordenadas (IDs)
        self.hijos = []               # Solo para nodos internos: guarda referencias a los hijos
        self.siguiente = None         # Solo para hojas: apunta a la siguiente hoja
        self.padre = None             # Apunta al nodo padre

        self.valores = [] if es_hoja else None

# Clase principal del Árbol B+
class ArbolBPlus:
    def __init__(self, orden):
        self.raiz = NodoBPlus(es_hoja=True)  # Al principio, la raíz es una hoja vacía
        self.orden = orden                   # Este número define el máximo de claves por nodo (tu lógica usa >= orden para dividir)

    def insertar(self, clave, valor):
        # Encuentra la hoja correcta donde insertar la nueva clave
        hoja = self.buscar_hoja(self.raiz, clave)
        # Inserta la clave en la hoja de forma ordenada
        self.insertar_en_hoja(hoja, clave, valor)

        # Si la hoja tiene muchas claves, hay que dividirla
        if len(hoja.claves) >= self.orden:
            nueva_hoja, clave_prom = self.dividir_hoja(hoja)

            # Insertamos la clave promovida al padre
            self.insertar_en_padre(hoja, clave_prom, nueva_hoja)

    def buscar_hoja(self, nodo, clave):
        # Si ya estamos en una hoja, retornamos esa hoja
        if nodo.es_hoja:
            return nodo

        # Si no es hoja, buscamos entre las claves para decidir a qué hijo bajar
        for i in range(len(nodo.claves)):
            if clave < nodo.claves[i]:
                return self.buscar_hoja(nodo.hijos[i], clave)

        # Si no es menor que ninguna clave, bajamos por el último hijo
        return self.buscar_hoja(nodo.hijos[-1], clave)

    def insertar_en_hoja(self, hoja, clave, valor):
        # actualiza si se encuentra la misma clave
        # Búsqueda lineal para encontrar posición (listas cortas por nodo)
        i = 0
        while i < len(hoja.claves) and hoja.claves[i] < clave:
            i += 1

        if i < len(hoja.claves) and hoja.claves[i] == clave:
            # Actualizar proveedor existente
            hoja.valores[i] = valor
        else:
            hoja.claves.insert(i, clave)
            hoja.valores.insert(i, valor)

    def dividir_hoja(self, hoja):
        # Creamos una nueva hoja (el nodo derecho)
        nueva_hoja = NodoBPlus(es_hoja=True)

        # Calculamos en qué punto dividir la hoja
        mitad = (self.orden + 1) // 2

        # Partimos las claves en dos partes
        izquierda_claves = hoja.claves[:mitad]   # Parte que se queda en la hoja original
        derecha_claves = hoja.claves[mitad:]     # Parte que se va a la nueva hoja

        # *** Partimos también los valores en paralelo ***
        izquierda_vals = hoja.valores[:mitad]
        derecha_vals = hoja.valores[mitad:]

        hoja.claves = izquierda_claves
        hoja.valores = izquierda_vals

        nueva_hoja.claves = derecha_claves
        nueva_hoja.valores = derecha_vals

        # Conectamos la nueva hoja con la siguiente, formando una lista enlazada de hojas
        nueva_hoja.siguiente = hoja.siguiente
        hoja.siguiente = nueva_hoja

        # Asignamos el mismo padre a la nueva hoja
        nueva_hoja.padre = hoja.padre

        # La clave que se va a subir al padre es la primera de la nueva hoja
        clave_prom = derecha_claves[0]

        return nueva_hoja, clave_prom

    def insertar_en_padre(self, nodo_izq, clave, nodo_der):
        # Si se dividió la raíz, se crea una nueva raíz
        if nodo_izq == self.raiz:
            nueva_raiz = NodoBPlus(es_hoja=False)
            nueva_raiz.claves = [clave]
            nueva_raiz.hijos = [nodo_izq, nodo_der]
            self.raiz = nueva_raiz

            nodo_izq.padre = nueva_raiz
            nodo_der.padre = nueva_raiz
            return

        # Obtenemos el nodo padre
        padre = nodo_izq.padre

        # Buscamos la posición del hijo izquierdo
        i = padre.hijos.index(nodo_izq)

        # Insertamos la clave en la lista de claves del padre
        padre.claves.insert(i, clave)

        # Insertamos el nuevo hijo (derecho) justo después del hijo izquierdo
        padre.hijos.insert(i + 1, nodo_der)

        # Asignamos el nuevo padre al hijo derecho
        nodo_der.padre = padre

        # Si el padre ahora tiene demasiadas claves, también hay que dividirlo
        if len(padre.claves) >= self.orden:
            nuevo_nodo, clave_prom = self.division_interna_nodos(padre)
            self.insertar_en_padre(padre, clave_prom, nuevo_nodo)

    def division_interna_nodos(self, nodo):
        # Creamos un nuevo nodo interno
        nuevo_nodo = NodoBPlus(es_hoja=False)

        # Buscamos el punto medio para dividir
        mitad = len(nodo.claves) // 2
        clave_prom = nodo.claves[mitad]  # Esta se va a subir al nivel superior

        # Dividimos las claves en izquierda y derecha
        claves_izq = nodo.claves[:mitad]
        claves_der = nodo.claves[mitad + 1:]

        # Dividimos los hijos
        hijos_izq = nodo.hijos[:mitad + 1]
        hijos_der = nodo.hijos[mitad + 1:]

        nodo.claves = claves_izq
        nodo.hijos = hijos_izq

        nuevo_nodo.claves = claves_der
        nuevo_nodo.hijos = hijos_der

        # Asignamos el nuevo padre a los hijos derechos
        for hijo in hijos_der:
            hijo.padre = nuevo_nodo

        nuevo_nodo.padre = nodo.padre

        return nuevo_nodo, clave_prom

    # se reformateo el texto para adaptarlo a la clase de proveed
    def imprimir_hojas(self):
        # Imprime todas las hojas conectadas (lista enlazada) mostrando id y nombre
        nodo = self.raiz
        while not nodo.es_hoja:
            nodo = nodo.hijos[0]

        while nodo:
            pares = ", ".join(f"{k}:{v.name}" for k, v in zip(nodo.claves, nodo.valores))
            print(f"[{pares}]", end=" -> ")
            nodo = nodo.siguiente
        print("None")


    #agregado especialmente para los requisitos del proyecto
    # Recorrido por hojas en el orden de los id devolviendo lista de Proveedores
    def listar_todos(self):
        resultado = [] #lista donde se guardaran todos los resultados
        nodo = self.raiz # empezamos desde la raiz para recorrer el arbol

        # se recorre toda el arbol y se van agregando a la lista hasta llegar a las hojas
        while not nodo.es_hoja:
            nodo = nodo.hijos[0]
        while nodo:
            resultado.extend(nodo.valores)
            nodo = nodo.siguiente
        return resultado

    # Búsqueda por ID (recorrido hasta hoja y búsqueda binaria lineal)
    def buscar_por_id(self, clave):
        #usa la funcion para descender hasta donde deberia esta la hoja con la clave
        hoja = self.buscar_hoja(self.raiz, clave)
        for i, k in enumerate(hoja.claves):
            if k == clave: # si encuentra la clave devuelve el objeto
                return hoja.valores[i]
        return None # si no esta existe un id asociado a un objeto retornara none

    # Búsqueda por servicio (case-insensitive) recorriendo hojas
    def buscar_por_servicio(self, servicio: str):
        servicio = servicio.strip().lower() #reconvierte servicio sin espacios y en minusculas para evitar errores
        resultados = [] # guarda los resultados en una lista
        nodo = self.raiz # empezamos de la raiz para poder recorrer todo el arbol
        while not nodo.es_hoja: # ciclo que se asegura de recorrer todo el arbol
            nodo = nodo.hijos[0]
        while nodo:
            for prov in nodo.valores:
                # convierte en minusculas el servicio y si coincide lo inserta en la lista de resultados y va al siguiente nodo
                if prov.service.lower() == servicio:
                    resultados.append(prov)
            nodo = nodo.siguiente
        return resultados #al recorrer todo el arbol al final retorna la lista

    # Listados ordenados por nombre o por calificación usando el recorrido por hojas
    def listar_por_nombre(self):
        # se usa la funcion listar para tener todo el contenido del arbol, despues usamos sorted para que se de a a la z
        return sorted(self.listar_todos(), key=lambda p: p.name.lower()) #key se usa para devolver el valor deseado a ordenar
        # p es un objeto provider al cual se accedio al nombre para poder ordenarlo de a a z de forma correcta


    def listar_por_calificacion(self, descendente=True):
        #usa un objeto de la lista rating que esta guardado str a float
        def keyfun(p):
            try: # usamos la exepcion si por alguna razon falla que no para el programa
                return float(p.rating)
            except:
                return p.rating
        return sorted(self.listar_todos(), key=keyfun, reverse=descendente) # se hace el sort de mayor a menor usando la lista
