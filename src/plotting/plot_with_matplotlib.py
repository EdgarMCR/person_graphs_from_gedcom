from copy import deepcopy as dc
from datetime import datetime as dt
from typing import Tuple, Optional, List
from dataclasses import dataclass

import matplotlib.pylab as plt
import matplotlib.patches as patches
from matplotlib.figure import Figure

from src.constants import Person, Family, Dimensions, PageInfo, BoxPlotInfo, TextInfo, LinePlotInfo
import src.plotting.utility as pu


def plot_on_figure(page_info: PageInfo, boxes: List[BoxPlotInfo], lines: List[LinePlotInfo]) -> Figure:
    page_size = (page_info.page_width, page_info.page_height)
    fig = plt.figure(figsize=page_size)

    for line in lines:
        fig = plot_line(line, page_info, fig)
    for box in boxes:
        fig = plot_person_box(box, page_info, fig)
    return fig


def plot_person_box(box: BoxPlotInfo, page_info: PageInfo, fig: Figure) -> Figure:
    page_size = (page_info.page_width, page_info.page_height)
    left, right, top, bottom, fig = plot_rectangle(box.x, box.y, box.w, box.h, page_size, fig)

    if len(box.lines) == 3:
        x, y = left + (right - left) / 2, bottom + (top - bottom) * (13 / 24)
        fig.text(x, y, box.lines[0].text, ha='center', va='bottom', fontsize=box.lines[0].font_size, weight='bold')
        x, y = left + (right - left) / 2, bottom + (top - bottom) * (4 / 12)
        fig.text(x, y, box.lines[1].text, ha='center', va='bottom', fontsize=box.lines[1].font_size, weight='bold')
        x, y = left + (right - left) / 2, bottom + (top - bottom) * (1 / 12)
        fig.text(x, y, box.lines[2].text, ha='center', va='bottom', fontsize=box.lines[2].font_size, weight='bold')
    elif len(box.lines) == 1:
        x, y = left + (right - left) / 2, bottom + (top - bottom) / 2
        fig.text(x, y, box.lines[0].text, ha='center', va='center', fontsize=box.lines[0].font_size, weight='bold')

    return fig


def plot_line(line: LinePlotInfo, page_info: PageInfo, fig: Figure) -> Figure:
    page_size = (page_info.page_width, page_info.page_height)
    x1, y1 = line.start
    x2, y2 = line.end
    x, y = (x1 + x2)/2, (y1 + y2) / 2
    if x1 == x2:
        height = y2 - y1
        _, _, _, _, fig = plot_rectangle(x, y, line.width, height, page_size, fig)
    elif y1 == y2:
        width = x2 - x1
        _, _, _, _, fig = plot_rectangle(x, y, width, line.width, page_size, fig)
    return fig


def plot_rectangle(x: float, y: float, w: float, h: float, page_size: Tuple[float, float],
                   fig: Figure, plot_shadow: bool = True) -> Tuple[float, float, float, float, Figure]:
    offset = w * 0.01
    offset_x, offset_y = pu.get_non_dimensional_size((offset, offset), page_size)

    x, y = pu.get_non_dimensional_size((x, y), page_size)
    w, h = pu.get_non_dimensional_size((w, h), page_size)
    left, right = x - w / 2, x + w / 2
    top, bottom = y + h / 2, y - h / 2

    if plot_shadow:
        shadow_left, shadow_bottom = left + offset_x, bottom - offset_y
        p = patches.Rectangle((shadow_left, shadow_bottom), w, h, facecolor='gray', fill=True, alpha=0.5)
        fig.add_artist(p)

    p = patches.Rectangle((left, bottom), w, h, facecolor='white', edgecolor='k', fill=True)
    fig.add_artist(p)
    return left, right, top, bottom, fig

