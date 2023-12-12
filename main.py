from re import X
from turtle import Screen
import pygame
from pygame import mixer
from pygame.constants import *


pygame.init()
mixer.init()

janela_larg = 1296
janela_alt = 720

janela = pygame.display.set_mode((janela_larg, janela_alt))
pygame.display.set_caption("Game")
clock = pygame.time.Clock()

exec = True
jogando = True
mapa_atual = 0
#ALGUMAS FONTES
fonts1 = pygame.font.SysFont('Bahnschrift', 60)
fonts2 = pygame.font.SysFont('Bahnschrift', 20)
fonts3 = pygame.font.SysFont('Bahnschrift', 30)
def desenhar_texto(texto, fonte, cor, x, y): #DESENHO O TEXTO NA TELA
    imagemtexto = fonte.render(texto, True, cor)
    janela.blit(imagemtexto, (x, y))

#imagens dos botoes
z_img= pygame.image.load('imgs/z.png').convert_alpha()
z_img = pygame.transform.scale(z_img,(35, 35))
enter_img = pygame.image.load('imgs/enter.png').convert_alpha()
enter_img = pygame.transform.scale(enter_img,(70, 35))

#dados do mapa
tile_size = int(janela_alt/10)
transforman = 0
class player():
  def __init__(self, x, y):
    self.mapa = 0
    self.altura = 120
    self.largura = 70
    self.robo_img_pd= pygame.image.load('imgs/robo_anim0.png').convert_alpha()
    self.img_dir = pygame.transform.scale(self.robo_img_pd,(self.largura, self.altura))
    self.img_esq = pygame.transform.flip(self.img_dir, True, False)
    self.img = self.img_dir
    self.rect = self.img.get_rect()
    self.rect.x = x
    self.rect.y = y
    self.width = self.img.get_width()
    self.height = self.img.get_height()
    self.vel_y = 0
    self.pulando = False
    self.caindo = False
    self.transformando = 0
    self.gravidade = True
    self.xpre = self.rect.x
    self.ypre = self.rect.y
    self.prel = self.largura
    self.prea = self.altura
  def telamod(self):
    fundo_img_pd = pygame.image.load('imgs/backgroundtelamod.png').convert_alpha()
    fundo_img = pygame.transform.scale(fundo_img_pd,(janela_larg,janela_alt))
    janela.blit(fundo_img,(0,0))
    self.rect.y = (210) - (self.altura/2)
    self.rect.x = (janela_larg/2) - (self.largura/2)
    desenhar_texto(f'Altura = {self.prea}', fonts3, 'black', (janela_larg/2 - 515),(janela_alt/2 + 85))
    desenhar_texto(f'Largura = {self.prel}', fonts3, 'black', (janela_larg/2 - 520),(janela_alt/2 - 200))
    desenhar_texto('X para Voltar', fonts3, 'black', (self.rect.x - 50), (self.rect.y + 285))
    desenhar_texto('Enter para Confirmar', fonts2, 'black', (self.rect.x - 60), (self.rect.y + 370))
    botao = pygame.key.get_pressed()
    if botao[pygame.K_RIGHT]:
      if self.prel < 150:
        self.prel+=1
    if botao[pygame.K_LEFT]:
      if self.prel > 40:
        self.prel-=1
    if botao[pygame.K_UP]:
      if self.prea < 250:
        self.prea+=1
    if botao[pygame.K_DOWN]:
      if self.prea > 60:
        self.prea-=1
    if botao[pygame.K_KP_ENTER] or botao[pygame.K_RETURN]:
      self.transformando = 0
      self.gravidade = True
      self.rect.x = self.xpre
      self.altura = self.prea
      self.largura = self.prel
      self.img_dir = pygame.transform.scale(self.robo_img_pd,(self.largura, self.altura))
      self.img_esq = pygame.transform.flip(self.img_dir, True, False)
      self.img = pygame.transform.scale(self.robo_img_pd,(self.largura, self.altura))
      self.rect = self.img.get_rect()
      self.width = self.img.get_width()
      self.height = self.img.get_height()
      self.rect.x = self.xpre
      self.rect.y = self.ypre - 200

  def reset(self):
    self.altura = 120
    self.largura = 70
    self.img_dir = pygame.transform.scale(self.robo_img_pd,(self.largura, self.altura))
    self.img_esq = pygame.transform.flip(self.img_dir, True, False)
    self.img = pygame.transform.scale(self.robo_img_pd,(self.largura, self.altura))
    self.rect = self.img.get_rect()
    self.width = self.img.get_width()
    self.height = self.img.get_height()
    self.rect.x = 80
    self.rect.y = 400
    self.prel = 70
    self.prea = 120
  
  def update(self):
    global mapa_atual
    dx = 0
    dy = 0
    botao = pygame.key.get_pressed()
    if self.gravidade == True:
      if botao[pygame.K_SPACE] and self.pulando == False and self.in_air == False:
          self.vel_y = -20
          self.pulando = True
      if botao[pygame.K_SPACE] == False:
        self.pulando = False
      if botao[pygame.K_LEFT]:
        if self.rect.left >= 0:
          self.img = self.img_esq
          dx-=5
      if botao[pygame.K_RIGHT]:
        if self.rect.right <= 1296:
          self.img = self.img_dir
          dx+=5
      if botao[pygame.K_r]:
        player.reset(self)
    if self.gravidade == False:
      if botao[pygame.K_x]:
        self.transformando = 0
        self.gravidade = True
        self.rect.x = self.xpre
        self.rect.y = self.ypre



    if self.transformando == 1:
      player.telamod(self)


    if self.gravidade == True:
      self.vel_y +=1
      if self.vel_y > 15:
        self.vel_y = 15
      dy=self.vel_y
  
    self.in_air = True
    for tile in world.tile_list:
      self.tile = tile[1]
      if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
        dx = 0
      if tile[1].colliderect(self.rect.x , self.rect.y + dy, self.width, self.height):
        if self.vel_y < 0:
          dy = tile[1].bottom - self.rect.top
          self.vel_y = 0
        elif self.vel_y >= 0:
          dy = tile[1].top - self.rect.bottom
          self.vel_y = 0
          self.in_air = False
    for tile in world.tile_list_nocol:
      self.tile = tile[1]
      if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
        janela.blit(z_img,(self.rect.x + 18, self.rect.y- 40))
        if botao[pygame.K_z]:
          self.transformando = 1
          self.xpre = self.rect.x
          self.ypre = self.rect.y
          self.gravidade = False
          if botao[pygame.K_z] == False:
            self.transformando = 1
    for tile in world.tile_list_espinhos:
      self.tile = tile[1]
      if tile[1].colliderect(self.rect.x, self.rect.y, self.width, self.height):
        player.reset(self)
    for tile in world.tile_list_portal:
      self.tile = tile[1]
      if tile[1].colliderect(self.rect.x, self.rect.y, self.width, self.height):
        janela.blit(enter_img,(self.rect.x, self.rect.y- 40))
        if botao[pygame.K_KP_ENTER] or botao[pygame.K_RETURN]:
          mapa_atual = 1
          player.reset(self)

          



    self.rect.x +=dx
    self.rect.y +=dy



    janela.blit(self.img, self.rect)
    #pygame.draw.rect(janela,'red', self.rect, 2)
  
  




class mapa():
  def __init__(self, data):
      self.tile_list = []
      self.tile_list_nocol = []
      self.tile_list_espinhos = []
      self.tile_list_portal = []
      #imagens
      block_img_pd = pygame.image.load('imgs/bloco0.png').convert_alpha()
      block_img = pygame.transform.scale(block_img_pd,(tile_size+0, tile_size+0))
      maquina_img_pd = pygame.image.load('imgs/maquina0.png').convert_alpha()
      maquina_img = pygame.transform.scale(maquina_img_pd,(tile_size+1,tile_size+73))
      espinho_img_pd = pygame.image.load('imgs/espinho0.png').convert_alpha()
      espinho_img = pygame.transform.scale(espinho_img_pd,(tile_size+1,tile_size+1))
      portal_img_pd = pygame.image.load('imgs/porta0.png').convert_alpha()
      portal_img = pygame.transform.scale(portal_img_pd,(tile_size+1,tile_size+73))
      linha_count = 0
      for row in data:
        coluna_count = 0
        for tile in row:
          #blocos com hitbox
          if tile == 1:
            block_rect = block_img.get_rect()
            block_rect.x = coluna_count * tile_size
            block_rect.y = linha_count * tile_size
            tile = (block_img, block_rect)
            self.tile_list.append(tile)
          
          
          
          
          if tile == 2:
            maquina_rect = maquina_img.get_rect()
            maquina_rect.x = coluna_count * tile_size
            maquina_rect.y = linha_count * tile_size
            tile = (maquina_img, maquina_rect)
            self.tile_list_nocol.append(tile)
          if tile == 3:
            espinho_rect = espinho_img.get_rect()
            espinho_rect.x = coluna_count * tile_size
            espinho_rect.y = linha_count * tile_size
            tile = (espinho_img, espinho_rect)
            self.tile_list_espinhos.append(tile)
          if tile == 4:
            portal_rect = portal_img.get_rect()
            portal_rect.x = coluna_count * tile_size
            portal_rect.y = linha_count * tile_size
            tile = (portal_img, portal_rect)
            self.tile_list_portal.append(tile)
          coluna_count+=1
        linha_count+=1

  def blocos(self):
    for tile in self.tile_list:
      janela.blit(tile[0],tile[1])
    for tile in self.tile_list_nocol:
      janela.blit(tile[0], tile[1])
    for tile in self.tile_list_espinhos:
      janela.blit(tile[0], tile[1])
    for tile in self.tile_list_portal:
      janela.blit(tile[0], tile[1])



personagem = player(80,400)

while exec:
  
  if mapa_atual == 0:
    mapa_rodando = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,4],
    [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,0,0,0,1,0,0,1,0,1,1,1],
    [0,0,2,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,1,3,3,3,3,3,3,3,3,3],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    ]

  if mapa_atual == 1:
    mapa_rodando = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,4],
    [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,1],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
    [0,0,2,0,0,1,1,0,0,1,0,0,1,0,1,1,0,0],
    [0,0,0,0,0,0,1,3,3,3,3,3,3,3,3,3,3,3],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    ]
  
  if jogando == True: 
    fundo_img_pd = pygame.image.load('imgs/background0.png').convert_alpha()
    fundo_img = pygame.transform.scale(fundo_img_pd,(janela_larg,janela_alt))
    janela.blit(fundo_img,(0,0))
    world = mapa(mapa_rodando)
    world.blocos() 
    personagem.update()
  if jogando == False:
    janela.fill('black')
    personagem.update()


  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      exec = False




  clock.tick(60)
  pygame.display.update()



pygame.quit()