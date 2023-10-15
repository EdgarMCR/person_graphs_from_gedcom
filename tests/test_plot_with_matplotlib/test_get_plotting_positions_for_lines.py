import unittest

import src.plotting.plot_with_matplotlib as pwm


class Test(unittest.TestCase):
    def test_1(self):
        top, bottom = 1, 2
        line_ys = pwm.get_plotting_positions_for_lines(top, bottom, 2)
        self.assertEqual([1.25, 1.75], line_ys)

    def test_2(self):
        top, bottom = 1, 2
        line_ys = pwm.get_plotting_positions_for_lines(top, bottom, 4)
        expected = [1.125, 1.375, 1.625, 1.875]
        self.assertEqual(expected, line_ys)

    def test_3(self):
        top, bottom = 1, 2
        line_ys = pwm.get_plotting_positions_for_lines(top, bottom, 6)
        expected = [1.083333, 1.25, 1.416666, 1.583333, 1.749999, 1.916666]
        for ii in range(len(line_ys)):
            self.assertAlmostEqual(expected[ii], line_ys[ii], delta=0.00001)

    def test_4(self):
        top, bottom = 1, 2
        num_lines, size_ratios = 4, [1.5, 1.5, 1, 1]
        line_ys = pwm.get_plotting_positions_for_lines(top, bottom, num_lines, size_ratios)
        expected = [1.15, 1.45, 1.7, 1.9]
        for ii in range(len(line_ys)):
            self.assertAlmostEqual(expected[ii], line_ys[ii], delta=0.00001)
