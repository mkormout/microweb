import ujson

from microweb.core.filler import Filler


class FillerDict(Filler):

    async def write(self, content) -> [str, int]:
        ctype = self.get_ctype('application/json; charset=utf-8')

        payload = ujson.dumps(content)

        await self.response.writer.awrite('Content-Type: %s\r\n' % ctype)
        await self.response.writer.awrite('Content-Length: %s\r\n' % len(payload))
        await self.response.writer.awrite('\r\n')

        await self.response.writer.awrite(payload)

        return ctype, len(payload)
