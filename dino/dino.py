import pygame
from pygame.locals import *
from sys import exit
import os
#Randrange = números aleatórios com saltos pré definidos
from random import randrange, choice # Choice = objeto aleatório dentro de uma lista    

pygame.init()
pygame.mixer.init()

#local aonde o script está armazenado
diretorio_principal = os.path.dirname(__file__)
#junção para as pastas dentro do diretório
diretorio_imagens = os.path.join(diretorio_principal, 'imagem')
diretorio_sons = os.path.join(diretorio_principal, 'sons')

largura = 640
altura = 420

branco = (255,255,255)

tela = pygame.display.set_mode((largura,altura))

som_colisao = pygame.mixer.Sound(os.path.join(diretorio_sons, 'sons_death_sound.wav'))
som_colisao.set_volume(1)
colidir = False

som_pontuacao = pygame.mixer.Sound(os.path.join(diretorio_sons, 'sons_score_sound.wav'))
som_pontuacao.set_volume(1)

escolha_obstaculo = choice([0,1])

pontos = 0

velocidade_jogo = 10

pygame.display.set_caption('Jogo do dino')

def exibe_mensagem(msg, tamanho, cor):
    fonte = pygame.font.SysFont('arial', tamanho, True, False)
    mensagem = f'{msg}'
    texto_formatado = fonte.render(mensagem, True, cor)
    return texto_formatado

def reiniciar_jogo():
    global colidir, pontos, velocidade_jogo, escolha_obstaculo
    colidir = False
    pontos = 0
    velocidade_jogo = 10
    dinovoador.rect.x = largura
    cacto.rect.x = largura
    escolha_obstaculo = choice([0,1])
    dino.rect.y = altura - 64 - 96//2
    dino.pulo = False

#carregando imagem                                                                       Se a imagem houver transparência ela ignora o fundo da imagem
sprite_sheet = pygame.image.load(os.path.join(diretorio_imagens, 'dinoSpritesheet.png')).convert_alpha()

class Dino(pygame.sprite.Sprite):
    def __init__(self):
        #inicializar a classe do pygame
        pygame.sprite.Sprite.__init__(self)
        self.som_pulo = pygame.mixer.Sound(os.path.join(diretorio_sons, 'sons_jump_sound.wav'))
        self.som_pulo.set_volume(1)
        self.imagens_dinoussauro = []
        #Loop para recortar as imagens dos dinossauros
        for i in range(3):
            img = sprite_sheet.subsurface((i * 32,0), (32,32))
            img = pygame.transform.scale(img, (32*3,32*3))
            self.imagens_dinoussauro.append(img)
        #Recorte da imagem            pos.inicial  largura e altura
        #self.img = sprite_sheet.subsurface((0,0), (32,32))
        #self.img2 = sprite_sheet.subsurface((32,0), (32,32))
        #self.img3 = sprite_sheet.subsurface((64,0), (32,32))

        self.index_lista = 0
        self.image = self.imagens_dinoussauro[self.index_lista]
        self.rect = self.image.get_rect()
        #criando máscara do dino
        self.mask = pygame.mask.from_surface(self.image)

        self.pos_y_inicial = altura - 64 - 96//2
        self.rect.center = (100, altura - 64)

        self.pulo = False
    
    def pular(self):
        self.pulo = True
        self.som_pulo.play()

    def update(self):
        if self.pulo:
            if self.rect.y <= 200:
                self.pulo = False
            self.rect.y -= 20
        else:
            if self.rect.y < self.pos_y_inicial:
                self.rect.y += 20
            else:
                self.rect.y = self.pos_y_inicial
        if self.index_lista > 2:
            self.index_lista = 0
        
        self.index_lista += 0.25
        self.image = self.imagens_dinoussauro[int(self.index_lista)]

class Nuvens(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((7 * 32, 0), (32,32))
        #aumentar a imagem
        self.image = pygame.transform.scale(self.image, (32*3,32*3))
        self.rect = self.image.get_rect()
         #sorteando número em determinado intervalo em Y
        self.rect.y = randrange(50,200, 50) #Número entre 50 e 200 sorteando de 50 em 50
        self.rect.x = largura - randrange(30,300,90)
    
    def update(self):
        #Pegar posição superior direito da imagem [pegando só a posição X, ela é uma tupla que contém x,y]
        if self.rect.topright[0] < 0:
            self.rect.x = largura
            #sorteando novamente
            self.rect.y = randrange(50,200, 50)
        self.rect.x -= velocidade_jogo

class Chao(pygame.sprite.Sprite):
    def __init__(self, pos_x):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((6*32, 0), (32,32))
        self.image = pygame.transform.scale(self.image, (32*2,32*2))
        self.rect = self.image.get_rect()
        self.rect.y = altura - 64
        #pos_x = i do ranger
        self.rect.x = pos_x * 64

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = largura

        self.rect.x -= 10

class Cacto(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((5*32,0), (32,32))
        self.image = pygame.transform.scale(self.image, (32*2, 32*2))
        self.rect = self.image.get_rect()

        self.mask = pygame.mask.from_surface(self.image)
        self.escolha = escolha_obstaculo

        self.rect.center = (largura, altura - 64)

        self.rect.x = largura
    
    def update(self):
        if self.escolha == 0:
            if self.rect.topright[0] < 0:
                self.rect.x = largura
            self.rect.x -= velocidade_jogo

class DinoVoador(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.imagens_dinossauro = []
        for i in range(3,5):
            img = sprite_sheet.subsurface((i * 32, 0), (32,32))
            img = pygame.transform.scale(img, (32 *3, 32* 3))
            self.imagens_dinossauro.append(img)
        
        self.index_lista = 0
        self.image = self.imagens_dinossauro[self.index_lista]

        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = ((largura, 300))

        self.escolha = escolha_obstaculo

        self.rect.x = largura
    
    def update(self):
        if self.escolha == 1:

            if self.rect.topright[0] < 0:
                self.rect.x = largura
            self.rect.x -= velocidade_jogo

            if self.index_lista > 1:
                self.index_lista = 0
            self.index_lista += 0.1
            self.image = self.imagens_dinossauro[int(self.index_lista)]

todas_sprites = pygame.sprite.Group()
dino = Dino()
todas_sprites.add(dino)
cacto = Cacto()
todas_sprites.add(cacto)
dinovoador = DinoVoador()
todas_sprites.add(dinovoador)

#Obstáculos
grupo_obstaculo = pygame.sprite.Group()
grupo_obstaculo.add(cacto)
grupo_obstaculo.add(dinovoador)

#criando 4 nuvens
for i in range(4):
    nuvem = Nuvens()
    todas_sprites.add(nuvem)

for i in range(largura * 2//64):
    chao = Chao(i)
    todas_sprites.add(chao)

relogio = pygame.time.Clock()

while True:
    relogio.tick(30)
    tela.fill(branco)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                exit()
                
            if event.key == K_SPACE and not colidir:
                if dino.rect.y != dino.pos_y_inicial:
                    pass
                else:
                    dino.pular()
            
            if event.key == K_r and colidir:    
                reiniciar_jogo()
    #Colsisões                      vai colidir, com o que vai, Se True o objeto colidido some
    colisoes = pygame.sprite.spritecollide(dino, grupo_obstaculo, False, pygame.sprite.collide_mask)#Colisão por pixel
    #Colisão é uma lista que recebe os objetos que colidem com o dino

    #Sorteando novamente o obstáculo após o atual sair da tela
    if cacto.rect.topright[0] <= 0 or dinovoador.rect.topright[0] <= 0:
        escolha_obstaculo = choice([0,1])
        cacto.rect.x = largura
        dinovoador.rect.x = largura
        cacto.escolha = escolha_obstaculo
        dinovoador.escolha = escolha_obstaculo

    todas_sprites.draw(tela)
    #quando ocorrer uma colisão o jogo vai parar
    if colisoes and not colidir:
        som_colisao.play()
        colidir = True
    
    if colidir:
        if pontos%100 == 0:
            pontos +=1
        game_over = exibe_mensagem('Game  Over', 40, (0,0,0))
        reiniciar = exibe_mensagem('Recomeçar clique R', 20, (0,0,0))
        tela.blit(game_over, (largura//2, altura//2))
        tela.blit(reiniciar, (largura//2, (altura//2) + 60))
    else:
        pontos += 1
        todas_sprites.update()
        texto_pontos = exibe_mensagem(pontos, 40, (0,0,0))
    
    if pontos%100 == 0:
        som_pontuacao.play()
        if velocidade_jogo >= 23:
            velocidade_jogo += 0
        else:
            velocidade_jogo += 1

    tela.blit(texto_pontos, (520, 30))

    pygame.display.flip()