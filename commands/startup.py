from argparse import ArgumentParser, RawDescriptionHelpFormatter
from helpers.config import getConfig, saveConfig

# returns whether the step errored
# type step = () -> bool

def copyConfigStep():
    print("💾 Adding/updating configuration to your .kattisrc...")
    if not getConfig():
        print("""\
❌ Something went wrong in locating the configuration file
for kattis. Have you fetched the .kattisrc? Consult the 
README.md for more details.""")
        return False
    else:
        print("✅ Successfully added default configuration to your .kattisrc!")
        return True

def languageStep():
    cfg = getConfig()
    lang = cfg.get("kat", "language")
    allLangs = set(x.lower() for x in cfg["File associations"].values())
    iter(cfg["Run commands"])
    print('Choose your language')
    print('This tool works best with', ', '.join(cfg["Run commands"]))
    print('It also supports every language on Kattis, but you would need to tinker with the configurations to test optimally.')
    print('(These are', ', '.join(allLangs), ')')
    print('Leave blank for', lang)
    language = input('Your pick: ')
    cfg.set("kat", "language", language if language.lower() in allLangs else lang)
    return True

steps = [
    { 'fn': copyConfigStep, 'desc': 'Copy inbuilt configurations into your .kattisrc' },
    { 'fn': languageStep, 'desc': 'Choose the language you want to use' },
]

def startupCommand(data):
    skipsteps = data['skipstep'] if data['skipstep'] else []
    for i, v in enumerate(steps):
        if i in skipsteps:
            continue
        print('Step', i+1)
        result = v['fn']()
        if not result:
            print('Step', i, 'went wrong, exiting...')
            return
        print()
    saveConfig()

def startupParser(parsers: ArgumentParser):
    helpText = 'Copy configuration and initialize some user settings.'
    description = helpText + """
Useful if this is the first time using the tool, but also practical if some parts could use repeating.
Critically, you can skip steps with the optional argument.

Steps:
""" + '\n'.join([str(i+1) + ')  ' + step['desc'] for i, step in enumerate(steps)])
    parser = parsers.add_parser('startup', description=description, help=helpText, formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument('-s', '--skipstep', type=lambda x : int(x) - 1, help='Choose specific steps to skip.', nargs='*')