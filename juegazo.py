# -*- coding: utf-8 -*-
"""
Macrosoft Ltda. Presenta:
Super Paralympics Simulator 2017
"""

import pygame, os, sys, glob, random
#from pygame.locals import *

#---------------#
# Configuración #
#---------------#

Resolucion = [1024,700]
Jugadores = 2
Controles = ["space","up"] #jugador 1, jugador 2

#--------------------#
# Clases y Funciones #
#--------------------#

#Teclas y nombres/codigos
keys = [pygame.K_BACKSPACE,pygame.K_TAB,pygame.K_CLEAR,pygame.K_RETURN,pygame.K_PAUSE,pygame.K_ESCAPE,pygame.K_SPACE,pygame.K_EXCLAIM,pygame.K_QUOTEDBL,pygame.K_HASH,pygame.K_DOLLAR,pygame.K_AMPERSAND,pygame.K_QUOTE,pygame.K_LEFTPAREN,pygame.K_RIGHTPAREN,pygame.K_ASTERISK,pygame.K_PLUS,pygame.K_COMMA,pygame.K_MINUS,pygame.K_PERIOD,pygame.K_SLASH,pygame.K_0,pygame.K_1,pygame.K_2,pygame.K_3,pygame.K_4,pygame.K_5,pygame.K_6,pygame.K_7,pygame.K_8,pygame.K_9,pygame.K_COLON,pygame.K_SEMICOLON,pygame.K_LESS,pygame.K_EQUALS,pygame.K_GREATER,pygame.K_QUESTION,pygame.K_AT,pygame.K_LEFTBRACKET,pygame.K_BACKSLASH,pygame.K_RIGHTBRACKET,pygame.K_CARET,pygame.K_UNDERSCORE,pygame.K_BACKQUOTE,pygame.K_a,pygame.K_b,pygame.K_c,pygame.K_d,pygame.K_e,pygame.K_f,pygame.K_g,pygame.K_h,pygame.K_i,pygame.K_j,pygame.K_k,pygame.K_l,pygame.K_m,pygame.K_n,pygame.K_o,pygame.K_p,pygame.K_q,pygame.K_r,pygame.K_s,pygame.K_t,pygame.K_u,pygame.K_v,pygame.K_w,pygame.K_x,pygame.K_y,pygame.K_z,pygame.K_DELETE,pygame.K_KP0,pygame.K_KP1,pygame.K_KP2,pygame.K_KP3,pygame.K_KP4,pygame.K_KP5,pygame.K_KP6,pygame.K_KP7,pygame.K_KP8,pygame.K_KP9,pygame.K_KP_PERIOD,pygame.K_KP_DIVIDE,pygame.K_KP_MULTIPLY,pygame.K_KP_MINUS,pygame.K_KP_PLUS,pygame.K_KP_ENTER,pygame.K_KP_EQUALS,pygame.K_UP,pygame.K_DOWN,pygame.K_RIGHT,pygame.K_LEFT]
keycodes = ["backspace","tab","clear","return","pause","escape","space","exclaim","quotedbl","hash","dollar","ampersand","quote","left_paren","right_paren","asterisk","plus","comma","minus","period","slash","0","1","2","3","4","5","6","7","8","9","colon","semicolon","less","equals","greater","question","at","left_bracket","backslash","right_bracket","caret","underscore","backquote","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","delete","kp_0","kp_1","kp_2","kp_3","kp_4","kp_5","kp_6","kp_7","kp_8","kp_9","kp_period","kp_divide","kp_multiply","kp_minus","kp_plus","kp_enter","kp_equals","up","down","right","left"]
#Encontrar tecla a partir de codigo
def key(nombre):
    try: 
        keypos = keycodes.index(nombre)
    except ValueError:
        sys.exit("Tecla '" + nombre + "' no encontrada!")
    return keys[keypos]
#Encontrar codigo a partir de tecla
def keyName(key):
    try:    
        keypos = keys.index(key)
    except ValueError:
        sys.exit("Tecla " + str(key) + " no registrada!")
    return keycodes[keypos]
#Carga una imagen
def load_image(nombre, dir_imagen, alpha=False):
    # Encontramos la ruta completa de la imagen
    ruta = os.path.join(dir_imagen, nombre)
    try:
        image = pygame.image.load(ruta)
    except:
        sys.exit("Error, no se puede cargar la imagen: " + str(ruta))        
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
    #Crea un boton con texto, en una posicion dada
    def __init__ (self,texto,x,y):
        self.imagen_normal = load_image("boton.png","images",True)
        self.imagen_seleccion = load_image("boton_hover.png","images",True)
        self.imagen_actual = self.imagen_normal
        self.texto = Texto(texto,"Fipps-Regular.otf",False,20,(0,0,0))
        self.rect = self.imagen_actual.get_rect()
        self.rect.left,self.rect.top = (x,y)
    #Cambia el texto del boton
    def setTexto(self, texto):
        self.texto.setTexto(texto)
    #Actualiza el boton
    def updateBoton(self,pantalla,cursor):
        if cursor.colliderect(self.rect):
            self.imagen_actual = self.imagen_seleccion
        else: self.imagen_actual = self.imagen_normal
        
        pantalla.blit(self.imagen_actual,self.rect)
        pantalla.blit(self.texto.text,(self.rect.left+(self.imagen_actual.get_width()-self.texto.text.get_width())/2,self.rect.top+(self.imagen_actual.get_height()-self.texto.text.get_height())/2))

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
#Objeto jugador
class Jugador(pygame.sprite.Sprite):
    
    def __init__(self,control,imagen,pos,ID):
        pygame.sprite.Sprite.__init__(self)
        image = load_image(imagen,"images",True)
        self.image = pygame.transform.scale(image, (260, 186))
        self.rect = self.image.get_rect()
        self.control = key(control)
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
            top = 410
        elif pos == 0:
            top = 500
        self.rect.left = left
        self.rect.top = top
        self.posCero = left
        self.id = ID
        #animaciones
        self.initialAnimSpeed = 1
        self.currentAnimSpeed = self.initialAnimSpeed
        self.initialAnimSpeedMeta = 10
        self.currentAnimSpeedMeta = self.initialAnimSpeedMeta
        self.anim = sorted(glob.glob("images/animations/Atleta"+str(ID)+ "_*.png"))
        self.gameAnim = sorted(glob.glob("images/animations/AnimAtleta"+str(ID)+"_*.png"))
        self.animGanar = sorted(glob.glob("images/animations/Atleta"+str(ID)+"Gan*.png"))
        self.animPerder = sorted(glob.glob("images/animations/Atleta"+str(ID)+"Per*.png"))
        self.anim.sort()
        self.animPosition = 0
        self.animPosMeta = 0
        self.animMax = len(self.gameAnim) - 1
        self.animar(0)
        self.initT = 0
        self.initAnipos = 0
        self.initTimes = [0,15]
    
    def acelerar(self):
        if self.t == 60:
            self.t = 1
        else:
            self.t += 1
        self.contador = 0
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
    #AnimacionMeta
    def animacionMeta(self, pos, gano):
        animaciones = []
        if gano:
            animaciones = self.animGanar
        else:
            animaciones = self.animPerder
        if pos != 0:
            self.currentAnimSpeedMeta -= 1
            #self.x += pos
            
        if self.currentAnimSpeedMeta == 0:
            self.image = pygame.transform.scale(load_image(animaciones[self.animPosMeta],"",True), (260, 186))
            self.currentAnimSpeedMeta = self.initialAnimSpeedMeta
            if self.animPosMeta == 3:
                self.animPosMeta = 0
            else:
                self.animPosMeta += 1
        
    def colisiona(self, col):
        return self.rect.colliderect(col)

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

#Titulo
class Title():
    def __init__(self):
        self.image = pygame.transform.scale(load_image("title_0.png","images/animations",True), (600,300))
        self.initialAnimSpeed = 1
        self.currentAnimSpeed = self.initialAnimSpeed
        self.anim = sorted(glob.glob("images/animations/title_*.png"))
        self.anim.sort()
        self.animPosition = 0
        self.animMax = len(self.anim) - 1
        self.animar(0)
    def animar(self, pos):
        if pos != 0:
            self.currentAnimSpeed -= 1
            
        if self.currentAnimSpeed == 0:
            self.image = pygame.transform.scale(load_image(self.anim[self.animPosition],"",True), (600, 300))
            self.currentAnimSpeed = self.initialAnimSpeed
            if self.animPosition == 3:
                self.animPosition = 0
            else:
                self.animPosition += 1
    def update(self, screen, rect):
        screen.blit(self.image, rect)
#-----------#
# Variables #
#-----------#

caption = "Super Paralympics 2D Simulator 2017"
icon = load_image('icon.png', 'images', True);
w = Resolucion[0]
h = Resolucion[1]

#-----------#
# Principal #
#-----------#

#CHECK (Comprobar opciones y variables)
def check():
    print("Checkeando configuración...")
    if Jugadores < 0 or Jugadores > 2:
        sys.exit("Sólo 1 o 2 Jugadores!")
    for i in Controles:
        if i == "escape":
            sys.exit("No se puede utilizar la tecla escape")
        else:
            key(i)
    print("Revision completada.")
    print("Iniciando juego...")
    intro()
#INTRO
def intro():
    pygame.init()
    
    screen = pygame.display.set_mode((w,h))
    pygame.display.set_caption(caption)
    pygame.display.set_icon(icon)
    clock = pygame.time.Clock()
    
    intro = load_image("macrosoft.png","images",False)
    copy = Texto("© 2017 Macro Software Development","wide_pixel-7.ttf",False,20,(0,0,0))
    play = False
    
    t = 0
    i = 0
    
    while True:
        clock.tick(60)
        if t < 180:
            t = t+1
        else:
            play = True
        
        screen.fill((255,255,255))
        screen.blit(copy.text,(w/2-copy.text.get_width()/2,h-30))
        screen.blit(intro,(w/2-intro.get_width()/2,h/2-intro.get_height()/2))
        
        if play: #Si se presionó "Jugar"
            if i<50:
                s = pygame.Surface((w,h))
                s.set_alpha(i*10)
                s.fill((0,0,0))
                screen.blit(s, (0,0)) 
                i = i + 1
            else: #Termina el Fade Out y pasa a la siguiente pantalla
                break
        
        pygame.display.update()
    menu()
#MENU
def menu(musicPos = 0.0):
    pygame.init()
    pygame.mixer.init()
    
    pygame.mixer.music.load('sounds/BeepBox-Song-Lelu2.ogg')
    pygame.mixer.music.play(-1,musicPos/1000.0)    
    
    x = w
    
    screen = pygame.display.set_mode((w,h))
    pygame.display.set_caption(caption)
    pygame.display.set_icon(icon)
    clock = pygame.time.Clock()
    
    #Cambiar a funcion load_image
    ficha1= pygame.image.load("images/ficha1.png")
    retrato1= pygame.image.load("images/1.png")
    ficha2= pygame.image.load("images/ficha2.png")
    retrato2= pygame.image.load("images/2.png")
    ficha3= pygame.image.load("images/ficha3.png")
    retrato3= pygame.image.load("images/3.png")
    ficha4= pygame.image.load("images/ficha4.png")
    retrato4= pygame.image.load("images/4.png")
    macrosoft = Texto("Macrosoft Ltda. Presenta:","wide_pixel-7.ttf",False,20,(0,0,0))
    title = Title()
    
    botonJugar = Boton("Jugar",100,350)
    botonOpcion = Boton("Opciones",(100+w-100-214)/2,350)
    botonExit = Boton("Salir",w-100-214,350)
    botonFicha1 = Ficha(retrato1, ficha1, (100), (h-200))
    botonFicha2 = Ficha(retrato2, ficha2, (300), (h-200))
    botonFicha3 = Ficha(retrato3, ficha3, (500), (h-200))
    botonFicha4= Ficha(retrato4, ficha4, (700), (h-200))
    cursor = Cursor()

    fondo = Fondo("fondo.png")    
    
    #Para el efecto FadeOut y cambio de pantalla
    play = False
    action = ""
    o = 0
    i = 0    
    titleT = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if cursor.colliderect(botonExit.rect):
                    action = "close"
                    play = True
                elif cursor.colliderect(botonJugar.rect):
                    action = "game"
                    play = True
                elif cursor.colliderect(botonOpcion.rect):
                    action = "options"
                    play = True
        
        if titleT < 5:
            titleT+= 1
        else:
            title.animar(1)
            titleT = 0
        
        x = x - 2
        if x <= 0:
            x = w        
        
        clock.tick(60)
        screen.blit(fondo.imagen, (x,0))
        screen.blit(fondo.imagen2,(x-w,0))
        screen.blit(macrosoft.text,(w/2-macrosoft.text.get_width()/2,10))
        title.update(screen, (200,50))
        cursor.update()
        botonJugar.updateBoton(screen, cursor)
        botonOpcion.updateBoton(screen, cursor)
        botonExit.updateBoton(screen, cursor)
        botonFicha1.updateFicha(screen, cursor)
        botonFicha2.updateFicha(screen, cursor)
        botonFicha3.updateFicha(screen, cursor)
        botonFicha4.updateFicha(screen, cursor)
        #Efecto "Fade Out"
        if play: #Si se presionó "Jugar"
            if o<50:
                s = pygame.Surface((w,h))
                s.set_alpha(o*10)
                s.fill((0,0,0))
                screen.blit(s, (0,0)) 
                o = o + 1
            else: #Termina el Fade Out y pasa a la siguiente pantalla
                break
        #Efecto FadeIn
        if i<50:
            s = pygame.Surface((w,h))
            s.set_alpha(255-(i*10))
            s.fill((0,0,0))
            screen.blit(s, (0,0)) 
            i = i + 1  
        pygame.display.update()
    if action == "game":
        menuJugadores()
    elif action == "options":
        opciones(pygame.mixer.music.get_pos())
    elif action == "close":
        print("Gracias por jugar!")
        pygame.quit()
#MenuJugadores
def menuJugadores():
    pygame.init()
    boton1jugador = Boton("1 jugador", 175, h/2)
    boton2jugadores = Boton("2 jugadores", w/2+125, h/2)
    screen = pygame.display.set_mode((w,h))
    pygame.display.set_caption(caption)
    pygame.display.set_icon(icon)
    fondo = Fondo("fondo.png")
    clock = pygame.time.Clock()   
    cursor = Cursor()
    x=w
    menu = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu = True                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                    players = 1
                    if cursor.colliderect(boton2jugadores.rect):
                        players = 2
                    main(players)
                        
        clock.tick(60)        
        screen.blit(fondo.imagen, (x,0))
        screen.blit(fondo.imagen2,(x-w,0))
        cursor.update()
        boton1jugador.updateBoton(screen, cursor)
        boton2jugadores.updateBoton(screen, cursor)
                        
        if menu:
           break
        pygame.display.update()         
        
    
#OPCIONES
def opciones(musicPos):
    pygame.init()
    pygame.mixer.music.load('sounds/BeepBox-Song-Lelu2.ogg')
    pygame.mixer.music.play(-1,musicPos/1000.0)
    
    x = w
    
    screen = pygame.display.set_mode((w,h))
    pygame.display.set_caption(caption)
    pygame.display.set_icon(icon)
    clock = pygame.time.Clock()    
    
    title = Texto("OPCIONES","DOCTEURTACOTAC.ttf",False,70,(0,0,0))
    player1 = Texto("Jugador 1","Ubuntu",True,50,(0,0,0))
    player2 = Texto("Jugador 2","Ubuntu",True,50,(0,0,0))
    ins = Texto("Para cambiar la tecla, haz click en el boton del jugador, y pulsa una tecla nueva.","Ubuntu",True,20,(0,0,0))
    ins2 = Texto("Pulsa ESC para volver al menu.","Ubuntu",True,20,(0,0,0))
    
    boton1 = Boton(Controles[0], 200, 250)
    boton2 = Boton(Controles[1], w-200-player2.text.get_width(), 250)
    botones = [boton1,boton2]

    fondo = Fondo("fondo.png")        
    
    cursor = Cursor()
    
    i=0
    o=0
    
    keyChange = False
    keyToChange = -1
    
    play = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and not keyChange:
                    play = True                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not keyChange:
                    if cursor.colliderect(boton1.rect):
                        keyToChange = 0
                        keyChange = True
                        boton1.setTexto("")
                    elif cursor.colliderect(boton2.rect):
                        keyToChange = 1
                        keyChange = True
                        boton2.setTexto("")
            if event.type == pygame.KEYDOWN:
                if keyChange and event.key != pygame.K_ESCAPE:
                    Controles[keyToChange] = keyName(event.key)
                    botones[keyToChange].setTexto(Controles[keyToChange])
                    keyChange = False
                    keyToChange = -1
        
        x = x - 2
        if x <= 0:
            x = w  
        
        clock.tick(60)        
        screen.blit(fondo.imagen, (x,0))
        screen.blit(fondo.imagen2,(x-w,0))
        screen.blit(title.text,(w/2-title.text.get_width()/2,50))
        screen.blit(player1.text,(200,170))
        screen.blit(player2.text,(w-player2.text.get_width()-200,170))
        screen.blit(ins.text,(w/2-ins.text.get_width()/2,380))
        screen.blit(ins2.text,(w/2-ins2.text.get_width()/2,420))
        cursor.update()
        boton1.updateBoton(screen, cursor)
        boton2.updateBoton(screen, cursor)
        #Efecto "Fade Out"
        if play: #Si se presionó "Jugar"
            if o<50:
                s = pygame.Surface((w,h))
                s.set_alpha(o*10)
                s.fill((0,0,0))
                screen.blit(s, (0,0)) 
                o = o + 1
            else: #Termina el Fade Out y pasa a la siguiente pantalla
                break            
        #Efecto FadeIn
        if i<50:
            s = pygame.Surface((w,h))
            s.set_alpha(255-(i*10))
            s.fill((0,0,0))
            screen.blit(s, (0,0)) 
            i = i + 1          
        
        pygame.display.update()
    menu(pygame.mixer.music.get_pos())
#JUEGO
def main(players = Jugadores):
    pygame.init()
    pygame.mixer.init()
    
    x = w    
    
    screen = pygame.display.set_mode((w,h));
    clock = pygame.time.Clock()
    #pygame.mouse.set_visible(False)
    
    #FORMATO: Texto, Fuente, Sistema, Tamaño, Color RGB
    macrosoft = Texto("","Ubuntu",True,20,(0,0,0))
    superw = Texto("","DOCTEURTACOTAC.ttf",False,70,(0,0,0))
    demo = Texto("","Ubuntu",True,10,(0,0,0))
    FPS = Texto("FPS","Ubuntu",True,30,(0,0,0))
    
    fondoRegular = Fondo("fondo.png")
    fondoStart = Fondo("fondo_start.png")
    fondoEnd = Fondo("fondo_end.png")
    
    endRect = fondoEnd.imagen.get_rect()
    endRect.left,endRect.top = w,0
    
    jugador1 = Jugador(Controles[0],"animations/Atleta1_0.png",0,1)
    jugador2 = Jugador(Controles[1],"animations/Atleta2_0.png",1,2)
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
    winPL = ""
    
    #"Distancia" necesaria para ganar
    #(Veces que se repite el fondo)
    distancia = 10
    
    easter_egg = ""  
    easter = False
    
    ganador = ""
    botPress = False
    
    run = True
    
    fondoT = 0
    
    i=0 #Para el efecto FadeIn
    o = 0 #Para el efecto FadeOut
    t = 0
    play = False
    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
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
                    if iniciado and jugador1.move:
                        if not easter:
                            jugador1.animar(1)
                        jugador1.empezo = True
                        jugador1.acelerar()
                        comenzado = True
                if event.key == jugador2.control and players == 2:
                    if iniciado and jugador2.move:
                        jugador2.animar(1)
                        jugador2.empezo = True
                        comenzado = True
                        jugador2.acelerar()
                        
                if event.key == pygame.K_ESCAPE:
                    menu()
        
        if players == 1 and iniciado:
            r = random.random()
            if r > 0.85:
                botPress = True
                
        if botPress:
            jugador2.empezo = True
            comenzado = True
            jugador2.acelerar()
            botPress = False
        
        #Obs: Las imagenes van en orden de fondo -> frente
        if fondoT == 0:
            screen.blit(fondoRegular.imagen, (x,0))
            screen.blit(fondoStart.imagen,(x-w,0))
        elif fondoT == distancia:
            endRect.left = x
            screen.blit(fondoEnd.imagen, endRect)
            screen.blit(fondoRegular.imagen,(x-w,0))
        else:
            screen.blit(fondoRegular.imagen, (x,0))
            screen.blit(fondoRegular.imagen2,(x-w,0))

        #Textos
        screen.blit(macrosoft.text,(20,20))
        screen.blit(superw.text,(20,50))
        screen.blit(demo.text,(500,160))
        #Mostrar Velocidad
        vel.setTexto(velT + " Jugador 1: " + str(round(jugador1.velocidad)) + velT + " Jugador 2: " + str(round(jugador2.velocidad)) + velT + " Total: " + str(round(velocidadTotal)))
        #screen.blit(vel.text,(20,h-30))
        #Mostrar Pocición
        pos.setTexto("Posiciones: P1: " + str(jugador1.posicion)+" P2: " + str(jugador2.posicion))
        #screen.blit(pos.text,(20,h-60))        
        #Mostrar FPSs
        FPS.setTexto("FPS: " + str(round(clock.get_fps(),1)))
        screen.blit(FPS.text,(w-FPS.text.get_width()-20,20))
        #Sprites:
        pl2 = pygame.sprite.RenderPlain(jugador2)
        pl2.draw(screen)
        pl1 = pygame.sprite.RenderPlain(jugador1)
        pl1.draw(screen)
        
        if not iniciado and not easter:
            jugador1.animacionInicio()
            jugador2.animacionInicio()
        
        if contadorIniciado == tIniciado:
            iniciado = True
        else:
            contadorIniciado += 1
            
        if jugador1.empezo:
            jugador1.contador += 1
            if jugador1.contador>=60: #Si dejó de presionar
                jugador1.frenar()
        if jugador2.empezo:
            jugador2.contador += 1
            if jugador2.contador>=60: #Si dejó de presionar
                jugador2.frenar()
                
        diferenciaPosicion = jugador1.posicion - jugador2.posicion
        if diferenciaPosicion > 0: #Jugador 1 Ganando
            jugador2.rect.left = jugador2.posCero - diferenciaPosicion
            ganador = jugador1
            velocidadTotal = ganador.velocidad
        elif diferenciaPosicion < 0:
            jugador1.rect.left = jugador1.posCero + diferenciaPosicion
            ganador = jugador2
            velocidadTotal = ganador.velocidad
        else:
            velocidadTotal = 0
        
        if comenzado: #Si ya comenzó
            
            if ganador != "":
                if ganador.colisiona(endRect):
                    if winSound:
                        winPL = ganador
                        win.play()
                        winSound = False
                    if t < 120:
                        t = t+1
                    else:
                        play = True
                    jugador1.move = False
                    jugador1.animacionMeta(1, ganador == jugador1)
                    jugador2.animacionMeta(1, ganador == jugador2)
                    jugador1.frenar()
                    jugador2.move = False
                    jugador2.frenar()
            
            x -= velocidadTotal
            if x <= 0:
                x = w
                fondoT += 1
        
        #Easter egg "Grinchito"
        if easter_egg == "GRINCHITO":
            easter = True
            easter_egg = ""
            jugador1.cambiarImagen("easteregg.png")
            jugador1.rect.top = 400
            #Cambio textos como enfermo
            macrosoft.setTexto("Macrosoft Ltda. ama a Grinchito!")
            superw.setTexto("GRINCHITO IS LOVE")
            demo.setTexto("help")
            pygame.display.set_caption("donde boto el ramo?")
            velT = "Grinchibilidad"
        #Efecto FadeOut
        if play:
            if o<50:
                s = pygame.Surface((w,h))
                s.set_alpha(o*10)
                s.fill((0,0,0))
                screen.blit(s, (0,0)) 
                o = o + 1
            else: #Termina el Fade Out y pasa a la siguiente pantalla
                break  
        #Efecto FadeIn
        if i<50:
            s = pygame.Surface((w,h))
            s.set_alpha(255-(i*10))
            s.fill((0,0,0))
            screen.blit(s, (0,0)) 
            i = i + 1        
        
        clock.tick(60)
        pygame.display.flip()
    winner(winPL)
def winner(winPL):
    pygame.init()
    
    screen = pygame.display.set_mode((w,h));
    clock = pygame.time.Clock()
    elGanador = Texto("El Ganador es:","Ubuntu",True,20,(0,0,0))
    jugador = Texto("JUGADOR " + str(winPL.id),"DOCTEURTACOTAC.ttf",False,70,(0,0,0))    
    enter = Texto("Pulsa ENTER para continuar...","Ubuntu",True,20,(0,0,0))    
    
    i = 0
    o = 0
    play = False
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    play = True
        screen.fill((62,197,202))
        screen.blit(elGanador.text,(Resolucion[0]/2 - elGanador.text.get_width()/2,Resolucion[1]/2 - jugador.text.get_height()/2 - elGanador.text.get_height()))
        screen.blit(jugador.text,(Resolucion[0]/2 - jugador.text.get_width()/2,Resolucion[1]/2 - jugador.text.get_height()/2))       
        screen.blit(enter.text,(Resolucion[0]/2 - enter.text.get_width()/2,Resolucion[1] - enter.text.get_height() - 10))        
        clock.tick(60)
        if play: #Si se presionó "Jugar"
            if o<50:
                s = pygame.Surface((w,h))
                s.set_alpha(o*10)
                s.fill((0,0,0))
                screen.blit(s, (0,0)) 
                o = o + 1
            else: #Termina el Fade Out y pasa a la siguiente pantalla
                break
        #Efecto FadeIn
        if i<50:
            s = pygame.Surface((w,h))
            s.set_alpha(255-(i*10))
            s.fill((0,0,0))
            screen.blit(s, (0,0)) 
            i = i + 1 
        
        pygame.display.flip()
    menu()
if __name__ == "__main__":
    check()
print("Juanky Was Here!")
input("Pulsa ENTER para continuar...")
