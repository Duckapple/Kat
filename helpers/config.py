import configparser, os, sys
from pathlib import Path

_DEFAULT_CONFIG = "/etc/kattis/submit/kattisrc"

def configLocations():
    return [
        _DEFAULT_CONFIG,
        os.path.join(str(Path.home()), ".kattisrc"),
        os.path.join(os.path.dirname(sys.argv[0]), ".kattisrc"),
        os.path.join(os.getcwd(), ".kattisrc")
    ]

def findConfig(config = None):
    locations = configLocations()

    found = []
    for location in locations:
        if os.path.exists(location):
            if config:
                config.read(location)
            found.append(location)
    return found

_CONFIG_NOT_FOUND_MSG = """\
I failed to read in a config file from your home directory or from the
same directory as this script. Please go to your Kattis installation
to download a .kattisrc file.

The file should look something like this:
[user]
username: yourusername
token: *********

[kattis]
loginurl: https://<kattis>/login
submissionurl: https://<kattis>/submit"""

class Config:
    """The config singleton, use getConfig to access."""
    __instance: dict = None
    __location = None
    @staticmethod
    def getInstance():
        if Config.__instance == None:
            Config()
        return Config.__instance
    def getLocation():
        if Config.__location == None:
            Config()
        return Config.__location
    @staticmethod
    def save():
        if Config.__instance == None:
            Config()
        with open(Config.__location, "w") as configFile:
            Config.__instance.write(configFile)
    def __init__(self):
        if Config.__instance != None:
            raise Exception("Config was tried initialized outside static scope.")
        else:
            _config = configparser.ConfigParser(converters={"array": strToArr, "command": toCommandArray})

            found = findConfig(_config)
            if not found:
                print("No config found, consider reading the readme or running 'kattis startup'")
                _config = preconfigure(_config)
            else:
                _config = preconfigure(_config, found[-1])
                Config.__location = found[-1]

            self = vars(_config)['_sections']
            Config.__instance = self

def getConfig():
    return Config.getInstance()

def getConfigWithLocation():
    return Config.getInstance(), Config.getLocation()

def saveConfig():
    _config = configparser.ConfigParser(converters={"array": strToArr, "command": toCommandArray})
    found = findConfig(_config)
    if not found:
        return False
    location = found[-1]

    cfg = getConfig()
    for (section, settings) in cfg.items():
        if section not in _config.sections():
            _config.add_section(section)
        for (key, value) in settings.items():
            _config[section][key] = value
    if location:
        with open(location, "w") as configFile:
            _config.write(configFile)
    return True

def getConfigUrl(option, default):
    cfg = getConfig()
    section = cfg.get("kattis", {})
    item = section.get(option)
    if item:
        return item
    else:
        return formatUrl(section.get("hostname", "open.kattis.com"), default)

def formatUrl(hostname, path):
    return "https://%s/%s" % (hostname, path)

def preconfigure(cfg, location = None):
    defaults = {
        "kat": {
            "language": "python",
            "workCommand": "",
        },
        "File associations": {
            ".c": "C",
            ".c#": "C#",
            ".cpp": "C++",
            ".cc": "C++",
            ".cs": "C#",
            ".cxx": "C++",
            ".c++": "C++",
            ".go": "Go",
            ".h": "C++",
            ".hs": "Haskell",
            ".java": "Java",
            ".js": "JavaScript",
            ".m": "Objective-C",
            ".pas": "Pascal",
            ".php": "PHP",
            ".pl": "Prolog",
            ".py": "Python",
            ".rb": "Ruby",
            ".rs": "Rust",
            ".fs": "F#",
            ".fsx": "F#",
            ".fsscript": "F#",
        },
        "Initialize commands": {
            "F#": "dotnet new console -lang F#",
            "C#": "dotnet new console",
            "Rust": "cargo init --name problem", # Can't spawn problems to call all projects 'problem', right?
        },
        "Run commands": {
            "Python": "python @f",
            "PHP": "php @f",
            "Java": "java @c",
            "C#": "dotnet run",
            "F#": "dotnet run",
            "C++": "@p",
            "Rust": "cargo run",
            "Haskell": "./@p",
            "Go": "go run @f",
            # TODO: Support rest of the languages that kattis supports
        },
        "Compile commands": {
            "Java": "javac @f",
            "C++" : "g++ @f -o @p",
            "Haskell": "ghc -ferror-spans -threaded -rtsopts @f -o @p",
        },
        "Naming": {
            "Java": "Pascal",
        },
        "Default options": {
            "archive": "archive",
            "config": "config",
            "contest": "",
            "get": "get",
            "list": "list",
            "read": "read",
            "startup": "startup",
            "submit": "submit",
            "test": "test",
            "unarchive": "unarchive",
            "watch": "watch",
            "work": "work",
        },
        "contest": {}
    }

    for (section, settings) in defaults.items():
        if section not in cfg.sections():
            cfg.add_section(section)
        for (key, value) in settings.items():
            _set(cfg[section], key, value)

    if location:
        with open(location, "w") as configFile:
            cfg.write(configFile)
    return cfg

def _set(cfgForSection, key, value):
    if not cfgForSection.get(key, False):
        cfgForSection[key] = value

def strToArr(string):
    string = string.replace("[","").replace("]","")
    string = string.replace("'","").replace('"',"")
    return [item.strip() for item in string.split(",")]

def toCommandArray(string: str):
    splitString = string.split(" ")
    return commandConvert(splitString)

def commandConvert(array: list):
    result = []
    cumulator = None
    for item in array:
        if item[0] == '"' or item[0] == "'":
            cumulator = item
        elif cumulator:
            cumulator += " " + item
            if cumulator[-1] == cumulator[0]:
                result.append(cumulator)
                cumulator = None
        else:
            result.append(item)
    return result
