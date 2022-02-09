import utime

from microweb.core.request import Request
from microweb.core.response import Response
from microweb.lib.stdout import Color


def get_color(code: int):
    if code >= 500:
        return Color.FAIL
    elif code >= 400:
        return Color.WARNING
    elif code >= 300:
        return Color.OKCYAN
    elif code >= 200:
        return Color.OKGREEN
    else:
        return Color.HEADER


async def response_log(request: Request, response: Response):

    def log_response(r):
        time = utime.ticks_ms()
        status_color = get_color(r.http_status)
        route = ('%s%s %s%s - ' % (
            Color.HEADER,
            r.route.method,
            r.route.path,
            Color.ENDC,
        )) if r.route else ''
        print('[%s%s%s]: %s%s - %s%s%s - %s bytes' % (
            Color.OKCYAN,
            time,
            Color.ENDC,
            status_color,
            r.http_status,
            Color.ENDC,
            route,
            r.content_type,
            r.content_length
        ))

    response.on_send.observe(log_response)

    return True
