import http.client
import unittest
from pathlib import Path
from unittest import mock

from bing_gallery import Bing, Desktop, main


class BingTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.bing = Bing()

    def test_describe(self):
        with open('resources/bing_response.json', 'r') as f:
            self.bing._get_request = mock.MagicMock()
            self.bing._get_request.return_value = f.read()

            actual = self.bing.describe(idx=0, mkt='eu_US')

            self.assertTrue(actual['url'].startswith('/th?id=OHR.WatkinsGlen_EN-US1837020817_UHD.jpg'))
            self.assertEqual(actual['title'], 'Wandering Watkins Glen')
            self.bing._get_request.assert_called_once()
            url = self.bing._get_request.call_args[0][0]
            self.assertEqual(url, '/HPImageArchive.aspx?'
                                  'format=js&idx=0&n=1&pid=hp&uhd=1&mkt=eu_US&uhdwidth=3072&uhdheight=1920')

    def test_download(self):
        with mock.patch('builtins.open', mock.mock_open()) as mock_file, \
                mock.patch.object(Path, 'mkdir') as mock_mkdir:
            self.bing._get_request = mock.MagicMock()
            self.bing._get_request.return_value = b'image_binary'

            actual = self.bing.download('/th?id=OHR.WatkinsGlen_EN-US1837020817_UHD.jpg&rf=LaDigue_UHD.jpg',
                                        Path('foo'))

            mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
            mock_file.assert_called_once_with(Path('foo/OHR.WatkinsGlen_EN-US1837020817_UHD.jpg'), 'wb')
            handler = mock_file()
            handler.write.assert_called_once_with(b'image_binary')
            self.assertEqual(actual, handler.name)

    def test_get_request(self):
        with mock.patch('http.client.HTTPSConnection', autospec=True) as mock_https_connection:
            mock_connection = mock_https_connection.return_value
            mock_response = mock.MagicMock()
            mock_connection.getresponse.return_value = mock_response
            mock_response.getcode.return_value = 200
            mock_response.read.return_value = b'foo'

            actual = self.bing._get_request('example.com')

            self.assertEqual(actual, b'foo')
            mock_connection.request.assert_called_once_with('GET', 'example.com')
            mock_connection.getresponse.assert_called_once()
            mock_response.getcode.assert_called_once()
            mock_response.read.asssert_called_once()

    def test_get_request_failed(self):
        with mock.patch('http.client.HTTPSConnection', autospec=True) as mock_https_connection:
            mock_connection = mock_https_connection.return_value
            mock_response = mock.MagicMock()
            mock_connection.getresponse.return_value = mock_response
            mock_response.getcode.return_value = 500
            mock_response.reason = 'Internal Server Error'
            mock_response.read.return_value = b'foo'

            with self.assertRaisesRegex(expected_exception=http.client.HTTPException,
                                        expected_regex='Internal Server Error'):
                self.bing._get_request('example.com')

            mock_connection.request.assert_called_once_with('GET', 'example.com')
            mock_connection.getresponse.assert_called_once()


class DesktopTestCase(unittest.TestCase):

    def test_change_background_unknown_os(self):
        with mock.patch('platform.system') as mock_system:
            mock_system.return_value = 'Linux'

            with self.assertRaisesRegex(expected_exception=OSError, expected_regex='os unsupported'):
                Desktop.change_background('foo')

    def test_change_background_macos(self):
        with mock.patch('platform.system') as mock_system, \
                mock.patch('subprocess.Popen') as mock_subprocess:
            mock_system.return_value = 'Darwin'

            Desktop.change_background('foo')

            actual = mock_subprocess.call_args[0][0]
            self.assertEqual(actual, """/usr/bin/osascript<<END
tell application "Finder"
set desktop picture to POSIX file "foo"
end tell
END""")


class BingGalleryTestCase(unittest.TestCase):

    def test_main(self):
        with mock.patch('bing_gallery.Bing') as mock_bing, \
                mock.patch('bing_gallery.Desktop.change_background') as mock_change_background:
            mock_args = mock.MagicMock()
            mock_args.offset = 1
            mock_args.market = 'ru_RU'
            mock_args.output = 'bar'
            mock_bing = mock_bing.return_value
            mock_bing.describe.return_value = {'url': 'foo'}
            mock_bing.download.return_value = 'new_path'

            main(mock_args)

            mock_bing.describe.assert_called_once_with(idx=1, mkt='ru_RU')
            mock_bing.download.assert_called_once_with('foo', path=Path('bar'))
            mock_change_background.assert_called_once_with('new_path')
