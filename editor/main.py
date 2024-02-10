# MAP EDITOR
# Authors: Ewen B.
#          Thomas D.

# IMPORTS
import pygame
import time


# CLASSES
class Editor:  # main class for the editor
    def __init__(self):  # class init
        self.TIME_FLAG = time.time()  # CONST: timestamp used by the log function
        # 'self.TIME_FLAG' must be itinialized before the first log because his value is used by the 'log' method
        self.log('Starting setup')
        self.WS = (800, 600)  # CONST: window size: (width, height)
        self.WN = '<RPG MAP MAKER> -v0.1-dev'  # CONST: window name

        self.log('Creating window')
        self.root = pygame.display.set_mode(self.WS)  # creating the pygame window
        pygame.display.set_caption(self.WN)  # setting the window name to 'self.WN'

        self.workspace_path = ''  # variable used to know where to r/w data (path to workspace directory)
        self.warning_check_equal(self.workspace_path, '', "The value of 'self.workspace_path' is not initialized in __init__")

        self.running = True  # variable responsable for "mainloop while condition"
        self.log_success('Setup complete, starting the editor')
        self.run()  # actualy starting the editor
        pygame.quit()  # clean pygame exit
        self.log('Editor closed normaly, exiting program with code 0')
        exit(0)  # End the program and return exit code 0

    def log(self, msg):  # method to log a message into console with the corresponding timestamp
        print(f'{int((time.time() - self.TIME_FLAG) * 100) / 100}] {msg}')

    def log_success(self, msg):  # log a success message in green
        self.log(f'\033[1;32mSUCCESS: {msg}\033[0m')

    def warning_check_equal(self, variable, equal_to, msg) -> bool:  # log a warning message if 'variable' == 'equal_to'
        #                                                              return true if 'variable'=='equal_to' else false
        if variable == equal_to: self.log(f'\033[1;33mWARNING: {msg}\033[0m')  # loging with a yellow message
        return variable == equal_to

    def render(self):  # method responsable for the rendering (visual part.)
        self.root.fill('black')  # resetting the root with black
        # TODO: implement visual part

    def update(self):  # method responsable for the update (logical part.)
        # TODO: implement logical part
        pass

    def run(self):  # method containing the mainloop
        while self.running:  # mainloop
            for event in pygame.event.get():  # basic pygame event handling
                if event.type == pygame.QUIT:  #
                    self.running = False  #

            self.update()  # calling Editor.update method each frame
            self.render()  # calling Editor.render method each frame
            pygame.display.update()  # properly updating the displayed surface


# MAIN
if __name__ == "__main__":  # if directly started and not just imported
    editor_instance = Editor()  # creating an instance of 'Editor'
