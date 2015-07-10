import pilasengine
from pilasengine import persistencia
from pilasengine import actores


class ActorPersonalizado(actores.Actor, persistencia.Persistente):

    def iniciar(self):
        persistencia.Persistente.iniciar(self)

        self.aprender('arrastrable')

        if not self.esta_guardado():
            self.definir_datos_a_guardar()
        else:
            self.cargar_datos()

    def definir_datos_a_guardar(self):
        self.agregar_atributo('x')
        self.agregar_atributo('y')


pilas = pilasengine.iniciar()
pilas.habilitar_persistencia(persistencia.ArchivoJSON, 'ejemplo')

actor = ActorPersonalizado(pilas)

boton = pilas.actores.Boton(x=-100)
boton.conectar_presionado(actor.persistir)

pilas.ejecutar()
