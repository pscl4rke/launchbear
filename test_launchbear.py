

import unittest

import launchbear


class TestLaunchbear(unittest.TestCase):

    def test_corrupted_cache_files_are_handled(self):
        # there are lots of ways they could be corrupt, just try empty:
        cache = launchbear.load_cachefile(cache_path="/dev/null")
        self.assertEqual(len(cache['generators']), 0)


if __name__ == '__main__':
    unittest.main()
