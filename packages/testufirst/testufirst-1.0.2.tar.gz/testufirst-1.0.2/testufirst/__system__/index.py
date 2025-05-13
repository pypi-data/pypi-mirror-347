from testufirst.__system__.imports import *


class index:
    ####################################################################################// Load
    def __init__(self, app="", cwd="", args=[]):
        self.app, self.cwd, self.args = app, cwd, args
        # ...
        pass

    def __exit__(self):
        # ...
        pass

    ####################################################################################// Main
    def print(self):
        cli.hint(testusecond.print())

        version = importlib.metadata.version("testufirst")
        return f"First: " + version

    ####################################################################################// Helpers
