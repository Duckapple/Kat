from helpers.fileutils import getAllProblems
from commands.test import testCommand

def cleanupCommand(args, options):
    
    for problem in getAllProblems():
        testCommand([problem], {"archive": "true"})
        


    


cleanupFlags = []
