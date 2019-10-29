def printUsage():
    print("Usage: kattis [<OPTIONS>] <COMMAND> <ARGS>")


def printFullUsage():
    printUsage()
    print()
    print("COMMAND:")
    print("  get      Gets the argument problem test cases and prepares boilerplate")
    print("  test     Tests the argument problem against all test files")
    print("  submit   Submits the argument problem to the Kattis servers")
    print("  archive  Archives the problem in the '.archive'-folder")
    print("  list     Lists some problems directly from Kattis")

    print("OPTIONS:")
    print("  -h       Prints the help message for the typed command")
    print(
        "  -a       Archives the problem after executing the command if successful (applies to <submit> and <test>)"
    )


def printHelp(command):
    string = helpCommand.get(command, "")
    if string == "":
        printFullUsage()
    else:
        print(string)


helpCommand = {
    "archive": """
Usage: kattis [<options>] archive <problem>

    Archives the problem in the \".archive\"-folder""",
    "get": """
Usage: kattis [<options>] get <problem>

    Gets the argument problem test cases and prepares boilerplate""",
    "submit": """
Usage: kattis [<options>] submit <problem> [filePath]

    Submits the argument problem to the Kattis servers.
    If multiple supported source files are present within the problem 
    directory, you will be prompted to choose one. Alternativly you 
    can supply the path to your chosen script as a second argument.

Options:
    -a    Archives the problem after executing the command""",
    "test": """
Usage: kattis [<options>] test <problem> [filePath]

    Tests the argument problem against all test files.
    If multiple supported source files are present within the problem 
    directory, you will be prompted to choose one. Alternativly you 
    can supply the path to your chosen script as a second argument.

Options:
    -a    Archives the problem after executing the command""",
    "list": """
Usage: kattis list [<sorting>] [<filter>]
    
    Lists problems directly from Kattis according to some criteria. 
    Sorting and filtering can be applied in any order, and multiple 
    filters can be applied.
    
Sortings:
    easiest  Sorts the problems by ascending difficulty
    hardest  Sorts the problems by descending difficulty
    
Filters:
    unsolved
    solved
    untried
    tried""",
}


def helpIfNotCommand(command):
    print("Whoops, did not recognize command " + command + ".")
    printHelp(command)
