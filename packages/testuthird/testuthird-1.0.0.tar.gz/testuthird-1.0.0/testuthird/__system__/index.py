from testuthird.__system__.imports import *


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
    def third(self, param=""):  # (param) - Test demo method with param
        if not param:
            return "Invalid param!"

        version = importlib.metadata.version("testuthird")
        return f"Third {version}: {param}"

    ####################################################################################// Helpers
