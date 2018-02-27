import configparser
import os
import sys

def check_file():
    if not(os.path.isfile('config.cfg')):
        with open('config.cfg','w+') as file:
            file.write(
            "[check_mk]\n\
    folder =\n\
    user =\n\
    password =\n\
    url =\n\
    [agentes]\n\
    rpm =\n\
    deb =\n\
    win =\n\
    [logwatch]\n\
    plugin =\n\
    cfg =")

config = configparser.ConfigParser()
config.read('config.cfg')

def check(config = config):
    for i in config.sections():
        for j in config._sections[i]:
            if (config._sections[i][j] == ''):
                print(config._sections[i][j])
                return 0
    return 1

def sections(config = config):
    return config.sections()

def info(seccion,config = config):
    return config._sections[seccion]

def set(seccion,attrib,texto,config = config):
    config.set(seccion,attrib,texto)

def save(config = config):
    with open('config.cfg','r+') as file:
        config.write(file)
