from imports import *


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
    def demo(self, param=""):  # (param) - Test demo method with param
        if not param:
            return "Invalid param!"

        cli.done(testufirst.first("first"))

        version = importlib.metadata.version("testumbrella")
        return f"Umbrella {version}: {param}"

    ####################################################################################// Helpers
