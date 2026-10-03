import unittest
from mlx_model_lab.matrix import expand
from mlx_model_lab.runner import command


class Tests(unittest.TestCase):
    def test_matrix(self):
        cfg = {"models":["a","b"],"prompt_files":["p"],"max_tokens":[64,128],"temperature":0}
        self.assertEqual(len(list(expand(cfg))), 4)

    def test_command_contains_model(self):
        self.assertIn("model-x", command("model-x", "hello", 10, 0.0))


if __name__ == "__main__":
    unittest.main()
