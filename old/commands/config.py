from helpers.config import getConfig, commandConvert

def configCommand(args, options):
    if len(args) == 0:
        print("Adding/updating configuration to your .kattisrc...")
        if getConfig() == -1:
            print("""\
Something went wrong in locating the configuration file
for kattis. Have you fetched the .kattisrc? Consult the 
README.md for more details.""")
        else:
            print("Successfully added default configuration to your .kattisrc!")

    elif len(args) == 3:
        cfg, location = getConfig(shouldReturnLocation=True)
        if type(cfg) is int:
            print("""\
Something went wrong in locating the configuration file
for kattis. Have you fetched the .kattisrc? Consult the 
README.md for more details.""")
        elif cfg.has_section(args[0]):
            if not cfg.has_option(args[0], args[1]) and args[0].lower() in ["kat", "kattis", "user"]:
                print("Setting", args[1], "was not recognized for section [" + args[0] + "]")
            else:
                cfg.set(args[0], args[1], args[2])
                with open(location, "w") as configFile:
                    cfg.write(configFile)
                print("The setting", args[1], "from section [" + args[0] + "]", "was set to", args[2])
        else:
            print("Section [" + args[0] + "]", "was not found.")

    else:
        print("""\
Invalid number of arguments, expected 
'config <section> <option> <value>'. 
Remember to put arguments with spaces in quotes.""")