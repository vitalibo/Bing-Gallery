#!/usr/bin/env python3
import argparse
import http.client
import json
import os
import urllib.parse as urlparse

__version__ = '0.3.0'


def debug(log: str) -> None:
    if args.debug:
        print(log)


def request(host: str, url: str) -> bytes:
    try:
        conn = http.client.HTTPSConnection(host)
        conn.request('GET', url)

        response = conn.getresponse()
        if response.status / 100 != 2:
            raise http.client.HTTPException(f'{response.code} {response.reason}')

        return response.read()
    finally:
        debug(f'GET http://{host}{url} %s' %
              f'{response.code} {response.reason}' if 'response' in locals() else 'Unknown')


def set_desktop_picture(path: str) -> None:
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


def main(args: argparse.Namespace) -> None:
    host = 'www.bing.com'
    resolution = args.resolution.split(r'x')
    url = '/HPImageArchive.aspx?format={format}&idx={idx}&n={n}&pid=hp&uhd={uhd}&mkt={mkt}&uhdwidth={w}&uhdheight={h}' \
        .format(format='js', idx=args.offset, n=1, uhd=1, mkt=args.market, w=resolution[0], h=resolution[1])

    response = json.loads(request(host, url))
    image_url = response['images'][0]['url']
    image_name = urlparse.parse_qs(urlparse.urlparse(image_url).query)['id'][0]

    path = os.path.abspath(f'{args.output}/{image_name}')
    with open(path, 'wb') as f:
        f.write(request(host, image_url))

    if not args.dry_run:
        set_desktop_picture(path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Simple Python 3 script for download/change desktop picture based on Bing image archive.",
        epilog='Copyright (c) 2015-2019, Vitaliy Boyarsky. All rights reserved.',
        add_help=False)
    parser.add_argument('--offset', type=int, default=0, help="Position from which you want to start.")
    parser.add_argument('--market', type=str, default='en-US', help="Which of Bing markets you want to use.",
                        choices=['en-US', 'zh-CN', 'ja-JP', 'en-AU', 'en-UK', 'de-DE', 'en-NZ', 'en-CA'])
    parser.add_argument('--resolution', type=str, default='3840x2160', help="Allows you change resolution of image.")
    parser.add_argument("--dry-run", action="store_true", help="Allow only download picture.")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode.")
    parser.add_argument('--version', action='version', help="Show program's version number and exit.",
                        version=f'Bing Gallery v{__version__}')
    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                        help='Show this help message and exit.')
    parser.add_argument('output', type=str, help="Output location for downloads.")
    args = parser.parse_args()
    main(args)
