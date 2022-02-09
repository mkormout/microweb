import ure as re

from microweb.core.logger import logger
from microweb.lib.url import build


class Buildable:
    path: str
    recipe: str
    pattern: any
    params: list

    def build(self, path: str = None, start: bool = True, end: bool = True):
        path = path + self.path if path else self.path

        self.recipe, self.params = build(path=path, start=start, end=end)

        logger.debug('route: compiling: %s to %s with params %s' % (path, self.recipe, self.params))

        self.pattern = re.compile(self.recipe)
