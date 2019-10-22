def printUsage():
    print("Usage: kattis [<OPTIONS>] <COMMAND> <ARGS>")


def printFullUsage():
    printUsage()
    print()
    print("COMMAND:")
    print("  get      Gets the argument problem test cases and prepares boilerplate")
    print("  test     Tests the argument problem against all test files")
    print("  submit   Submits the argument problem to the Kattis servers")
    print('  archive  Archives the problem in the ".archive"-folder')
    print("OPTIONS:")
    print("  -f       Force the action directly (applies to <submit>)")
    print("  -h       Prints the help message for the typed command")
    print(
        "  -a       Archives the problem after executing the command (applies to <submit> and <test>)"
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
Usage: kattis [<options>] submit <problem>

    Submits the argument problem to the Kattis servers

Options:
    -a    Archives the problem after executing the command
    -f    Force the action directly""",
    "test": """
Usage: kattis [<options>] test <problem>

    Tests the argument problem against all test files

Options:
    -a    Archives the problem after executing the command""",
}


def helpIfNotCommand(command):
    print("Whoops, did not recognize command " + command + ".")
    printHelp()
