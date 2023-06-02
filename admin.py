import pickle
import socket

import pygame

width, height = 800, 600
win = pygame.display.set_mode((width, height))

class Admin:
    def __init__(self):
        self.clients = {}
        self.font = pygame.font.SysFont(None, 50)
        self.server = "172.18.194.8"
        self.port = 5555
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.server, self.port))

    def update_clients(self):
        data = pickle.dumps("get_clients")  
        self.socket.send(data)
        data = self.socket.recv(2048)  
        self.clients = pickle.loads(data)

    def draw(self, win):
        win.fill((255, 255, 255))
        y = 50
        for addr, name in self.clients.items():
            text = self.font.render(f"{name} ({addr})", True, (0, 0, 0))
            win.blit(text, (50, y))
            y += 50
        pygame.display.update()

def main():
    pygame.init()
    clock = pygame.time.Clock()
    admin = Admin()

    run = True
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        admin.update_clients()
        admin.draw(win)

main()