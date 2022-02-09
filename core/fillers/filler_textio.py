from microweb.core.filler import Filler

BUFFER_CHUNK_LENGTH = 512


class FillerTextIO(Filler):

    async def write(self, content) -> [str, int]:
        ctype = self.get_ctype('application/octet-stream')

        await self.response.writer.awrite('Content-Type: %s\r\n' % ctype)
        # TODO: how to get stream length?
        #  await self.response.writer.awrite('Content-Length: %s\r\n' % len(fillers))
        await self.response.writer.awrite('\r\n')

        buffer = bytearray(BUFFER_CHUNK_LENGTH)

        total = 0

        while True:
            length = content.readinto(buffer)

            if not length:
                break

            await self.response.writer.awrite(buffer, 0, length)

            total += length

        return ctype, total
