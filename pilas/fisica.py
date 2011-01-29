# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

import pilas
import Box2D as box2d
import math


class Fisica(object):
    "Representa un simulador de mundo fisico, usando la biblioteca box2d."
    
    def __init__(self):
        self.escenario = box2d.b2AABB()
        self.escenario.lowerBound = (-1000.0, -1000.0)
        self.escenario.upperBound = (1000.0, 1000.0)
        self.mundo = box2d.b2World(self.escenario, (0.0, -90.0), True)
        
        self.i = 0

    def actualizar(self):
        self.mundo.Step(1.0 / 20.0, 10, 8)
        self.i += 1
        
    def dibujar_figuras_sobre_pizarra(self, pizarra):
        "Dibuja todas las figuras en una pizarra. Indicado para depuracion."
        cuerpos = self.mundo.bodyList
        cantidad_de_figuras = 0
        
        pizarra.definir_color(pilas.colores.amarillo)
        
        for cuerpo in cuerpos:
            xform = cuerpo.GetXForm()
            
            for figura in cuerpo.shapeList:
                cantidad_de_figuras += 1
                tipo_de_figura = figura.GetType()
                
                if tipo_de_figura == box2d.e_polygonShape:
                    vertices = []
                    
                    for v in figura.vertices:
                        pt = box2d.b2Mul(xform, v)
                        
                        vertices.append((pt.x, pt.y))
                        
                    pizarra.dibujar_poligono(vertices)
                    
                elif tipo_de_figura == box2d.e_circleShape:
                    pizarra.dibujar_circulo(cuerpo.position.x, cuerpo.position.y, figura.radius, False)
                else:
                    print "no se que este esta figura..."
        
    def crear_cuerpo(self, definicion_de_cuerpo):
        return self.mundo.CreateBody(definicion_de_cuerpo)
    
    def crear_suelo(self):
        bodyDef = box2d.b2BodyDef()
        bodyDef.position=(0.0, -240)

        dynamic = False

        if not dynamic:
            density = 0

        body = self.mundo.CreateBody(bodyDef)
                    
        boxDef = box2d.b2PolygonDef()
        width = 640
        height= 1
        boxDef.SetAsBox(width, height, (0,0), 0)
        

        restitution=0.16
        friction=0.5
        
        boxDef.density = density
        boxDef.restitution = restitution
        boxDef.friction = friction
        body.CreateShape(boxDef)
        
        body.SetMassFromShapes()
    
        self.suelo = body
        
    def obtener_distancia_al_suelo(self, x, y, dy):
        """Obtiene la distancia hacia abajo desde el punto (x,y). 
        
        El valor de 'dy' tiene que ser positivo.
        
        Si la funcion no encuentra obstaculos retornara
        dy, pero en paso contrario retornara un valor menor
        a dy.
        """
        
        if dy < 0:
            raise Exception("El valor de 'dy' debe ser positivo, ahora vale '%f'." %(dy))

        delta = 0
        
        while delta < dy:
            
            if self.obtener_cuerpos_en(x, y-delta):
                return delta
            
            delta += 1
            
        return delta

    def obtener_cuerpos_en(self, x, y):
        "Retorna una lista de cuerpos que se encuentran en la posicion (x, y) o retorna una lista vacia []."

        AABB = box2d.b2AABB()
        f = 1
        AABB.lowerBound = (x-f, y-f)
        AABB.upperBound = (x+f, y+f)

        cuantos, cuerpos = self.mundo.Query(AABB, 2)

        if cuantos == 0:
            return []
        
        lista_de_cuerpos = []
        
        for s in cuerpos:
            cuerpo = s.GetBody()
                    
            if s.TestPoint(cuerpo.GetXForm(), (x, y)):
                lista_de_cuerpos.append(cuerpo)

        return lista_de_cuerpos

class Figura(object):
    "Representa un figura que simula un cuerpo fisico."

    def obtener_x(self):
        return self._cuerpo.position.x

    def definir_x(self, x):
        self._cuerpo.SetXForm((x, self.y), self._cuerpo.GetAngle())

    def obtener_y(self):
        return self._cuerpo.position.y

    def definir_y(self, y):
        self._cuerpo.SetXForm((self.x, y), self._cuerpo.GetAngle())

    def obtener_rotacion(self):
        return - math.degrees(self._cuerpo.GetAngle())

    def definir_rotacion(self, angulo):
        self._cuerpo.SetXForm((self.x, self.y), math.radians(-angulo))
        
    def impulsar(self, dx, dy):
        self._cuerpo.ApplyImpulse((dx, dy), self._cuerpo.GetWorldCenter())

    x = property(obtener_x, definir_x)
    y = property(obtener_y, definir_y)
    rotacion = property(obtener_rotacion, definir_rotacion)
    
class Circulo(Figura):
    "Representa un cuerpo de circulo."
    
    def __init__(self, x, y, radio, dinamica=True, densidad=1.0, restitucion=0.56, friccion=10.5):
        fisica = pilas.mundo.fisica
        bodyDef = box2d.b2BodyDef()
        bodyDef.position=(x, y)

        #userData = { 'color' : self.parent.get_color() }
        #bodyDef.userData = userData
        #self.parent.element_count += 1
        
        body = fisica.crear_cuerpo(bodyDef)

        # Create the Body
        if not dinamica:
            densidad = 0

        # Add a shape to the Body
        circleDef = box2d.b2CircleDef()
        circleDef.density = densidad
        circleDef.radius = radio
        circleDef.restitution = restitucion
        circleDef.friction = friccion

        body.CreateShape(circleDef)
        body.SetMassFromShapes()    

        self._cuerpo = body

class Rectangulo(Figura):
    
    def __init__(self, x, y, ancho, alto, dinamica=True, densidad=1.0, restitucion=0.56, friccion=10.5):
        fisica = pilas.mundo.fisica
        bodyDef = box2d.b2BodyDef()
        bodyDef.position=(x, y)

        #userData = { 'color' : self.parent.get_color() }
        #bodyDef.userData = userData
        #self.parent.element_count += 1
        
        body = fisica.crear_cuerpo(bodyDef)

        # Create the Body
        if not dinamica:
            densidad = 0

        # Add a shape to the Body
        boxDef = box2d.b2PolygonDef()
        
        boxDef.SetAsBox(ancho, alto, (0,0), 0)
        boxDef.density = densidad
        boxDef.restitution = restitucion
        boxDef.friction = friccion
        body.CreateShape(boxDef)

        body.SetMassFromShapes()    

        self._cuerpo = body

class ConstanteDeDistancia():
    
    def __init__(self, figura_1, figura_2):
        if not isinstance(figura_1, Figura) or not isinstance(figura_2, Figura):
            raise Exception("Las dos figuras tienen que ser objetos de la clase Figura.")
        
        constante = box2d.b2DistanceJointDef()
        constante.Initialize(c._cuerpo, c1._cuerpo, (0,0), (0,0))
        constante.collideConnected = True
        f.mundo.CreateJoint(constante)
