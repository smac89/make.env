import unittest, shutil
import tempfile
from make_env import load_make_env
import os


class MakeEnv(unittest.TestCase):
    def setUp(self) -> None:
        self.test_dir = tempfile.mkdtemp()
        self.current_dir = os.curdir
        os.chdir(self.test_dir)

    def tearDown(self) -> None:
        os.chdir(self.current_dir)
        shutil.rmtree(self.test_dir)

    def test_dot_env_is_loaded(self) -> None:
        with open(os.path.join(self.test_dir, ".env"), "w") as f:
            f.write("TEST_VAR=test_value")
        load_make_env(["make.env"])
        self.assertIn("TEST_VAR", os.environ)
        self.assertEqual(os.environ["TEST_VAR"], "test_value")

    def test_empty_value_not_ignored(self) -> None:
        with open(os.path.join(self.test_dir, ".env"), "w") as f:
            f.write("TEST_VAR=")
        load_make_env(["make.env"])
        self.assertEqual(os.environ["TEST_VAR"], "")

    def test_special_value_remains(self) -> None:
        with open(os.path.join(self.test_dir, ".env"), "w") as f:
            f.write("TEST_VAR='4dabfs#a%d73w$Z2TBN4!nYD4Y$TW'")
        load_make_env(["make.env"])
        self.assertEqual(os.environ["TEST_VAR"], "4dabfs#a%d73w$Z2TBN4!nYD4Y$TW")
