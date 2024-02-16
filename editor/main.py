# MAP EDITOR
# Authors: Ewen B.
#          Thomas D.

# IMPORTS
import json
import os.path

import pygame
import time
import tkinter
from tkinter import filedialog


# CLASSES
class Editor:  # main class for the editor
    def __init__(self):  # class init
        self.TIME_FLAG = time.time()  # CONST: timestamp used by the log function
        # 'self.TIME_FLAG' must be initialized before the first log because his value is used by the 'log' method
        self.log('Starting setup')
        self.WS = (800, 600)  # CONST: window size: (width, height)
        self.WN = '<RPG MAP MAKER> -v0.1-dev'  # CONST: window name

        self.log('Creating window')
        self.root = pygame.display.set_mode(self.WS)  # creating the pygame window
        pygame.display.set_caption(self.WN)  # setting the window name to 'self.WN'

        self.workspace_path = ''  # variable used to know where to r/w data (path to workspace directory)
        self.warning_check_equal(self.workspace_path,
                                 '',
                                 "The value of 'self.workspace_path' is not initialized in __init__")

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

    def check_and_create_file(self, relative_path):
        # creating the json files if they don't exist
        if not os.path.exists(f'{self.workspace_path}/{relative_path}'):
            _map_file = open(f'{self.workspace_path}/{relative_path}', 'a')  # the 'a' open argument creates the file if he
            #                                                                doesn't exist
            _map_file.close()  # closing it after the existence check is done
            self.log_success(f'\033[0;37m"{self.workspace_path}/{relative_path}"\033[0m created successfully')
        else:
            self.log(f'\033[0;37m"{self.workspace_path}/{relative_path}"\033[0m already exists')

    def render(self):  # method responsible for the rendering (visual part.)
        self.root.fill('black')  # resetting the root with black
        # TODO: implement visual part

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
        self.log('Project coherence check')
        self.check_and_create_file('map.json')
        with open(f'{self.workspace_path}/map.json', 'r+') as _map_file:  # opening map.json
            if _map_file.readlines():  # if the file is not empty
                _map_file.seek(0)  # setting read index to the beggining of the file
                _data = json.load(_map_file)  # loading file content into data variable
                for file_name in _data['areas']:  # parsing each area name inside the json map _data
                    self.check_and_create_file(f'{file_name}.json')  # checking if area files exists


        self.log_success('Coherence check done')
        self.log('Project setup')
        flag = False  # flag used to know if any setup was done inside the project
        with open(f'{self.workspace_path}/map.json', 'r+') as _map_file:  # opening map.json
            if not _map_file.readlines():  # if the file is empty
                self.log_warning('map.json is empty, creating basic structure')
                _BASIC_STRUCTURE = {
                    'name': self.input("Map name :"),
                    'areas': []
                }
                # writing the default data into map.json
                _map_file.seek(0)
                json.dump(_BASIC_STRUCTURE, _map_file, indent=4)
                _map_file.truncate()
                flag = True
            else:
                _map_file.seek(0)  # going to begining of the map file
                _data = json.load(_map_file)  # load the map file as _data
                for area_name in _data['areas']:  # parsing each area name in _data
                    with open(f'{self.workspace_path}/{area_name}.json', 'r+') as _area_file:  # opening map.json
                        if not _area_file.readlines():  # area file is empty
                            _area_file.write('{}')  # writing empty json structure into area map
                            flag = True
        if flag:
            self.log_success('Project setup done')
        else:
            self.log('No setup needed')

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
