from commands.submit import submitFlags
from commands.test import testFlags
from commands.list import listFlags
from commands.get import getFlags
from commands.read import readFlags

def defineFlags(args):
    flags = {}
    flagNames = set()
    # Important! Add the flag definition to this statement!
    for flag in args: 
        if flag[0] not in flagNames:
            flagNames.add(flag[0])
            flags.update({flag[0]: flag[1:]})
        elif flag[1] and flag not in flags:
            flags.update({flag[0]: flag[1:]})
    
    shorthands = {}
    for flag in flags:
        letter = flag[0][0]
        if letter in shorthands:
            shorthands.update({letter: None})
        else:
            shorthands.update({letter: flag})

    flags["shorthands"] = shorthands

    return flags

flags = defineFlags(submitFlags + testFlags + listFlags + getFlags + readFlags + [("help", False)])


def divideArgs(args):
    arg = []
    options = {}
    for i in range(0, len(args)):
        word = args[i]
        if "-" in word:
            otherWord = args[i+1] if i+1 < len(args) else None
            option = makeOption(word, otherWord)
            if option:
                options.update(option)
        else:
            arg.append(word)
    return arg, options

def makeOption(word, nextWord):
    flag = None
    value = None
    if "=" in word:
        word, value = word.split("=")
    if "--" not in word:
        splits = {}
        for sh in word.replace("-", ""):
            if sh in flags["shorthands"]:
                flag = flags["shorthands"][sh]
                splits.update(makeOption("--"+flag, value if value else nextWord))
        return splits
    flag = word.replace("-", "")
    if flag in flags:
        flagDef = flags[flag]
        if flagDef[0] and not value:
            value = nextWord
            if not value:
                value = flagDef[1]
        return {flag: value}
