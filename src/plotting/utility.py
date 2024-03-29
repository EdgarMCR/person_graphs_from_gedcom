import os
import time
import logging
from copy import deepcopy as dc
from datetime import datetime as dt
from typing import Tuple, Optional, List
from dataclasses import dataclass

import matplotlib.pylab as plt
import matplotlib.patches as patches

from src.constants import Person, Family, Dimensions

DT_FMT = '%d/%m/%Y'

def get_non_dimensional_size(position: Tuple[float, float], dimensions: Tuple[float, float]) -> Tuple[float, float]:
    return position[0] / dimensions[0], position[1] / dimensions[1]


def get_dimensional_size(position: Tuple[float, float], dimensions: Tuple[float, float]) -> Tuple[float, float]:
    return position[0] * dimensions[0], position[1] * dimensions[1]


def get_string_for_event(date_str: str, date_dt: Optional[dt], place: str, prefix: str) -> str:
    date = get_date_string_for_event(date_str, date_dt)
    place = trim_place_length(place)

    if place and date:
        text = '{} {} {}'.format(prefix, date, place)
    elif place:
        text = '{} {}'.format(prefix, place)
    elif date:
        text = '{} {}'.format(prefix, date)
    else:
        text = ''
    return text


def get_two_line_string_for_event(date_str: str, date_dt: Optional[dt], place: str, prefix: str) -> (str, str):
    date = get_date_string_for_event(date_str, date_dt)
    place = trim_place_length(place)

    text1, text2 = '', ''
    if place and date:
        text1, text2 = f'{prefix} {date}', f'{place}'
    elif place:
        text1 = '{} {}'.format(prefix, place)
    elif date:
        text1 = '{} {}'.format(prefix, date)

    return text1, text2


def get_date_string_for_event(date_str: str, date_dt: Optional[dt]) -> str:
    if date_dt:
        date = date_dt.strftime(DT_FMT)
    else:
        date = date_str
    return date


def trim_place_length(place: Optional[str], max_len: int = 26) -> Optional[str]:
    if place and len(place) > max_len:
        parts = place.split(', ')
        place = ', '.join(parts[1:])
    return place


def get_box_dimensions_for_line(x1: float, y1: float, x2: float, y2: float, linewidth: float,
                                page_size: Tuple[float, float]) -> Dimensions:
    x, y = (x1 + x2) /2, (y1 + y2) / 2
    if x1 == x2:
        width, height = linewidth, abs(y1 - y2)
    else:
        width, height = abs(x1 - x2), linewidth
    dimension = Dimensions((x, y), width, height, page_size)
    return dimension


def prepare_for_plotting(person: Person, family_parents: Family, families: List[Family]) -> Tuple[Family, List[Family]]:
    pt = person.gedcom_element.get_pointer()

    for ii in range(len(families)):
        if families[ii].parent1.gedcom_element.get_pointer() == pt:
            families[ii].parent1, families[ii].parent2 = families[ii].parent2, families[ii].parent1

    if family_parents and families:
        family_parents.one_child_already_plotted = True
        children = []
        for child in family_parents.children:
            if child.gedcom_element.get_pointer() != pt:
                children.append(child)
        family_parents.children = children

    return family_parents, families
