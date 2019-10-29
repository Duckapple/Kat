class ArgsParser:
    def __init__(self, argv):
        self.argv = argv

    def parse(self, availableFlags):
        self.defineFlags(availableFlags)
        self.divideArgs()

    def defineFlags(self, availableFlags):
        self.flags = {}
        flagNames = set()

        for flag in availableFlags:
            if flag[0] not in flagNames:
                flagNames.add(flag[0])
                self.flags.update({flag[0]: flag[1:]})
            elif flag[1] and flag not in flags:
                self.flags.update({flag[0]: flag[1:]})

        shorthands = {}
        for flag in self.flags:
            letter = flag[0][0]
            if letter in shorthands:
                shorthands.update({letter: None})
            else:
                shorthands.update({letter: flag})

        self.flags["shorthands"] = shorthands

    def divideArgs(self):
        self.args = []
        self.options = {}
        for i in range(0, len(self.argv)):
            word = self.argv[i]
            if "-" in word:
                otherWord = self.argv[i + 1] if i + 1 < len(self.argv) else None
                option = self.makeOption(word, otherWord)
                if option:
                    self.options.update(option)
            else:
                self.args.append(word)

    def makeOption(self, word, nextWord):
        flag = None
        value = None
        if "=" in word:
            word, value = word.split("=")
        if "--" not in word:
            splits = {}
            for sh in word.replace("-", ""):
                if sh in self.flags["shorthands"]:
                    flag = self.flags["shorthands"][sh]
                    splits.update(makeOption("--" + flag, value if value else nextWord))
            return splits
        flag = word.replace("-", "")
        if flag in self.flags:
            flagDef = self.flags[flag]
            if flagDef[0] and not value:
                value = nextWord
                if not value:
                    value = flagDef[1]
            return {flag: value}
