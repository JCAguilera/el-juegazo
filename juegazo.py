# -*- coding: utf-8 -*-
"""
Macrosoft Ltda. Presenta:
Super Paralympics 2D Simulator 2017
"""

import pygame
#from pygame.locals import *
import os
import sys

#---------------#
# Configuración #
#---------------#

Resolucion = [1024,700]
Jugadores = 2
#Pantalla_Completa = False

#--------------------#
# Clases y Funciones #
#--------------------#

#Carga una imagen
def load_image(nombre, dir_imagen, alpha=False):
    # Encontramos la ruta completa de la imagen
    ruta = os.path.join(dir_imagen, nombre)
    try:
        image = pygame.image.load(ruta)
    except:
        print("Error, no se puede cargar la imagen: " + str(ruta))
        sys.exit(1)        
    # Comprobar si la imagen tiene "canal alpha" (como los png)
    if alpha == True:
        image = image.convert_alpha()
    else:
        image = image.convert()
    return image

#Retorna un objeto fuente, a partir del nombre y si la fuente es del sistema
def selFuente(fuente,tamano,sistema = True):
    if sistema:
        return pygame.font.SysFont(fuente, tamano)
    return pygame.font.Font(fuente, tamano)

#Crea y renderiza un objeto de dexto con una fuente y un color
def crearTexto(fuente, texto, colorRGB):
    text = fuente.render(texto, True, colorRGB)
    return text

def tecla(x):
    teclas = [["espacio","escape","arriba","abajo","izquierda","derecha","q","w","e","r","t","y","u","i","o","p","a","s","d","f","g","h","j","k","l","z","x","c","v","b","n","m"],
              [pygame.K_SPACE,pygame.K_ESCAPE,pygame.K_UP,pygame.K_DOWN,pygame.K_LEFT,pygame.K_RIGHT,pygame.K_q,pygame.K_w,pygame.K_e,pygame.K_r,pygame.K_t,pygame.K_y,pygame.K_u,pygame.K_i,pygame.K_o,pygame.K_p,pygame.K_a,pygame.K_s,pygame.K_d,pygame.K_f,pygame.K_g,pygame.K_h,pygame.K_j,pygame.K_k,pygame.K_l,pygame.K_z,pygame.K_x,pygame.K_c,pygame.K_v,pygame.K_b,pygame.K_n,pygame.K_m]]            
    for i in range(len(teclas)):
        if x == teclas[0][i]:
            return teclas[1][i]

#Objeto cursor
class Cursor(pygame.Rect):
    #Crea un rectángulo en la posicion (0,0) con 1px de largo y ancho.
    def __init__(self):
        pygame.Rect.__init__(self, 0, 0, 1, 1)
    
    #Retorna la posicion del cursor
    def update(self):
        (self.left,self.top) = pygame.mouse.get_pos()

#Objeto Boton
class Boton(pygame.sprite.Sprite):
   
    def __init__ (self,imagen1,imagen2,x = 0, y = 0):
        self.imagen_normal = imagen1
        self.imagen_seleccion = imagen2
        self.imagen_actual = self.imagen_normal
        self.rect = self.imagen_actual.get_rect()
        self.rect.left,self.rect.top = (x-(self.rect.right)/2,y-(self.rect.bottom)/2)
        
    
    def updateBoton(self,pantalla,cursor):
        if cursor.colliderect(self.rect):
            self.imagen_actual = self.imagen_seleccion
        else: self.imagen_actual = self.imagen_normal
        
        pantalla.blit(self.imagen_actual,self.rect)      

#Objeto jugador
class Jugador(pygame.sprite.Sprite):
    
    def __init__(self,control,imagen,pos):
        pygame.sprite.Sprite.__init__(self)
        image = load_image(imagen,"",True)
        self.image = pygame.transform.scale(image, (250, 186))
        self.rect = self.image.get_rect()
        self.control = tecla(control)
        self.velocidad = 0
        self.contador = 0
        self.presionado = False
        self.empezo = False
        self.maximo = 25
        self.ganando = False
        self.posicion = 0
        self.t = 0
        left = 100
        if pos == 1:
            left += 20
            top = 410
        elif pos == 0:
            top = 460
        self.rect.left = left
        self.rect.top = top
        self.posCero = left
    
    def acelerar(self):
        self.maximo = 25
        if self.velocidad < self.maximo:
            self.velocidad += 0.5
        self.posicion += self.velocidad
        return None
    
    def frenar(self):
        if self.velocidad > 0:
            x = self.velocidad%0.2
            if self.velocidad == x:
                self.velocidad = 0
            else:
                self.velocidad -= 0.2
        self.posicion += self.velocidad
        return None
    
    def cambiarImagen(self,nuevaImagen):
        tmpImg = load_image(nuevaImagen,"",True)
        self.image = pygame.transform.scale(tmpImg, (250, 250))
        return None

#Objeto de texto
class Texto():
    
    def __init__(self,texto,fuente,sistema,tamano,color):
        self.font = selFuente(fuente, tamano, sistema)
        self.color = color
        self.text = crearTexto(self.font, texto, self.color)
        self.rect = pygame.Rect(0,0,self.text.get_width(),self.text.get_height())
        
    def setTexto(self,texto):
        self.text = crearTexto(self.font, texto, self.color)
        return None

#Fondo de pantalla        
class Fondo():
    
    def __init__(self,ruta):
        img = load_image(ruta,"",False)
        self.imagen = pygame.transform.scale(img,(Resolucion[0],Resolucion[1]))
        self.imagen2 = pygame.transform.scale(img,(Resolucion[0],Resolucion[1]))

#-----------#
# Principal #
#-----------#

#MENU
def menu():
    pygame.init()
    
    w = Resolucion[0]
    h = Resolucion[1]
    
    screen = pygame.display.set_mode((w,h))
    pygame.display.set_caption("Super Paralympics 2D Simulator 2017")
    clock = pygame.time.Clock()
    
    imagenJugar1 = pygame.image.load("Boton Jugar 1 Prueba.png")
    imagenJugar2 = pygame.image.load("Boton Jugar 2 Prueba.png")
    imagenOpcion1 = pygame.image.load("Boton Opcion 1 recortado.png")
    imagenOpcion2 = pygame.image.load("Boton Opcion 2 recortado.png")
    imagenExit1 = pygame.image.load("Boton salir 1.png")
    imagenExit2 = pygame.image.load("Boton salir 2.png")
  
    
    botonJugar = Boton(imagenJugar1,imagenJugar2, (w)/2, (h-350)/2)
    botonOpcion = Boton(imagenOpcion1, imagenOpcion2 , (w)/2 , (h-100)/2)
    botonExit = Boton(imagenExit1, imagenExit2, (w)/2, (h+150)/2)
    cursor = Cursor()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if cursor.colliderect(botonExit.rect):
                    pygame.quit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if cursor.colliderect(botonJugar.rect):
                    main()
    
        clock.tick(60)
        screen.fill((0,0,0))
        cursor.update()
        botonJugar.updateBoton(screen, cursor)
        botonOpcion.updateBoton(screen, cursor)
        botonExit.updateBoton(screen, cursor)
        pygame.display.update()
        
#JUEGO
def main():
    pygame.init()
    
    pygame.mixer.init()
    pygame.mixer.music.load("BeepBox-Song-Lelu2.midi")
    pygame.mixer.music.play()
    
    w = Resolucion[0]    
    h = Resolucion[1]
    x = w    
    
    screen = pygame.display.set_mode((w,h));
    clock = pygame.time.Clock()
    #pygame.mouse.set_visible(False)
    
    macrosoft = Texto("Macrosoft Ltda. Presenta:","Ubuntu",True,20,(0,0,0))
    superw = Texto("Super Paralympics 2D","DOCTEURTACOTAC.ttf",False,70,(0,0,0))
    superw2 = Texto("Simulator 2017","DOCTEURTACOTAC.ttf",False,70,(0,0,0))  
    demo = Texto("","Ubuntu",True,10,(0,0,0))
    FPS = Texto("FPS","Ubuntu",True,30,(0,0,0))
    
    fondo = Fondo("16-bit-wallpaper-3.jpg.png")
    
    jugador1 = Jugador("espacio","atletaunos.png",0)
    jugador2 = Jugador("arriba","atletadoss.png",1)
    vel = Texto(str(jugador1.velocidad),"Ubuntu",True,20,(0,0,0))
    pos = Texto(str(jugador1.posicion),"Ubuntu",True,20,(0,0,0))
    velT = "Velocidad"
    
    velocidadTotal = 0
    comenzado = False
    
    easter_egg = ""    
    
    run = True
    while(run):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYUP:
                #if event.key == jugador1.control:              
                    #Se levanta la tecla
                if event.key == pygame.K_g:
                    easter_egg = ""
                    easter_egg += "G"
                if event.key == pygame.K_r:
                    easter_egg += "R"
                if event.key == pygame.K_i:
                    easter_egg += "I"
                if event.key == pygame.K_n:
                    easter_egg += "N"
                if event.key == pygame.K_c:
                    easter_egg +="C"
                if event.key == pygame.K_h:
                    easter_egg += "H"
                if event.key == pygame.K_t:
                    easter_egg += "T"
                if event.key == pygame.K_o:
                    easter_egg += "O"
            if event.type == pygame.KEYDOWN:
                if event.key == jugador1.control:
                    jugador1.empezo = True
                    jugador1.acelerar()
                    comenzado = True
                    jugador1.contador = 0
                    if jugador1.t == 60:
                        jugador1.t = 1
                    else:
                        jugador1.t += 1
                if event.key == pygame.K_UP:
                    jugador2.empezo = True
                    comenzado = True
                    jugador2.acelerar()
                    jugador2.contador = 0
                    if jugador2.t == 60:
                        jugador2.t = 1
                    else:
                        jugador2.t += 1
                if event.key == pygame.K_ESCAPE:
                    run = False
                
        #Obs: Las imagenes van en orden de fondo -> frente
        screen.blit(fondo.imagen, (x,0))
        screen.blit(fondo.imagen2,(x-w,0))
        #Textos
        screen.blit(macrosoft.text,(20,20))
        screen.blit(superw.text,(20,50))
        screen.blit(superw2.text,(20,100))
        screen.blit(demo.text,(500,160))
        #Mostrar Velocidad
        vel.setTexto(velT + " Jugador 1: " + str(round(jugador1.velocidad)) + velT + " Jugador 2: " + str(round(jugador2.velocidad)) + velT + " Total: " + str(round(velocidadTotal)))
        screen.blit(vel.text,(20,h-30))
        #Mostrar Pocición
        pos.setTexto("Posiciones: P1: " + str(jugador1.posicion)+" P2: " + str(jugador2.posicion))
        screen.blit(pos.text,(20,h-60))        
        #Mostrar FPSs
        FPS.setTexto("FPS: " + str(round(clock.get_fps(),1)))
        screen.blit(FPS.text,(w-FPS.text.get_width()-20,20))
        #Sprites:
        if Jugadores == 2:
            pl2 = pygame.sprite.RenderPlain(jugador2)
            pl2.draw(screen)
        pl1 = pygame.sprite.RenderPlain(jugador1)
        pl1.draw(screen)
            
        if jugador1.empezo:
            jugador1.contador += 1
            if jugador1.contador>=60: #Si dejó de presionar
                jugador1.frenar()
        if jugador2.empezo and Jugadores == 2:
            jugador2.contador += 1
            if jugador2.contador>=60: #Si dejó de presionar
                jugador2.frenar()
                
        if Jugadores == 2:  
            diferenciaPosicion = jugador1.posicion - jugador2.posicion
            #diferenciaVelocidad = jugador1.velocidad - jugador2.velocidad
                
            if diferenciaPosicion > 0: #Jugador 1 Ganando
                jugador2.rect.left = jugador2.posCero - diferenciaPosicion
                velocidadTotal = jugador1.velocidad
            elif diferenciaPosicion < 0:
                jugador1.rect.left = jugador1.posCero + diferenciaPosicion
                velocidadTotal = jugador2.velocidad
        else:
            velocidadTotal = jugador1.velocidad
        
        if comenzado: #Si ya empezó
            x = x - velocidadTotal
            if x <= 0:
                x = w
        
        #Easter egg "Grinchito"
        if easter_egg == "GRINCHITO":
            easter_egg = ""
            jugador1.cambiarImagen("easteregg.png")
            jugador1.rect.top = 400
            #Cambio textos como enfermo
            macrosoft.setTexto("Macrosoft Ltda. ama a Grinchito!")
            superw.setTexto("GRINCHITO IS LOVE")
            demo.setTexto("help")
            pygame.display.set_caption("donde boto el ramo?")
            velT = "Grinchibilidad"
        
        clock.tick(60)
        pygame.display.flip()
    print("Juanky Was Here!")
    pygame.quit()
if __name__ == "__main__":
    menu()
    
