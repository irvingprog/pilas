# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

import pilas
from pilas.interfaz.base_interfaz import BaseInterfaz

class Boton(BaseInterfaz):
    """Representa un botón que se puede pulsar y disparar una acción."""

    def __init__(self, texto="Sin texto", x=0, y=0, icono=None):
        """Inicializa al actor.

        :param texto: Texto que se mostrará dentro de botón.
        :param x: Posición horizontal inicial.
        :param y: Posición vertical inicial.
        :param icono: Imagen que se mostrará sobre el botón.
        """
        BaseInterfaz.__init__(self, x=x, y=y)
        self.texto = texto
        self._crear_imagenes_de_botones()
        self.centro = ("centro", "centro")
        self.funcion = None
        self.fijo = True

        if icono:
            self.icono = pilas.imagenes.cargar(icono)
        else:
            self.icono = None

        self.escena.mueve_mouse.conectar(self.cuando_mueve_el_mouse)
        self.escena.click_de_mouse.conectar(self.cuando_hace_click)

    def conectar(self, funcion):
        """Asocia la función a ejecutar cuando se haga click sobre el botón.

        :param funcion: Referencia a la función que se desea vincular.
        """
        self.funcion = funcion

    def _crear_imagenes_de_botones(self):
        "Genera las 3 imagenes de los botones."
        ancho, alto = pilas.utils.obtener_area_de_texto(self.texto)
        tema = pilas.imagenes.cargar("boton/tema.png")

        self.imagen_normal = self._crear_imagen(tema, self.texto, ancho, 0)
        self.imagen_sobre = self._crear_imagen(tema, self.texto, ancho, 103)
        self.imagen_click = self._crear_imagen(tema, self.texto, ancho, 205)

        self.imagen = self.imagen_normal

    def cuando_mueve_el_mouse(self, evento):
        """Detecta el movimiento del mouse.

        :param evento: El objeto que representa el movimiento del mouse.
        """
        if self.activo:
            if self.colisiona_con_un_punto(evento.x, evento.y):
                self.imagen = self.imagen_sobre
            else:
                self.imagen = self.imagen_normal

    def cuando_hace_click(self, evento):
        """Gestiona los clicks sobre el botón.

        :param evento: Evento que representa al click.
        """
        if self.activo:
            if self.imagen == self.imagen_sobre:
                self.imagen = self.imagen_click

                if self.funcion:
                    self.funcion()

    def _crear_imagen(self, tema, texto, ancho, dx):
        "Genera una imagen de superficie de boton."
        imagen = pilas.imagenes.cargar_superficie(20 + ancho, 30)
        imagen.pintar_parte_de_imagen(tema, dx, 0, 5, 25, 0, 0)

        for x in range(1, ancho + 20, 5):
            imagen.pintar_parte_de_imagen(tema, dx + 5, 0, 5, 25, x, 0)

        imagen.pintar_parte_de_imagen(tema, dx + 75, 0, 5, 25, ancho + 15, 0)
        imagen.texto(texto, 10, 7)
        return imagen
