import unittest
from mlx_model_lab.matrix import expand
from mlx_model_lab.jobs import make_job
from mlx_model_lab.report import summarize


class Tests(unittest.TestCase):
    def test_ids_are_stable(self):
        a = make_job(experiment="x", model="m", prompt_file="p", max_tokens=64,
                     temperature=0, repeat=0, mode="warm")
        b = make_job(experiment="x", model="m", prompt_file="p", max_tokens=64,
                     temperature=0, repeat=0, mode="warm")
        self.assertEqual(a.id, b.id)

    def test_matrix_size(self):
        rows = expand({
            "name":"x", "models":["a","b"], "prompt_files":["p"],
            "max_tokens":[64,128], "temperature":[0], "mode":["warm"], "repeats":2
        })
        self.assertEqual(len(rows), 8)

    def test_report(self):
        rows = [
            {"ok":True,"experiment":"e","model":"m","prompt_file":"p","max_tokens":64,"mode":"warm","elapsed_seconds":1},
            {"ok":True,"experiment":"e","model":"m","prompt_file":"p","max_tokens":64,"mode":"warm","elapsed_seconds":3},
        ]
        out = summarize(rows)
        self.assertEqual(out[0]["median_seconds"], 2)


if __name__ == "__main__":
    unittest.main()
