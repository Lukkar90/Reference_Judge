# Python libs
from configparser import ConfigParser


def read_config(file):
    config = ConfigParser()
    config.read(file)
    return config


config = read_config("config.ini")
