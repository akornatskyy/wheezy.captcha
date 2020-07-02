import unittest

from wheezy.captcha.bezier import pascal_row


class BezierTestCase(unittest.TestCase):
    def test_pascal_row(self):
        samples = [
            [1],
            [1, 1],
            [1, 2.0, 1],
            [1, 3.0, 3.0, 1],
            [1, 4.0, 6.0, 4.0, 1],
            [1, 5.0, 10.0, 10.0, 5.0, 1],
            [1, 6.0, 15.0, 20.0, 15.0, 6.0, 1],
            [1, 7.0, 21.0, 35.0, 35.0, 21.0, 7.0, 1],
            [1, 8.0, 28.0, 56.0, 70.0, 56.0, 28.0, 8.0, 1],
            [1, 9.0, 36.0, 84.0, 126.0, 126.0, 84.0, 36.0, 9.0, 1]
        ]
        for i, expected in enumerate(samples):
            r = pascal_row(i)
            self.assertEqual(r, expected)
