from argparse import ArgumentParser
import os


def switchCommand(data):
    instance = data['instance'] and data['instance'].replace('.\\', '')
    allConfigs = [*filter(lambda x: x.endswith('kattisrc'), os.listdir())]
    rc, configs = splitRcs(allConfigs)
    if (not instance):
        if (len(configs) == 1):
            swapInstances(configs[0], rc)
        else:
            choose(configs, rc, 'configs')
    else:
        matches = [x for x in allConfigs if x.startswith(instance)]
        if (rc and len(matches) == 1 and rc != matches[0]):
            swapInstances(matches[0], rc)
        elif (len(matches) > 1):
            choose(matches, rc, 'matches')
        else:
            print(f"🤷 Could not find config '{instance}'")

def choose(choices, rc, choiceName = 'configs'):
    print(f'🔢 Found several {choiceName}:')
    for i, c in enumerate(choices):
        print(f'    {i+1}) {c}')
    x = input('Which do you choose? > ')
    if x.isdigit() and int(x) <= len(choices):
        swapInstances(choices[int(x) - 1], rc)
    elif x.strip() == '':
        print(f'❌ Aborted')
    else:
        print(f"🤷 Could not understand your choice.")

def swapInstances(other, rc):
    newName = getName(rc)
    if not newName:
        newName = input('✍  Please enter the new name of your current .kattisrc > ')
        if (not newName):
            print(f'❌ Aborted')
            return
        if (not newName.endswith('kattisrc')):
            newName = newName + '.kattisrc'

    if other.startswith(newName.split('.')[0]):
        print(f'❌ Aborted: Names {other} and {newName} too similar')
        return

    os.rename(rc, newName)
    os.rename(other, rc)

    print(f'🔁 Renamed old rc to {newName} and activated {other}')

def getName(rc):
    with open(rc, "r") as rc_file:
        for l in rc_file.readlines():
            if l.startswith('hostname'):
                name = l.split('=')[1].strip().split('.')[0]
                return f'{name}{rc}'

def splitRcs(rcs: list[str]):
    i = None
    try: i = rcs.index('kattisrc')
    except:
        try: i = rcs.index('.kattisrc')
        except: return None, rcs # if no file was found, return None for the file
    return rcs[i], rcs[:i] + rcs[i + 1:] # Otherwise, return the file with a list copy without the file


def switchParser(parsers: ArgumentParser):
    helpText = 'Switch Kattis instance.'
    descText = helpText + ' Useful if you have exercises on e.g. itu.kattis.com using problems from open.kattis.com, allowing you to use a single folder for both (or even more). It is (currently) required that the configs share folder with your problems.';
    parser = parsers.add_parser('switch', description=descText, help=helpText)
    parser.add_argument('instance', help='Name of instance to switch to', nargs='?')
