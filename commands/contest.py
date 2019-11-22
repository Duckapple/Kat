
def contestCommand(args, options):

    if(len(args) == 0):
        raise RuntimeError(
            "No argument given. Must be either start [url] or end"
        )

    arg = args[0]

    if(arg == "start" and len(args) > 1):
        startContest(args[1])
    elif(arg == "end"):
        endContest()
    else:
        raise RuntimeError(
            "Invalid argument '{}'. Must be either start [url] or end".format(
                arg
            )
        )


def startContest(contestUrl):
    # If already in contest mode, exit with warning

    # Decide if input is full url or simply an id

    # if only id, assume open kattis, them make url

    # write new contest to config file

    print("Starting contest with url {}".format(contestUrl))


def endContest():
    print("Ending contest")
    # remove contest from config if exist (perhaps warning if not in contest mode)
    pass
