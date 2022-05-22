""" Two step process of plotting: 1. find out where to put each box and line and then 2. plot it """
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
import src.plotting.utility as pu

DETAILS_FS = 6
GAP_REDUCTION = 0.7
INDENTATION = 0.05


def plot_family(stride: Tuple[float, float], dimensions: Dimensions, family: Family, child_start_y: float, fig,
                indent_spouse: int = 0) -> Tuple[float, float]:
    """ Position is for Mother (top box) """
    child_bottom = draw_family_lines(stride, dimensions, family, fig)

    mother = Person()
    if family.parent2:
        mother = family.parent2
    plot_person_box(dimensions, mother, fig)

    dim = dc(dimensions)
    x, y = dim.position[0], dim.position[1] - stride[1]
    x += indent_spouse * INDENTATION * dim.width

    dim.position = (x, y)
    father = Person()
    if family.parent1:
        father = family.parent1
    plot_person_box(dim, father, fig)

    gap = stride[1] - dimensions.height
    parent_bottom = y-gap
    return parent_bottom, child_bottom


def draw_family_lines(stride: Tuple[float, float], dimensions: Dimensions, family: Family, fig) -> float:

    mid_position = dimensions.position[1] - stride[1] / 2.
    gap = stride[1] - dimensions.height

    # line between parents
    dim = Dimensions((dimensions.position[0], mid_position), 0.01, stride[1], dimensions.page_size)
    plot_rectangle(dim, fig, plot_shadow=False)

    # vertical connecting line
    num_children = len(family.children)
    gap_reduction_factor = GAP_REDUCTION * gap

    xo, yo = dimensions.position
    x = xo + stride[0] / 2
    y_bottom = yo - (stride[1] - gap_reduction_factor) * (num_children - 1)
    if family.one_child_already_plotted:
        y_bottom -= stride[1] * 2

    y = (yo + y_bottom) / 2
    height = yo - y_bottom
    dim = Dimensions((x, y), 0.01, height, dimensions.page_size)
    plot_rectangle(dim, fig, plot_shadow=False)
    child_bottom = y_bottom + 0.5 * dimensions.height + gap

    # line marriage to right
    x1, y1 = dimensions.position[0], mid_position
    x2, y2 = x1 + stride[0] / 2, mid_position
    x, y = (x1 + x2)/2, (y1 + y2) / 2
    dim = Dimensions((x, y), stride[0] / 2, 0.01, dimensions.page_size)
    plot_rectangle(dim, fig, plot_shadow=False)

    # Children lines
    x, y = dimensions.position
    if family.one_child_already_plotted:
        xs, ys = x + stride[0], y - stride[1] * 2

        x_, y_ = x + (stride[0] * (3 / 4)), y
        dim = Dimensions((x_, y_), stride[0] / 2, 0.01, dimensions.page_size)
        plot_rectangle(dim, fig, plot_shadow=False)

    else:
        xs, ys = x + stride[0], y

    for ii in range(len(family.children)):
        x_, y_ = xs - (stride[0] / 4), ys - (stride[1] - gap_reduction_factor) * ii
        print('{}: {},{}'.format(ii, x_, y_))
        dim = Dimensions((x_, y_), stride[0] / 2, 0.01, dimensions.page_size)
        plot_rectangle(dim, fig, plot_shadow=False)

        # Plot children
        print(' " {},{}'.format(x_, y_))
        dim_ = dc(dimensions)
        dim_.position = (xs, y_)
        plot_person_box(dim_, family.children[ii], fig)

    # marriage box position
    dim = dc(dimensions)
    dim.position = (dim.position[0] + INDENTATION * dim.width, mid_position)
    dim.height = gap / 2

    left, right, top, bottom = plot_rectangle(dim, fig)
    x, y = left + (right - left) / 2, bottom + (top - bottom) / 2
    text = pu.get_string_for_event(family.marriage_date, family.marriage_place, 'm.')
    fig.text(x, y, text, ha='center', va='center', fontsize=DETAILS_FS)
    return child_bottom


def plot_rectangle(dimensions: Dimensions, fig, plot_shadow: bool = True):
    offset = dimensions.width * 0.03
    offset_x, offset_y = pu.get_non_dimensional_size((offset, offset), dimensions.page_size)

    x, y = pu.get_non_dimensional_size(dimensions.position, dimensions.page_size)
    w, h = pu.get_non_dimensional_size((dimensions.width, dimensions.height), dimensions.page_size)
    left, right = x - w / 2, x + w / 2
    top, bottom = y + h / 2, y - h / 2

    if plot_shadow:
        shadow_left, shadow_bottom = left + offset_x, bottom - offset_y
        p = patches.Rectangle((shadow_left, shadow_bottom), w, h, facecolor='gray', fill=True, alpha=0.5)
        fig.add_artist(p)

    p = patches.Rectangle((left, bottom), w, h, facecolor='white', edgecolor='k', fill=True)
    fig.add_artist(p)
    return left, right, top, bottom


def plot_person_box(dimensions: Dimensions, person: Person, fig):
    name_fs, details_fs = 12, 6

    left, right, top, bottom = plot_rectangle(dimensions, fig)

    x, y = left + (right - left) / 2, bottom + (top - bottom) * (7 / 12)
    text = '{} {}'.format(person.first_name, person.last_name)
    fig.text(x, y, text, ha='center', va='bottom', fontsize=name_fs, weight='bold')

    x, y = left + (right - left) / 2, bottom + (top - bottom) * (5 / 12)
    text = pu.get_string_for_event(person.birth_date, person.birth_place, 'b.')
    fig.text(x, y, text, ha='center', va='center', fontsize=details_fs)

    x, y = left + (right - left) / 2, bottom + (top - bottom) * (1 / 6)
    text = pu.get_string_for_event(person.death_date, person.death_place, 'd.')
    fig.text(x, y, text, ha='center', va='center', fontsize=details_fs)

