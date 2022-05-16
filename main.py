# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import os

from Config.global_dict import dict_init
from Config.yaml_read import load_yaml


# import Config.yaml_read from load_yaml

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    dict_init()
    environ_name = os.environ.get("pytest")
    if environ_name:
        environ_name = 'test'
    load_yaml("D:\pythonworks\pytest-allure\config\config-" + environ_name + ".yaml")
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
