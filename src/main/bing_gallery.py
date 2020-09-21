#!/usr/bin/env python3

import argparse
import http.client
import json
import urllib.parse as urlparse
from pathlib import Path

__version__ = '0.4.0'


class Bing:

    def __init__(self, host='www.bing.com'):
        self.host = host

    def describe(self, idx: int, mkt: str, uhd_width: int = 3072, uhd_height: int = 1920,
                 format: str = 'js', n: int = 1, pid: str = 'hp', uhd: int = 1) -> dict:
        response = self._get_request(f'/HPImageArchive.aspx?format={format}&idx={idx}&n={n}&pid={pid}'
                                     f'&uhd={uhd}&mkt={mkt}&uhdwidth={uhd_width}&uhdheight={uhd_height}')
        return json.loads(response)['images'][0]

    def download(self, url: str, path: Path) -> str:
        path.mkdir(parents=True, exist_ok=True)
        with open(path.joinpath(urlparse.parse_qs(urlparse.urlparse(url).query)['id'][0]), 'wb') as f:
            f.write(self._get_request(url))
            return f.name

    def _get_request(self, url: str) -> bytes:
        conn = http.client.HTTPSConnection(self.host)
        conn.request('GET', url)
        response = conn.getresponse()
        if response.getcode() / 100 != 2:
            raise http.client.HTTPException('request failed with status: {code} {reason}'.format(
                code=response.getcode(), reason=response.reason))
        return response.read()


class Desktop:

    @staticmethod
    def change_background(path: str) -> None:
        import platform
        if platform.system() == 'Darwin':
            import subprocess
            subprocess.Popen("""/usr/bin/osascript<<END
tell application "Finder"
set desktop picture to POSIX file "{path}"
end tell
END""".format(path=path), shell=True)

        elif platform.system() == 'Windows':
            import ctypes
            ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 3)

        else:
            raise OSError('os unsupported')


def parse_args():
    parser = argparse.ArgumentParser(
        description='Command-line tool for change a desktop picture based on daily Bing images',
        epilog='Copyright (c) 2015-2020, Vitaliy Boyarsky', add_help=False)
    parser.add_argument('--offset', type=int, default=0, choices=range(0, 8),
                        help='Specify index of photo to use.')
    parser.add_argument('--market', type=str, default='en-US',
                        choices=['en-US', 'zh-CN', 'ja-JP', 'en-AU', 'en-UK', 'de-DE', 'en-NZ', 'en-CA'],
                        help='Specify market that you want to use.')
    parser.add_argument('--output', type=str, default=f'{Path.home()}/Pictures/Bing/',
                        help='Output folder for storing images.')
    parser.add_argument('--version', action='version', version=f'Bing Gallery v{__version__}',
                        help='Display the version of this tool.')
    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                        help='Show this help message.')
    return parser.parse_args()


def main(args=parse_args()):
    bing = Bing()
    image = bing.describe(idx=args.offset, mkt=args.market)
    path = bing.download(image['url'], path=Path(args.output))
    Desktop.change_background(path)


if __name__ == '__main__':
    main()
