from microweb.core.request import Request
from microweb.core.response import Response
from microweb.lib.node import CompositeNode, Node

Handler = [[Request, Response], bool]


class Handleable:

    def match(self, request: Request):
        pass

    async def handle(self, request: Request, response: Response):
        pass


class HandleableContainer(CompositeNode, Handleable):
    pass


class HandleableNode(Node, Handleable):

    def __init__(self, handler: Handler):
        super().__init__()
        self.handler = handler
