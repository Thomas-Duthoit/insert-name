import pygame
import time

class Editor:
    def __init__(self):
        self.TIME_FLAG = time.time()
        self.WS = [800, 600]

        self.log("Création de la fenêtre")
        self.root = pygame.display.set_mode(self.WS)
        self.running = True
        self.run()
        pygame.quit()
        self.log("Fermeture de l'éditeur")

    def log(self, msg):
        print(f"{int((time.time()-self.TIME_FLAG)*100)/100}] {msg}")

    def render(self):
        self.root.fill("black")

    def update(self):
        pass

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.update()
            self.render()


editor_instance = Editor()
