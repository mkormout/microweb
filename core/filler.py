class Filler:

    def __init__(self, response):
        self.response = response

    def clear(self):
        del self.response

    def get_ctype(self, ctype: str = None) -> str:
        return self.response.content_type if self.response.content_type else ctype

    async def write(self, content) -> [str, int]:
        pass
