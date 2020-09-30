import os

from playsound import playsound
prefix = os.path.dirname(os.path.realpath(__file__)) + '/../resources/'


def winsound():
    playsound(prefix + 'win.mp3')


def losesound():
    playsound(prefix + 'lose.mp3')

