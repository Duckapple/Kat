import glob, os, random
from playsound import playsound

prefix = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'resources')

def winsound():
    playsound(random.choice(glob.glob(os.path.join(prefix, "win", "*.mp3"))))


def losesound():
    playsound(random.choice(glob.glob(os.path.join(prefix, "lose", "*.mp3"))))
