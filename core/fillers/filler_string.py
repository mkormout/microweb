from microweb.core.filler import Filler


class FillerString(Filler):

    async def write(self, content) -> [str, int]:
        ctype = self.get_ctype('text/html; charset=utf-8')

        await self.response.writer.awrite('Content-Type: %s\r\n' % ctype)
        await self.response.writer.awrite('Content-Length: %s\r\n' % len(content))
        await self.response.writer.awrite('\r\n')

        await self.response.writer.awrite(content)

        return ctype, len(content)

