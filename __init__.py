from microweb.core.application import Application
from microweb.core.router import Router
from microweb.core.static import Static


def app():
    return Application()


def router():
    return Router()


def static(root: str, options: dict = None):
    return Static(root, options)
