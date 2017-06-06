# -*- coding: utf-8 -*-
"""
Macrosoft Ltda. Presenta:
Super Paralympics 2D Simulator 2017
"""

import pygame, os, sys, glob
#from pygame.locals import *

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
    return pygame.font.Font("fonts/" + fuente, tamano)

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

#Objeto Ficha
class Ficha(pygame.sprite.Sprite):
   
    def __init__ (self,imagen1,imagen2,x = 0, y = 0):
        self.x = x
        self.y = y 
        self.imagen_normal = pygame.transform.scale(imagen1, (150,150))
        self.imagen_seleccion = pygame.transform.scale(imagen2, (1000,360))
        self.imagen_actual = self.imagen_normal
        self.rect = self.imagen_actual.get_rect()
        self.rectangulo = self.imagen_actual.get_rect()
        self.rectangulo.left=x
        self.rectangulo.top =y
        self.rect.left=x-(self.rect.right)/2
        self.rect.top =y-(self.rect.bottom)/2
              
    
    def updateFicha(self,pantalla,cursor):
        if cursor.colliderect(self.rectangulo):
            self.imagen_actual = self.imagen_seleccion
            self.rect.left,self.rect.top = (10,120)           
        else: 
            self.imagen_actual = self.imagen_normal
            self.rect.left,self.rect.top = (self.x,self.y)
        
        pantalla.blit(self.imagen_actual,self.rect)
# 
#Objeto jugador
class Jugador(pygame.sprite.Sprite):
    
    def __init__(self,control,imagen,pos,ID):
        pygame.sprite.Sprite.__init__(self)
        image = load_image(imagen,"images",True)
        self.image = pygame.transform.scale(image, (260, 186))
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
        self.move = True
        left = 100
        if pos == 1:
            left += 20
            top = 410
        elif pos == 0:
            top = 460
        self.rect.left = left
        self.rect.top = top
        self.posCero = left
        self.id = ID
        #animaciones
        self.initialAnimSpeed = 1
        self.currentAnimSpeed = self.initialAnimSpeed
        self.anim = sorted(glob.glob("images/animations/AtletaUno_*.png"))
        self.gameAnim = sorted(glob.glob("images/animations/AtletaUnoA_*.png"))
        self.anim.sort()
        self.animPosition = 0
        self.animMax = len(self.gameAnim) - 1
        self.animar(0)
        self.initT = 0
        self.initAnipos = 0
        self.initTimes = [0,15]
    
    def acelerar(self):
        self.maximo = 25
        if self.velocidad < self.maximo:
            self.velocidad += 0.5
        self.posicion += self.velocidad + 0.5
        return None    
    
    def frenar(self):
        if self.velocidad > 0:
            if self.velocidad%0.5 > 0:
                self.velocidad = 0
                self.posicion += self.velocidad%0.5
            else:            
                self.velocidad -= 0.5
                self.posicion += self.velocidad - 0.5
        return None
    
    def cambiarImagen(self,nuevaImagen):
        tmpImg = load_image(nuevaImagen,"images",True)
        self.image = pygame.transform.scale(tmpImg, (250, 250))
        return None
        
    #Animacion del comienzo
    def animacionInicio(self):
        self.initTimes[0] += 1
        if self.initTimes[0] == self.initTimes[1] and self.initAnipos < 15:
            self.initTimes[1] += 15
            self.image = pygame.transform.scale(load_image(self.anim[self.initAnipos],"",True), (260, 186))
            self.initAnipos += 1
    #Anima al jugador!
    def animar(self, pos):
        if pos != 0:
            self.currentAnimSpeed -= 1
            #self.x += pos
            
        if self.currentAnimSpeed == 0:
            self.image = pygame.transform.scale(load_image(self.gameAnim[self.animPosition],"",True), (260, 186))
            self.currentAnimSpeed = self.initialAnimSpeed
            if self.animPosition == self.animMax:
                self.animPosition = 0
            else:
                self.animPosition += 1
        #self.screen.blit(self.image, (self.rect.left, self.rect.top))

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
        img = load_image(ruta,"images",False)
        self.imagen = pygame.transform.scale(img,(Resolucion[0],Resolucion[1]))
        self.imagen2 = pygame.transform.scale(img,(Resolucion[0],Resolucion[1]))

#-----------#
# Variables #
#-----------#

caption = "Super Paralympics 2D Simulator 2017"

#-----------#
# Principal #
#-----------#

#MENU
def menu():
    pygame.init()
    pygame.mixer.init()
    
    pygame.mixer.music.load('sounds/BeepBox-Song-Lelu2.midi')
    pygame.mixer.music.play(-1)    
    
    w = Resolucion[0]
    h = Resolucion[1]
    x = w
    
    screen = pygame.display.set_mode((w,h))
    pygame.display.set_caption(caption)
    clock = pygame.time.Clock()
    
    #Cambiar a funcion load_image
    imagenJugar1 = pygame.image.load("images/Boton Jugar 1 Prueba.png")
    imagenJugar2 = pygame.image.load("images/Boton Jugar 2 Prueba.png")
    imagenOpcion1 = pygame.image.load("images/Boton Opcion 1 recortado.png")
    imagenOpcion2 = pygame.image.load("images/Boton Opcion 2 recortado.png")
    imagenExit1 = pygame.image.load("images/Boton salir 1.png")
    imagenExit2 = pygame.image.load("images/Boton salir 2.png")
    ficha1= pygame.image.load("images/ficha1.png")
    retrato1= pygame.image.load("images/1.png")
    ficha2= pygame.image.load("images/ficha2.png")
    retrato2= pygame.image.load("images/2.png")
    ficha3= pygame.image.load("images/ficha3.png")
    retrato3= pygame.image.load("images/3.png")
    ficha4= pygame.image.load("images/ficha4.png")
    retrato4= pygame.image.load("images/4.png")
  
    
    botonJugar = Boton(imagenJugar1,imagenJugar2, (w)/2, (h-350)/2)
    botonOpcion = Boton(imagenOpcion1, imagenOpcion2 , (w)/2 , (h-100)/2)
    botonExit = Boton(imagenExit1, imagenExit2, (w)/2, (h+150)/2)
    botonFicha1 = Ficha(retrato1, ficha1, (100), (h-200))
    botonFicha2 = Ficha(retrato2, ficha2, (300), (h-200))
    botonFicha3 = Ficha(retrato3, ficha3, (500), (h-200))
    botonFicha4= Ficha(retrato4, ficha4, (700), (h-200))
    cursor = Cursor()

    fondo = Fondo("16-bit-wallpaper-3.jpg.png")    
    
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
        
        x = x - 2
        if x <= 0:
            x = w        
        
        clock.tick(60)
        screen.blit(fondo.imagen, (x,0))
        screen.blit(fondo.imagen2,(x-w,0))
        cursor.update()
        botonJugar.updateBoton(screen, cursor)
        botonOpcion.updateBoton(screen, cursor)
        botonExit.updateBoton(screen, cursor)
        botonFicha1.updateFicha(screen, cursor)
        botonFicha2.updateFicha(screen, cursor)
        botonFicha3.updateFicha(screen, cursor)
        botonFicha4.updateFicha(screen, cursor)
        pygame.display.update()
        
#JUEGO
def main():
    pygame.init()
    pygame.mixer.init()
    
    w = Resolucion[0]    
    h = Resolucion[1]
    x = w    
    
    screen = pygame.display.set_mode((w,h));
    clock = pygame.time.Clock()
    #pygame.mouse.set_visible(False)
    
    #FORMATO: Texto, Fuente, Sistema, Tamaño, Color RGB
    macrosoft = Texto("Macrosoft Ltda. Presenta:","Ubuntu",True,20,(0,0,0))
    superw = Texto("Super Paralympics 2D","DOCTEURTACOTAC.ttf",False,70,(0,0,0))
    superw2 = Texto("Simulator 2017","DOCTEURTACOTAC.ttf",False,70,(0,0,0))  
    demo = Texto("","Ubuntu",True,10,(0,0,0))
    FPS = Texto("FPS","Ubuntu",True,30,(0,0,0))
    elGanador = Texto("Pulsa ENTER para continuar...","Ubuntu",True,30,(0,0,0))
    
    fondo = Fondo("16-bit-wallpaper-3.jpg.png")
    
    jugador1 = Jugador("espacio","animations/AtletaUno_0.png",0,1)
    jugador2 = Jugador("arriba","atletadoss.png",1,2)
    vel = Texto(str(jugador1.velocidad),"Ubuntu",True,20,(0,0,0))
    pos = Texto(str(jugador1.posicion),"Ubuntu",True,20,(0,0,0))
    velT = "Velocidad"

    #Musica y sonidos
    ready = pygame.mixer.Sound("sounds/ready_set_go.ogg")
    ready.play()
    win = pygame.mixer.Sound("sounds/ganador.ogg")
    pygame.mixer.music.load('sounds/estadio_ambiente.mp3')
    pygame.mixer.music.play(-1)
    
    
    velocidadTotal = 0
    comenzado = False
    iniciado = False
    contadorIniciado = 0
    tIniciado = 300
    winSound = True
    winPL = jugador1    
    
    easter_egg = ""    
    
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
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
                if event.key == pygame.K_RETURN:
                    if not winSound:
                        run = False
            if event.type == pygame.KEYDOWN:
                if event.key == jugador1.control:
                    if iniciado and jugador1.move:
                        jugador1.animar(1)
                        jugador1.empezo = True
                        jugador1.acelerar()
                        comenzado = True
                        jugador1.contador = 0
                        if jugador1.t == 60:
                            jugador1.t = 1
                        else:
                            jugador1.t += 1
                if event.key == pygame.K_UP:
                    if iniciado and jugador2.move:
                        jugador2.empezo = True
                        comenzado = True
                        jugador2.acelerar()
                        jugador2.contador = 0
                        if jugador2.t == 60:
                            jugador2.t = 1
                        else:
                            jugador2.t += 1
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                
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
        
        if not iniciado:
            jugador1.animacionInicio()
        
        if contadorIniciado == tIniciado:
            iniciado = True
        else:
            contadorIniciado += 1
            
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
            ganador = jugador1
            if diferenciaPosicion > 0: #Jugador 1 Ganando
                jugador2.rect.left = jugador2.posCero - diferenciaPosicion
                ganador = jugador1
            elif diferenciaPosicion < 0:
                jugador1.rect.left = jugador1.posCero + diferenciaPosicion
                ganador = jugador2
        else:
            ganador = jugador1
        
        velocidadTotal = ganador.velocidad
        
        if ganador.posicion >= 2000:
            if winSound:
                winPL = ganador
                win.play()
                winSound = False
            screen.blit(elGanador.text,(Resolucion[0] - elGanador.text.get_width() - 10,Resolucion[1] - elGanador.text.get_height() - 10))
        
        if jugador1.posicion >= 3000:
            jugador1.move = False
            jugador1.frenar()
        if jugador2.posicion >= 3000:
            jugador2.move = False
            jugador2.frenar()
        
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
    winner(winPL)
def winner(winPL):
    pygame.init()
    
    screen = pygame.display.set_mode((Resolucion[0],Resolucion[1]));
    clock = pygame.time.Clock()
    elGanador = Texto("El Ganador es:","Ubuntu",True,20,(0,0,0))
    jugador = Texto("JUGADOR " + str(winPL.id),"DOCTEURTACOTAC.ttf",False,70,(0,0,0))    
    enter = Texto("Pulsa ENTER para continuar...","Ubuntu",True,20,(0,0,0))    
    
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    run = False
        screen.fill((62,197,202))
        screen.blit(elGanador.text,(Resolucion[0]/2 - elGanador.text.get_width()/2,Resolucion[1]/2 - jugador.text.get_height()/2 - elGanador.text.get_height()))
        screen.blit(jugador.text,(Resolucion[0]/2 - jugador.text.get_width()/2,Resolucion[1]/2 - jugador.text.get_height()/2))       
        screen.blit(enter.text,(Resolucion[0]/2 - enter.text.get_width()/2,Resolucion[1] - enter.text.get_height() - 10))        
        clock.tick(60)
        pygame.display.flip()
    menu()
if __name__ == "__main__":
    menu()
