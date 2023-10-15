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
        fig = plot_person_box_2(box, page_info, fig)

    return fig


def get_plotting_positions_for_lines(top: float, bottom: float, num_lines: int,
                                     line_ratios: Optional[List] = None):
    if line_ratios is None:
        line_ratios = [1] * num_lines

    height = bottom - top
    gap = height / sum(line_ratios)

    positions = []
    previous_bottom = top
    for ii in range(num_lines):
        gap_ = gap * line_ratios[ii]
        pos = previous_bottom + gap_/2
        previous_bottom = previous_bottom + gap_
        positions.append(pos)
    return positions


def plot_person_box(box: BoxPlotInfo, page_info: PageInfo, fig: Figure) -> Figure:
    page_size = (page_info.page_width, page_info.page_height)
    left, right, top, bottom, fig = plot_rectangle(box.x, box.y, box.w, box.h, page_size, fig)

    if len(box.lines) == 3:
        x, y = left + (right - left) / 2, bottom + (top - bottom) * (13 / 24)
        fig.text(x, y, box.lines[0].text, ha='center', va='bottom', fontfamily='serif', fontsize=box.lines[0].font_size, weight='bold')
        x, y = left + (right - left) / 2, bottom + (top - bottom) * (4 / 12)
        fig.text(x, y, box.lines[1].text, ha='center', va='bottom', fontfamily='serif', fontsize=box.lines[1].font_size)
        x, y = left + (right - left) / 2, bottom + (top - bottom) * (1 / 12)
        fig.text(x, y, box.lines[2].text, ha='center', va='bottom', fontfamily='serif', fontsize=box.lines[2].font_size)
    elif len(box.lines) == 1:
        x, y = left + (right - left) / 2, bottom + (top - bottom) / 2
        fig.text(x, y, box.lines[0].text, ha='center', va='center', fontfamily='serif', fontsize=box.lines[0].font_size)

    return fig


def get_line_ratios(lines: List[TextInfo], bold_line_factor: float = 1.1):
    line_ratios = []
    for line in lines:
        if line.text:
            if line.bold:
                line_ratios.append(bold_line_factor)
            else:
                line_ratios.append(1.)
    return line_ratios


def plot_person_box_2(box: BoxPlotInfo, page_info: PageInfo, fig: Figure) -> Figure:
    """ Improve this to remove empty space. """
    page_size = (page_info.page_width, page_info.page_height)
    left, right, top, bottom, fig = plot_rectangle(box.x, box.y, box.w, box.h, page_size, fig)

    x = left + (right - left) / 2
    if len(box.lines) == 3:
        x, y = left + (right - left) / 2, bottom + (top - bottom) * (7 / 12)
        fig.text(x, y, box.lines[0].text, ha='center', va='bottom', fontfamily='serif', fontsize=box.lines[0].font_size, weight='bold')
        x, y = left + (right - left) / 2, bottom + (top - bottom) * (7 / 24)
        fig.text(x, y, box.lines[1].text, ha='center', va='bottom', fontfamily='serif', fontsize=box.lines[1].font_size)
        x, y = left + (right - left) / 2, bottom + (top - bottom) * (1 / 24)
        fig.text(x, y, box.lines[2].text, ha='center', va='bottom', fontfamily='serif', fontsize=box.lines[2].font_size)

    elif len(box.lines) == 1:
        x, y = left + (right - left) / 2, bottom + (top - bottom) / 2
        fig.text(x, y, box.lines[0].text, ha='center', va='center', fontfamily='serif', fontsize=box.lines[0].font_size)

    else:
        plot_text_in_box(fig, box.lines, left, right, top, bottom)

    return fig


def plot_text_in_box(fig, lines, left, right, top, bottom):
    x = left + (right - left) / 2
    line_ratios = get_line_ratios(lines, bold_line_factor=1.1)
    leng = len(line_ratios)

    if leng == 0:
        return

    height = bottom - top
    top_, bottom_ = top + height * 0.02, bottom - height * 0.02
    y_pos = get_plotting_positions_for_lines(top_, bottom_, leng, line_ratios)

    count = 0
    for ii, line in enumerate(lines):
        if not line.text:
            continue

        y = y_pos[count]
        if line.bold:
            fig.text(x, y, line.text, ha='center', va='center', fontfamily='serif',
                     fontsize=line.font_size, weight='bold')
        else:
            fig.text(x, y, line.text, ha='center', va='center', fontfamily='serif',
                     fontsize=line.font_size)

        count += 1


def plot_line(line: LinePlotInfo, page_info: PageInfo, fig: Figure) -> Figure:
    page_size = (page_info.page_width, page_info.page_height)
    x1, y1 = line.start
    x2, y2 = line.end
    x, y = (x1 + x2)/2, (y1 + y2) / 2
    if x1 == x2:
        height = y2 - y1
        _, _, _, _, fig = plot_rectangle(x, y, line.width, height, page_size, fig, plot_shadow=False)
    elif y1 == y2:
        width = x2 - x1
        _, _, _, _, fig = plot_rectangle(x, y, width, line.width, page_size, fig, plot_shadow=False)
    return fig


def plot_rectangle(x: float, y: float, w: float, h: float, page_size: Tuple[float, float],
                   fig: Figure, plot_shadow: bool = True) -> Tuple[float, float, float, float, Figure]:
    offset = w * 0.02
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

