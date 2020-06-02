import unittest
from kgtk.cli_entry import cli_entry
from kgtk.cli.dummy import run
from kgtk.exceptions import KGTKException


class TestDummy(unittest.TestCase):
    def test_module(self):
        # test separate module files
        pass

    def test_run(self):
        # test run function
        # exceptions here are not trapped by KGTKExceptionHandler
        with self.assertRaises(KGTKException):
            run(name="kgtk", info=None, error=True, _debug=False)

    def test_cli(self):
        # test command from cli entry
        assert cli_entry("kgtk", "dummy", "normal_test") == 0
        assert cli_entry("kgtk", "dummy", "test_exception", "-e") != 0


if __name__ == "__main__":
    unittest.main()
