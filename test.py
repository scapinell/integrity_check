import io
import io
import sys
import unittest
from unittest.mock import patch
from integrity_check import check_integrity


class TestCheckIntegityFunc(unittest.TestCase):

    def test_isequal(self):
        self.assertEqual(check_integrity('file1.txt md5 9e3b3e4829b69b4b02d5b3f7ecc6f9ad', 'files_to_check'),
                         'file1.txt OK')
        self.assertEqual(check_integrity('file2.txt md5 acc32e152b8b3c4ce5d6dcd9443a6864', 'files_to_check'),
                         'file2.txt OK')
        self.assertEqual(
            check_integrity('1.jpg sha256 60e6578a15fb6283a3d0a239ebab735466172987d43e054323cfd0ac240910a0',
                            'files_to_check'), '1.jpg OK')
        self.assertEqual(check_integrity('file3.txt sha1 acc32e152b8b3c4ce5d6dcd9443a6864', 'files_to_check'),
                         'file3.txt NOT FOUND')
        self.assertEqual(check_integrity('file4.txt sha256 123', 'files_to_check'),
                         'file4.txt FAIL')
        self.assertEqual(check_integrity('file5.txt sha1 65ecadeb3ba1fc635bd8ad6f8e589b5a335db662', 'files_to_check'),
                         'file5.txt OK')
        self.assertEqual(check_integrity('file6.txt skjhb vmlkghjfdvmlhjkgf', 'files_to_check'),
                         'Please use one of the following hash algorithms for the file6.txt: mda5, sha1, sha256')
        self.assertEqual(check_integrity('file7.txt sha1 8db71cd696665e530fb293c554bdae9e075e0aad', 'files_to_check'),
                         'file7.txt OK')
        self.assertEqual(check_integrity('file8.txt md5', 'files_to_check'),
                         'Please specify hash sum for the file8.txt')
        self.assertEqual(check_integrity('file9.txt ghj', 'files_to_check'),
                         'Please specify hash sum for the file9.txt')
        self.assertEqual(check_integrity('file10.txt dfgk hljskhgljkgslk', 'files_to_check'),
                         'Please use one of the following hash algorithms for the file10.txt: mda5, sha1, sha256')
        self.assertEqual(
            check_integrity('file11.txt sha256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 ffg',
                            'files_to_check'),
            'Something but hash algorithm and hash sum was specified for the file11.txt')
        self.assertEqual(check_integrity('war_and_peace.txt md5 24f13f44a3d91da2acdf8e92dba0cefa', 'files_to_check'),
                         'war_and_peace.txt OK')
        self.assertEqual(check_integrity('testgif.gif sha1 48c24373f3057aa731b78648223f6c5f72497e34', 'files_to_check'),
                         'testgif.gif OK')
        self.assertEqual(
            check_integrity('file12.txt sha1 cf7dd1ec00ee7515b485455421726de37fe33ac276efd994a60ec1c567502a49',
                            'files_to_check'),
            'file12.txt FAIL')


if __name__ == '__main__':
    unittest.main()
