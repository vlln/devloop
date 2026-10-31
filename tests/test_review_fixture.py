"""Verify the deliberately faulty review fixture stays a useful eval seed.

The repository fixture must remain faulty. Agent repairs run in isolated copies;
these checks establish ground truth, not correctness of the faulty candidate.
"""
import importlib.util
import unittest
from pathlib import Path

FIXTURE = Path(__file__).resolve().parent / 'fixtures/review-project'


def load(name):
    spec = importlib.util.spec_from_file_location(name, FIXTURE / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ReviewGroundTruth(unittest.TestCase):
    def test_two_instances_share_one_seeded_arithmetic_fault(self):
        billing = load('billing')
        for function in (billing.checkout_total, billing.preview_total):
            self.assertEqual(function([11, 4], 3), 18)
            self.assertNotEqual(function([11, 4], 3), 12)
            self.assertEqual(function([11, 4]), 15)
        self.assertEqual(billing.checkout_total([11, 4], 3),
                         billing.preview_total([11, 4], 3))

    def test_label_is_a_clean_intentional_behavior_control(self):
        labels = load('labels')
        for value in (-7, '<b>&</b>', None, [1, -2]):
            with self.subTest(value=value):
                self.assertEqual(labels.render_label(value), str(value))


if __name__ == '__main__':
    unittest.main()
