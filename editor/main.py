# MAP EDITOR
# Authors: Ewen B.
#          Thomas D.

# IMPORTS
import pygame
import time
import tkinter
from tkinter import filedialog

# IMPORTS (EXTERN SCRIPTS)
import file_manager
import text


# CLASSES
class Editor:  # main class for the editor
    def __init__(self):  # class init

        pygame.init()  # pygame global init

        self.TIME_FLAG = time.time()  # CONST: timestamp used by the log function
        # 'self.TIME_FLAG' must be initialized before the first log because his value is used by the 'log' method
        self.log('Starting setup')
        self.WS = (800, 600)  # CONST: window size: (width, height)
        self.WN = '<RPG MAP MAKER> -v0.1-dev'  # CONST: window name

        self.log('Creating window')
        self.root = pygame.display.set_mode(self.WS)  # creating the pygame window
        pygame.display.set_caption(self.WN)  # setting the window name to 'self.WN'


        self.workspace_path = ''  # variable used to know where to r/w data (path to workspace directory)
        self.map_data = {
            'name': 'UNDEFINED',
            'areas': []
        }

        self.zoom_factor = 2

        self.FILE_MANAGER = file_manager.FileManager()
        self.TM_AREA = text.TextManager('Consolas.ttf', size=0)

        self.running = True  # variable responsible for "mainloop while condition"
        self.log_success('Setup complete, starting the editor')
        self.run()  # starting the editor
        pygame.quit()  # clean pygame exit
        self.log('Editor closed normally, exiting program with code 0')
        exit(0)  # End the program and return exit code 0

    def log(self, msg):  # method to log a message into console with the corresponding timestamp
        print(f'{int((time.time() - self.TIME_FLAG) * 100) / 100}] {msg}')

    def log_success(self, msg):  # log a success message in green
        self.log(f'\033[1;32mSUCCESS: {msg}\033[0m')

    def log_warning(self, msg):  # log a warning message in yellow
        self.log(f'\033[1;33mWARNING: {msg}\033[0m')  # log with a yellow message

    def warning_check_equal(self, variable, equal_to, msg) -> bool:  # log a warning message if 'variable' == 'equal_to'
        #                                                              return true if 'variable'=='equal_to' else false
        if variable == equal_to:
            self.log_warning(msg)
        return variable == equal_to

    def fatal_error(self, msg, exit_code=1):  # log an error message and exit with the specified exit code
        self.log(f'\033[1;31mERROR: {msg}\033[0m')  # log the error message
        pygame.quit()  # exiting pygame cleanly
        exit(exit_code)  # exiting the program with the specified exit code

    @staticmethod  # not using self -> static method
    def input(msg):  # gets user input and returns it
        return input(f'\033[1;35mINPUT:\033[0m {msg}')

    @staticmethod  # not using self -> static method
    def ask_for_path(title):  # method to open an explorer window to select a directory (freeze  but pygame don't crash)
        root = tkinter.Tk()  # creating a tkinter window to have a reference to it and avoid having one created by
        #                      default
        root.wm_iconify()  # hiding the window so that only the explorer gui is shown
        path = filedialog.askdirectory(title=title)  # using tkinter.filedialog to ask for directory
        root.destroy()
        return path

    def render(self):  # method responsible for the rendering (visual part.)
        self.root.fill('black')  # resetting the root with black
        # -/*/- MINIMAP RENDER -/*/- #
        for area in self.map_data['areas']:
            pygame.draw.rect(self.root, 'green',
                             (area['x']*self.zoom_factor, area['y']*self.zoom_factor,
                              area['w']*self.zoom_factor, area['h']*self.zoom_factor),
                             1)
        # -/*/- AREAs NAME RENDER -/*/- #
        for i, area in enumerate(self.map_data['areas']):
            self.TM_AREA.display(area['name'], (self.WS[0] - 200, i), self.root)


    def update(self):  # method responsible for the update (logical part.)
        # TODO: implement logical part
        pass

    def run(self):  # method containing the mainloop
        self.workspace_path = self.ask_for_path('Select workspace directory')  # ask for the workspace path
        self.log(f'Selected workspace path: "{self.workspace_path}"')
        if self.workspace_path == '':  # checking if the answer is correct
            self.fatal_error('Workspace path is empty, exiting with code -2', -2)
        else:
            self.log_success('Workspace path is valid, loading data from directory')

        self.FILE_MANAGER.project_setup(self)
        self.FILE_MANAGER.load_project(self)

        while self.running:  # mainloop
            for event in pygame.event.get():  # basic pygame event handling
                if event.type == pygame.QUIT:  # if the red cross is pressed
                    self.running = False  # stopping the mainloop

            self.update()  # calling Editor.update method each frame
            self.render()  # calling Editor.render method each frame
            pygame.display.update()  # properly updating the displayed surface


# MAIN
if __name__ == "__main__":  # if directly started and not just imported
    editor_instance = Editor()  # creating an instance of 'Editor'
