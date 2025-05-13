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
    def print(self):
        version = importlib.metadata.version("testumbrella")

        cli.hint(testufirst.print())

        return "Umbrella: " + version

    def next(self):
        return SemVer.umbrella(
            "1.0.1",
            [
                "1.0.1",
                "1.0.1",
                "1.0.1",
            ],
            [
                "1.0.1",
                "1.0.5",
                "1.0.1",
            ],
        )

    ####################################################################################// Helpers
