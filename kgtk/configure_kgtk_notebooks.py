import os
import json
import subprocess
from pathlib import Path
from typing import List
from kgtk.files_config import files_config

always_print_env_variables = {'EXAMPLES_DIR', 'USE_CASES_DIR', 'GRAPH', 'OUT', 'TEMP', 'STORE', 'kgtk', 'kypher'}


class ConfigureKGTK(object):
    def __init__(self, file_list: List[str], kgtk_path: str = None, input_files_url: str = None):

        self.files = file_list
        self.INPUT_FILES_URL = "https://github.com/usc-isi-i2/kgtk-tutorial-files/raw/main/datasets/arnold" \
            if input_files_url is None else input_files_url

        self.kgtk_environment_variables = set()
        self.user_home = str(Path.home())
        print(f'User home: {self.user_home}')

        self.default_folder = "isi-kgtk-tutorial"

        self.current_dir = os.getcwd()
        print(f'Current dir: {self.current_dir}')
        if kgtk_path is not None:
            self.kgtk_path = kgtk_path
        else:
            self.kgtk_path = Path(self.current_dir).parent.absolute()
        print(f'KGTK dir: {self.kgtk_path}')
        self.examples_dir = f"{self.kgtk_path}/examples"
        self.use_cases_dir = f"{self.kgtk_path}/use-cases"
        print(f'Use-cases dir: {self.use_cases_dir}')

        os.environ['EXAMPLES_DIR'] = self.examples_dir
        os.environ['USE_CASES_DIR'] = self.use_cases_dir

        self.kgtk_environment_variables.add('EXAMPLES_DIR')
        self.kgtk_environment_variables.add('USE_CASES_DIR')

    def configure_kgtk(self,
                       input_graph_path: str = None,
                       output_path: str = None,
                       project_name: str = "kgtk",
                       graph_cache_path: str = None,
                       json_config_file: str = None,
                       debug=False):
        """
        configures the environment for a jupyter notebook.
        :param input_graph_path: path to the input graph files. By default it'll create a folder "isi-kgtk-tutorial" in
        user home and download files from github
        :param output_path: path where the output and temp files will be created. By default, "isi-kgtk-tutorial-out" in
        user home
        :param project_name: output folder name, 'kgtk' by default
        :param graph_cache_path: absolute path to the '.db' file. If not specified, create a new cache file in output path
        :param json_config_file: absolute path to json file which contains "file_key": "file_name" key-value pairs. By
        default, read a file from kgtk repo
        :return:
        """

        self.graph_files = json.load(open(json_config_file)) \
            if json_config_file is not None \
            else files_config

        # If the input graph path is not None, it is assumed it has the files required
        if input_graph_path is None:
            input_graph_path = f"{self.user_home}/{self.default_folder}/input"
            Path(input_graph_path).mkdir(parents=True, exist_ok=True)
            self.download_tutorial_files(input_graph_path)

        os.environ['GRAPH'] = input_graph_path
        self.kgtk_environment_variables.add('GRAPH')

        for key in self.graph_files:
            os.environ[key] = f"{input_graph_path}/{self.graph_files[key]}"
            self.kgtk_environment_variables.add(key)

        if output_path is None:
            output_project_path = f"{self.user_home}/{self.default_folder}/{project_name}"
        else:
            output_project_path = f"{output_path}/{project_name}"

        temp_path = f"{output_project_path}/temp.{project_name}"

        Path(output_project_path).mkdir(parents=True, exist_ok=True)
        Path(temp_path).mkdir(parents=True, exist_ok=True)

        os.environ['OUT'] = output_project_path
        os.environ['TEMP'] = temp_path
        self.kgtk_environment_variables.add('OUT')
        self.kgtk_environment_variables.add('TEMP')

        if graph_cache_path is None:
            graph_cache_path = f"{temp_path}/wikidata.sqlite3.db"
        os.environ['STORE'] = graph_cache_path
        self.kgtk_environment_variables.add('STORE')

        kgtk = "kgtk --debug" if debug else "kgtk"
        os.environ['kgtk'] = kgtk
        self.kgtk_environment_variables.add('kgtk')

        kypher = kgtk + " query --graph-cache " + os.environ['STORE']
        os.environ['kypher'] = kypher
        self.kgtk_environment_variables.add('kypher')

    def download_tutorial_files(self, graph_path):
        if not graph_path.endswith('/'):
            graph_path += '/'

        for f in self.files:
            if f in self.graph_files:
                url = f"{self.INPUT_FILES_URL}/{self.graph_files[f]}"
                cmd = f" wget {url} --directory-prefix={graph_path}"
                print(subprocess.getoutput(cmd))
            else:
                print(f"File: {f} not present in files config: {self.graph_files}")

    def print_env_variables(self):
        for key in self.kgtk_environment_variables:
            if key in always_print_env_variables:
                print(f"{key}: {os.environ[key]}")

        for key in self.files:
            print(f"{key}: {os.environ[key]}")

    def load_files_into_cache(self):
        """
        Loads files into graph cache. The keys in this list should be in json_config_file
        :param file_list:
        :return:
        """
        kypher_command = f"{os.environ['kypher']}"

        for f_key in self.files:
            kypher_command += f" -i \"{os.environ[f_key]}\" --as {f_key} "
        kypher_command += " --limit 3"
        print(kypher_command)
        print(subprocess.getoutput(kypher_command))
