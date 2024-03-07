# MAP EDITOR
# Authors: Ewen B.
#          Thomas D.

# IMPORTS
import os
import json


# CLASSES
class FileManager:
    def __init__(self):
        pass

    @staticmethod
    def check_and_create_file(editor_instance, relative_path):  # create file if he doesn't exist
        # creating the json files if they don't exist
        if not os.path.exists(f'{editor_instance.workspace_path}/{relative_path}'):
            _map_file = open(f'{editor_instance.workspace_path}/{relative_path}', 'a')  # the 'a' open argument creates the file if he
            #                                                                doesn't exist
            _map_file.close()  # closing it after the existence check is done
            editor_instance.log_success(f'\033[0;37m"{editor_instance.workspace_path}/{relative_path}"\033[0m created successfully')
        else:
            editor_instance.log(f'\033[0;37m"{editor_instance.workspace_path}/{relative_path}"\033[0m already exists')

    def project_coherence_check(self, editor_instance):
        self.check_and_create_file(editor_instance, 'map.json')
        with open(f'{editor_instance.workspace_path}/map.json', 'r+') as _map_file:  # opening map.json
            if _map_file.readlines():  # if the file is not empty
                _map_file.seek(0)  # setting read index to the beggining of the file
                _data = json.load(_map_file)  # loading file content into data variable
                for file_name in _data['areas']:  # parsing each area name inside the json map _data
                    self.check_and_create_file(editor_instance, f'{file_name}.json')  # checking if area files exists

    def project_setup(self, editor_instance):
        editor_instance.log('Project coherence check')
        self.project_coherence_check(editor_instance)
        editor_instance.log_success('Coherence check done')

        editor_instance.log('Project setup')
        flag = False  # flag used to know if any setup was done inside the project
        with open(f'{editor_instance.workspace_path}/map.json', 'r+') as _map_file:  # opening map.json
            if not _map_file.readlines():  # if the file is empty
                editor_instance.log_warning('map.json is empty, creating basic structure')
                _BASIC_STRUCTURE = {
                    'name': editor_instance.input('Map name : '),
                    'areas': [],
                }
                editor_instance.log('Initializing areas creation (press enter without a name if you are done)')
                _input_data = 'not empty'
                while _input_data != '':
                    _input_data = editor_instance.input('Provide area name : ')
                    if _input_data != '': _BASIC_STRUCTURE['areas'].append(_input_data)
                # writing the default data into map.json
                _map_file.seek(0)
                json.dump(_BASIC_STRUCTURE, _map_file, indent=4)
                _map_file.truncate()
                flag = True

        if flag:
            editor_instance.log_success('Changes have been made to map.json')
            editor_instance.log('Redoing a coherence check')
            self.project_coherence_check(editor_instance)
            editor_instance.log_success('Coherence check done')

        flag = False
        with open(f'{editor_instance.workspace_path}/map.json', 'r+') as _map_file:  # opening map.json
            _map_file.seek(0)  # going to beginning of the map file
            _data = json.load(_map_file)  # load the map file as _data
            for area_name in _data['areas']:  # parsing each area name in _data
                with open(f'{editor_instance.workspace_path}/{area_name}.json', 'r+') as _area_file:  # opening area files
                    if not _area_file.readlines():  # area file is empty
                        editor_instance.log(f'Updating \033[0;37m"{area_name}.json"\033[0m')
                        _AREA_STRUCTURE = {
                            'w': int(editor_instance.input('Area width (in chunk, resizable later): ')),
                            'h': int(editor_instance.input('Area height (in chunk, resizable later): ')),
                            'x': int(editor_instance.input('Area X-position (in chunk, movable later): ')),
                            'y': int(editor_instance.input('Area Y-position (in chunk, movable later): ')),
                        }
                        _area_file.seek(0)
                        json.dump(_AREA_STRUCTURE, _area_file, indent=4)
                        _area_file.truncate()
                        flag = True
        if flag:
            editor_instance.log_success('Changes have been made to areas')

        editor_instance.log('Project setup done')

    @staticmethod
    def load_project(editor_instance):
        editor_instance.log('Loading project')
        with open(f'{editor_instance.workspace_path}/map.json', 'r+') as _map_file:  # opening map.json
            _data = json.load(_map_file)
            editor_instance.map_data['name'] = _data['name']
            for area_name in _data['areas']:  # parsing each area name in _data
                _area = {'name': area_name}  # added to the map_data dict later
                with open(f'{editor_instance.workspace_path}/{area_name}.json', 'r+') as _area_file:  # opening area files
                    _area_data = json.load(_area_file)
                    _area['x'] = _area_data['x']
                    _area['y'] = _area_data['y']
                    _area['w'] = _area_data['w']
                    _area['h'] = _area_data['h']
                editor_instance.map_data['areas'].append(_area)
        editor_instance.log_success('Project is loaded')
