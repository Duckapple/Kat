from argparse import ArgumentParser
import os, time
from helpers.debounce import debounce
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent

from helpers.webutils import promptToFetch
from commands.test import testCommand, testFlags
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

    observer = Observer()
    event_handler = KatWatchEventHandler({**data, "file": programFile["relativePath"]}, observer)

    observer.schedule(event_handler, directory)
    observer.start()

    print("🕵️  Watching " + programFile["relativePath"] + " for changes. Press Ctrl+C to terminate.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


class KatWatchEventHandler(FileSystemEventHandler):
    def __init__(self, data, observer):
        self.data = data
        self.observer = observer
        self.fileType = self.data["file"].split('.')[-1]
        FileSystemEventHandler.__init__(self)

    def on_modified(self, event):
        if isinstance(event, FileModifiedEvent):
            isLangType = event.src_path.endswith(self.fileType)
            if isLangType:
                self.runTests()

    @debounce(1)
    def runTests(self):
        shouldEnd = testCommand(self.data)
        if shouldEnd:
            print('Done testing, stopping due to successful end.')
            os._exit(0)
        print('Done testing, still watching...')

def watchParser(parsers: ArgumentParser):
    helpText = 'Watch a problem, running tests on updates.'
    parser = parsers.add_parser('watch', description=helpText, help=helpText)
    testFlags(parser)
