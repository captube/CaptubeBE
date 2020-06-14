import re


class YoutubeIdParser:
    def parse(self, url):
        regex = re.compile(
            r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?(?P<id>[A-Za-z0-9\-=_]{11})')

        match = regex.match(url)

        if not match:
            raise Exception(f'Couldn\'t find youtube id for ${url}')
        return match.group('id')
