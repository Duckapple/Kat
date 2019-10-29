import os, time
from debounce import debounce
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent

from get import promptToGet
from test import test
from programSelector import selectProgramFile, formatProgramFile


def watch(args, options):
    problemName = args[0]
    directory = os.path.join(os.getcwd(), problemName)

    if not os.path.exists(problemName):
        promptToGet(args, options)
        return

    # if programFile is not given, we will attempt to guess it
    programFile = (
        formatProgramFile(args[1]) if args[1:] else selectProgramFile(problemName)
    )
    if programFile == -1:
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
        test([self.problemName, self.programFile["relativePath"]], [])
