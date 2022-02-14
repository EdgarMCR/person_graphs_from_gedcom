import os
import time
import logging
from copy import deepcopy as dc
from datetime import datetime as dt
from typing import Tuple, Optional
from dataclasses import dataclass
from unittest import TestCase

from src.constants import Person, Family, Dimensions
import src.plotting.utility as pu


class TestUtility(TestCase):
    def test_get_box_dimensions_for_line_1(self):
        x1, y1, x2, y2, linewidth, page_size = 10, 5, 10, 10, 0.01, (15, 15)
        expected = Dimensions((10, 7.5), 0.01, 5, page_size)
        result = pu.get_box_dimensions_for_line(x1, y1, x2, y2, linewidth, page_size)
        self.assertEqual(expected, result)

    def test_get_box_dimensions_for_line_2(self):
        x1, y1, x2, y2, linewidth, page_size = 5, 10, 10, 10, 0.01, (15, 15)
        expected = Dimensions((7.5, 10), 5, 0.01, page_size)
        result = pu.get_box_dimensions_for_line(x1, y1, x2, y2, linewidth, page_size)
        self.assertEqual(expected, result)
