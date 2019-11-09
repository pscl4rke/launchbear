

import unittest, tempfile

import launchbear


class TestLaunchbear(unittest.TestCase):

    def test_corrupted_cache_files_are_handled(self):
        # there are lots of ways they could be corrupt, just try empty:
        cache = launchbear.load_cachefile(cache_path="/dev/null")
        self.assertEqual(len(cache['generators']), 0)


class TestCacheFile(unittest.TestCase):

    def test_saving_and_loading(self):
        with tempfile.NamedTemporaryFile() as cachefile:
            initially = {'generators': {}}
            launchbear.save_cachefile(initially, cache_path=cachefile.name)
            after = launchbear.load_cachefile(cache_path=cachefile.name)
        self.assertEqual(initially, after)


if __name__ == '__main__':
    unittest.main()
