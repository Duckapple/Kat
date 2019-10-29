from submit import submitFlags
from test import testFlags

def defineFlags():
    flags = {}
    flagNames = set()
    for flag in submitFlags + testFlags:
        if flag[0] not in flagNames:
            flagNames.add(flag[0])
            flags.update({flag[0]: flag[1]})
        elif flag[1] and flag not in flags:
            flags.update({flag[0]: flag[1]})
    
    shorthands = {}
    for flag in flags:
        letter = flag[0][0]
        if letter in shorthands:
            shorthands.update({letter: None})
        else:
            shorthands.update({letter: flag})

    flags["shorthands"] = shorthands

    return flags

flags = defineFlags()

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
        if flags[flag] and not value:
            value = nextWord
        return {flag: value}
        