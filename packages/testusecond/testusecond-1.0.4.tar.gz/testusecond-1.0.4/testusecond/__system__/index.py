from testusecond.__system__.imports import *


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
        cli.hint(testuthird.print())

        version = importlib.metadata.version("testusecond")
        return f"Second: " + version

    ####################################################################################// Helpers
