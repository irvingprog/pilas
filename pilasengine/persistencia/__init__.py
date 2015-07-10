import os
import json


class Persistente(object):
    
    id_persistencia = 0

    def iniciar(self):
        self.backend = self.pilas.backend_persistencia
        self.nombre_de_persistencia = self.__class__.__name__ + str(self.id_persistencia)
        if not self.esta_guardado():
            self.backend.agregar_objeto(self.nombre_de_persistencia)

        Persistente.id_persistencia += 1

    def agregar_atributo(self, atributo):
        self.backend.agregar_atributo(self.nombre_de_persistencia, atributo)

    def persistir(self):
        self.actualizar_data()
        self.backend.persistir()

    def actualizar_data(self):
        data = self.obtener_data()
        for atributo in data.get(self.nombre_de_persistencia, []):
            datos = self.backend.data[self.nombre_de_persistencia]
            datos[atributo] = getattr(self, atributo)

    def esta_guardado(self):
        return self.backend.objeto_esta_guardado(self.nombre_de_persistencia)

    def obtener_data(self):
        return self.backend.data

    def cargar_datos(self):
        data = self.obtener_data()
        for attr, valor in data[self.nombre_de_persistencia].items():
            setattr(self, attr, valor)


class ArchivoJSON(object):
    
    def __init__(self, nombre_archivo):
        self.nombre_archivo = '{}.json'.format(nombre_archivo)
        self.crear_o_cargar_datos()

    def persistir(self):
        with open(self.nombre_archivo, 'w') as f:
            json.dump(self.data, f)

    def agregar_objeto(self, nombre):
        self.data.update({nombre:dict()})

    def agregar_atributo(self, objeto, atributo):
        self.data[objeto].update({atributo:None})

    def objeto_esta_guardado(self, nombre):
        with open(self.nombre_archivo, 'r') as f:
            tmp_data = json.load(f)

        return nombre in tmp_data

    def crear_o_cargar_datos(self):
        if not os.path.exists(self.nombre_archivo):
            self.data = {}
            self.persistir()
        else:
            with open(self.nombre_archivo, 'r') as f:
                self.data = json.load(f)

