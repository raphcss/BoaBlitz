import pickle  # Pour envoyer des objets via un socket
import socket
import sys

import pygame

width, height = 800, 600
win = pygame.display.set_mode((width, height))

class Button:
    def __init__(self, color, x, y, width, height, text):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False

def redrawWindow(win, button1, button2):
    win.fill((255,255,255))
    button1.draw(win)
    button2.draw(win)

def menu():
    button1 = Button((0,255,0), 100, 200, 250, 100, text='Solo')
    button2 = Button((0,255,0), 450, 200, 250, 100, text='Multiplayer')
    run = True
    while run:
        redrawWindow(win, button1, button2)
        pygame.display.update()
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button1.isOver(pos):
                    print('Clicked the button1')
                    solo_game()
                if button2.isOver(pos):
                    print('Clicked the button2')
                    multiplayer_game()

            if event.type == pygame.MOUSEMOTION:
                if button1.isOver(pos):
                    button1.color = (255,0,0)
                else:
                    button1.color = (0,255,0)
                if button2.isOver(pos):
                    button2.color = (255,0,0)
                else:
                    button2.color = (0,255,0)
class Player():
    def __init__(self, x, y, width, height, color, name):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height)
        self.vel = 3
        self.name = name

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)
        font = pygame.font.SysFont(None, 50)
        img = font.render(self.name, True, self.color)
        win.blit(img, (self.x, self.y - 20))

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.vel
        if keys[pygame.K_RIGHT]:
            self.x += self.vel
        if keys[pygame.K_UP]:
            self.y -= self.vel
        if keys[pygame.K_DOWN]:
            self.y += self.vel
        self.rect = (self.x, self.y, self.width, self.height)
    def get_pseudo():
        pygame.init()
        window = pygame.display.set_mode((300, 200))
        pygame.display.set_caption("Enter your pseudo")
        font = pygame.font.Font(None, 32)
        clock = pygame.time.Clock()
        input_box = pygame.Rect(50, 50, 200, 32)
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_inactive
        active = False
        text = ''
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
                    color = color_active if active else color_inactive
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            return text
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode

            window.fill((30, 30, 30))
            txt_surface = font.render(text, True, color)
            width = max(200, txt_surface.get_width()+10)
            input_box.w = width
            window.blit(txt_surface, (input_box.x+5, input_box.y+5))
            pygame.draw.rect(window, color, input_box, 2)
            pygame.display.flip()
            clock.tick(30)

def solo_game():
    print('Launching the solo game...')
    def redrawWindowGame(win, player):
        win.fill((255, 255, 255))
        player.draw(win)
        pygame.display.update()
    run = True
    p = Player(50, 50, 100, 100, (0, 255, 0), Player.get_pseudo())
    clock = pygame.time.Clock()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        p.move()
        redrawWindowGame(win, p)
        pygame.display.update()
        clock.tick(60)

def multiplayer_game():
    print('Connecting to the server...')
    def redrawWindowGame(win, player):
        win.fill((255, 255, 255))
        player.draw(win)
        pygame.display.update()
    server = "192.168.1.1"  # Mettez ici l'adresse IP de votre serveur
    port = 5555
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((server, port))
    print('Successfully connected to the server')
    run = True
    p = Player(50, 50, 100, 100, (0, 255, 0), Player.get_pseudo())
    clock = pygame.time.Clock()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        p.move()
        data = pickle.dumps(p)
        clientSocket.send(data)
        other_players = pickle.loads(clientSocket.recv(2048))
        redrawWindowGame(win, p, other_players)
        pygame.display.update()
        clock.tick(60)

pygame.init()
menu()







