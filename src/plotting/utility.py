import os
import time
import logging
from copy import deepcopy as dc
from datetime import datetime as dt
from typing import Tuple, Optional
from dataclasses import dataclass

import matplotlib.pylab as plt
import matplotlib.patches as patches

from src.constants import Person, Family, Dimensions


def get_non_dimensional_size(position: Tuple[float, float], dimensions: Tuple[float, float]) -> Tuple[float, float]:
    return position[0] / dimensions[0], position[1] / dimensions[1]


def get_dimensional_size(position: Tuple[float, float], dimensions: Tuple[float, float]) -> Tuple[float, float]:
    return position[0] * dimensions[0], position[1] * dimensions[1]


def get_string_for_event(date: Optional[dt], place: str, prefix: str) -> str:
    if date:
        text = '{} {} {}'.format(prefix, date.strftime('%d/%m/%Y'), place)
    else:
        text = '{} {}'.format(prefix, place)
    return text


def get_box_dimensions_for_line(x1: float, y1: float, x2: float, y2: float, linewidth: float,
                                page_size: Tuple[float, float]) -> Dimensions:
    x, y = (x1 + x2) /2, (y1 + y2) / 2
    if x1 == x2:
        width, height = linewidth, abs(y1 - y2)
    else:
        width, height = abs(x1 - x2), linewidth
    dimension = Dimensions((x, y), width, height, page_size)
    return dimension