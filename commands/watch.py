from argparse import ArgumentParser
import os, time
from helpers.debounce import debounce
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent

from helpers.webutils import promptToFetch
from commands.test import testCommand
from helpers.programSelector import selectProgramFile, formatProgramFile


def watchCommand(data):
    problemName = data["problem"]
    directory = os.path.join(os.getcwd(), problemName)

    if not os.path.exists(problemName):
        promptToFetch(problemName)
        return

    # if programFile is not given, we will attempt to guess it
    programFile = (
        formatProgramFile(data["file"]) if "file" in data and data['file'] else selectProgramFile(problemName)
    )
    if not programFile:
        return

    event_handler = KatWatchEventHandler(problemName, programFile)

    observer = Observer()
    observer.schedule(event_handler, directory)
    observer.start()

    print("🕵️  Watching " + programFile["relativePath"] + " for changes")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


class KatWatchEventHandler(FileSystemEventHandler):
    def __init__(self, problemName, programFile):
        self.problemName = problemName
        self.programFile = programFile
        FileSystemEventHandler.__init__(self)

    def on_modified(self, event):
        if isinstance(event, FileModifiedEvent):
            self.runTests()

    @debounce(1)
    def runTests(self):
        testCommand({"problem": self.problemName, "file": self.programFile["relativePath"]})

def watchParser(parsers: ArgumentParser):
    helpText = 'Watch a problem, running a test on updates.'
    parser = parsers.add_parser('watch', description=helpText, help=helpText)
    parser.add_argument('problem', help='Name of problem to watch')
    parser.add_argument('file', nargs='?', help='Name of the specific file to watch')
