# MAP EDITOR
# Authors: Ewen B.
#          Thomas D.

# IMPORTS
import pygame
import time


# CLASSES
class Editor:  # main class for the editor
    def __init__(self):  # class init
        self.TIME_FLAG = time.time()  # used by the log function
        self.WS = (800, 600)  # window size: (width, height)

        self.log("Création de la fenêtre")
        self.root = pygame.display.set_mode(self.WS)  # creating the pygame window
        self.running = True  # variable responsable for "mainloop while condition"
        self.run()  # actualy starting the editor
        pygame.quit()  # clean pygame exit
        self.log("Fermeture de l'éditeur")

    def log(self, msg):  # method to log a message into console with the corresponding timestamp
        print(f"{int((time.time()-self.TIME_FLAG)*100)/100}] {msg}")

    def render(self):  # method responsable for the rendering (visual part.)
        self.root.fill("black")  # resetting the root with black
        # TODO: implement visual part

    def update(self):  # method responsable for the update (logical part.)
        # TODO: implement logical part
        pass

    def run(self):  # method containing the mainloop
        while self.running:  # mainloop
            for event in pygame.event.get():   # basic pygame event handling
                if event.type == pygame.QUIT:  #
                    self.running = False       #

            self.update()  # calling Editor.update method each frame
            self.render()  # calling Editor.render method each frame
            pygame.display.update()  # properly updating the displayed surface


# MAIN
if __name__ == "__main__":
    editor_instance = Editor()
