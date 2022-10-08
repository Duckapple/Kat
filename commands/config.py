from argparse import ArgumentParser

from helpers.cli import yes
from helpers.config import getConfig, commandConvert, getConfigWithLocation, saveConfig

def configCommand(data):
    if 'section' not in data:
        print("Adding/updating configuration to your .kattisrc...")
        if not getConfig():
            print("""\
Something went wrong in locating the configuration file
for kattis. Have you fetched the .kattisrc? Consult the 
README.md for more details.""")
        else:
            print("Successfully added default configuration to your .kattisrc!")

    elif "value" in data:
        cfg, location = getConfigWithLocation()
        section = data["section"]
        option = data["option"]
        value = data["value"]
        if not cfg:
            print("""\
Something went wrong in locating the configuration file
for kattis. Have you fetched the .kattisrc? Consult the 
README.md for more details.""")
        elif section in cfg:
            cfgSection = cfg.get(section)
            if not option in cfgSection and section.lower() in ["kat", "kattis", "user"]:
                print("Setting", option, "was not recognized for section [" + section + "]")
            else:
                if section == "kat" and option == "language" and value.lower() not in [name.lower() for name in cfg["File associations"].values()]:
                    print("Warning, you are about to set your language to a language not recognized by kat tool. You will be unable to use kat tool if you do so. Do you want to continue?")
                    if not yes():
                        return
                cfgSection[option] = value
                if (section, option) == ("kattis", "hostname"):
                    print("You have changed your hostname. Would you like to change your loginurl, submissionurl and submissionsurl similarly? This is required for submitting.")
                    if yes():
                        prefix = "https://" + value + "/"
                        cfgSection["loginurl"] = prefix + "login"
                        cfgSection["submissionurl"] = prefix + "submit"
                        cfgSection["submissionsurl"] = prefix + "submissions"
                saveConfig()
                print("The setting", option, "from section [" + section + "]", "was set to", value)
        else:
            print("Section [" + section + "]", "was not found.")

    else:
        print("""\
Invalid number of arguments, expected 
'config <section> <option> <value>'. 
Remember to put arguments with spaces in quotes.""")

def configParser(parsers: ArgumentParser):
    helpText = 'Modify a configuration line.'
    parser = parsers.add_parser('config', description=helpText, help=helpText)
    parser.add_argument('section', help='The section of the config to access')
    parser.add_argument('option', help='The option to change')
    parser.add_argument('value', help='The updated value')
