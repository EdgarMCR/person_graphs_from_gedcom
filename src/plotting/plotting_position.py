from copy import deepcopy as dc
from datetime import datetime as dt
from typing import Tuple, Optional, List
from dataclasses import dataclass

import matplotlib.pylab as plt
import matplotlib.patches as patches

from src.constants import Person, Family, Dimensions, PageInfo, BoxPlotInfo, TextInfo, LinePlotInfo
import src.plotting.utility as pu

DETAILS_FS = 6
GAP_REDUCTION = 0.7
INDENTATION = 0.05
DPI = 72  # Dots per inch


def get_diagram_plot_position(page_info: PageInfo, family_parents: Optional[Family], families_person: List[Family]
                              ) -> Tuple[List[BoxPlotInfo], List[LinePlotInfo], PageInfo]:
    """ Calculates family position with main person located at the position provided.
    Page origin is at top left of page. However, as we do not know page size, start it at (0,0) to begin with.
    """

    boxes_to_plot, lines_to_plot = [], []
    page_info = calculate_box_page_and_column(page_info)
    main_person, main_person_position, is_father = None, None, None
    ii = 0
    for ii, family in enumerate(families_person):
        if main_person is None:
            if family.father_plotted_top:
                main_person = family.parent1
                is_father = True
            else:
                main_person = family.parent2
                is_father = False
        else:
            family.spouse_already_plotted_position = main_person_position
            if is_father:
                family.father_already_plotted = True
            else:
                family.mother_already_plotted = True

        boxes_to_plot_, lines_to_plot_, page_info = get_family_plot_position(family, page_info, parent_column_index=1,
                                                                             family_number=ii)
        if main_person_position is None:
            main_person_position = boxes_to_plot_[0]

        boxes_to_plot += boxes_to_plot_
        lines_to_plot += lines_to_plot_

    if family_parents:
        boxes_to_plot_, lines_to_plot_, page_info = get_family_plot_position(
            family_parents, page_info, parent_column_index=0, family_number=ii)
        boxes_to_plot += boxes_to_plot_
        lines_to_plot += lines_to_plot_

    boxes_to_plot, lines_to_plot, page_info = move_origin_from_bottom_to_top_of_page(boxes_to_plot, lines_to_plot,
                                                                                     page_info)

    return boxes_to_plot, lines_to_plot, page_info


def move_origin_from_bottom_to_top_of_page(boxes_to_plot: List[BoxPlotInfo], lines_to_plot: List[LinePlotInfo],
                                           page_info: PageInfo) -> Tuple[BoxPlotInfo, LinePlotInfo, PageInfo]:
    max_y = max(page_info.column_top_position) - page_info.gap[1] + page_info.margin[1]
    page_info.page_height = max_y

    boxes_to_plot_ = []
    for bp in boxes_to_plot:
        bp_ = dc(bp)
        bp_.y = max_y - bp.y
        boxes_to_plot_.append(bp_)

    lines_to_plot_ = []
    for lp in lines_to_plot:
        lp_ = dc(lp)
        s, e = lp.start, lp.end
        s, e = (s[0], max_y - s[1]), (e[0], max_y - e[1])
        lp_.start, lp_.end = s, e
        lines_to_plot_.append(lp_)

    return boxes_to_plot_, lines_to_plot_, page_info


def calculate_box_page_and_column(page_info: PageInfo) -> PageInfo:
    # We need to keep track up to where we are filled up the columns
    num_cols = 3
    page_info.column_top_position = [page_info.margin[1]] * num_cols

    # Next calculate the  stride
    # horizontal stride
    box_width = (page_info.page_width - 2 * page_info.margin[0] - (num_cols - 1) * page_info.gap[0]) / num_cols
    x_stride = box_width + page_info.gap[0]

    if page_info.minimize_y_or_x == 'x':
        box_height = 2 * (page_info.font_size_large / DPI) + 4 * (page_info.font_size_small / DPI) + 0.1
        y_stride = box_height + page_info.gap[1]
        page_info.box_size = (box_width, box_height)
        page_info.stride = (x_stride, y_stride)
    else:
        # vertical stride based on fontsize
        # Expect 1 large line and two small lines
        box_height = page_info.font_size_large / DPI + 2 * (page_info.font_size_small / DPI) + 0.1
        y_stride = box_height + page_info.gap[1]
        page_info.box_size = (box_width, box_height)
        page_info.stride = (x_stride, y_stride)

    # This assumes 3 columns for now
    middle = page_info.page_width / 2.
    page_info.column_x = [middle - x_stride, middle, middle + x_stride]

    return page_info


def get_family_plot_position(family: Family, page_info: PageInfo, parent_column_index: int, family_number: int
                             ) -> Tuple[List, List, PageInfo]:
    boxes_to_plot, lines_to_plot, page_info, plot_info_mbox = plot_parents(family, page_info, parent_column_index,
                                                                           family_number)
    boxes_to_plot_, lines_to_plot_, page_info = plot_children(family, page_info, parent_column_index + 1,
                                                              plot_info_mbox, family_number)
    boxes_to_plot += boxes_to_plot_
    lines_to_plot += lines_to_plot_

    return boxes_to_plot, lines_to_plot, page_info


def plot_parents(family: Family, page_info: PageInfo, parent_column_index: int, family_number: int
                 ) -> Tuple[List, List, PageInfo, BoxPlotInfo]:
    boxes_to_plot, lines_to_plot, plot_info_mbox = [], [], None

    # Which parent goes on top?
    spouse1, spouse2 = who_gets_plotted_on_top(family)

    if spouse2 is None and (spouse1 or not family.one_child_already_plotted):
        # If spouse 2 is None, s/he has already been plotted.
        if (family.parent1 and family.parent2) or family.children:
            plot_info_mbox, page_info = add_marriage_box(family, parent_column_index, page_info)
            page_info.column_top_position[parent_column_index] += page_info.minimum_gap_y
            boxes_to_plot += [plot_info_mbox]

        plot_info_spouse1, page_info = add_person_box(spouse1, parent_column_index, page_info)
        page_info.column_top_position[parent_column_index] += page_info.gap[1]
        boxes_to_plot += [plot_info_spouse1]

        if (family.parent1 and family.parent2) or family.children:
            indentation = page_info.indentation * family_number
            # TODO: something gets assigned wrong, this should be of a single type
            if isinstance(family.spouse_already_plotted_position, tuple):
                x, y = family.spouse_already_plotted_position
            else:
                x, y = family.spouse_already_plotted_position.x, family.spouse_already_plotted_position.y
            start = (x + indentation, y)
            end = (plot_info_spouse1.x + indentation, plot_info_spouse1.y)
            lines_to_plot.append(LinePlotInfo(start, end))

    else:
        plot_info_spouse1, page_info = add_person_box(spouse1, parent_column_index, page_info)
        page_info.column_top_position[parent_column_index] += page_info.minimum_gap_y
        plot_info_mbox, page_info = add_marriage_box(family, parent_column_index, page_info)
        page_info.column_top_position[parent_column_index] += page_info.minimum_gap_y
        plot_info_spouse2, page_info = add_person_box(spouse2, parent_column_index, page_info)
        page_info.column_top_position[parent_column_index] += page_info.gap[1]
        boxes_to_plot += [plot_info_spouse1, plot_info_mbox, plot_info_spouse2]

        start = (plot_info_spouse1.x, plot_info_spouse1.y)
        end = (plot_info_spouse2.x, plot_info_spouse2.y)
        lines_to_plot.append(LinePlotInfo(start, end))

    return boxes_to_plot, lines_to_plot, page_info, plot_info_mbox


def plot_children(family: Family, page_info: PageInfo, column_index: int, marriage_box_position: BoxPlotInfo,
                  family_number: int) -> Tuple[List, List, BoxPlotInfo]:
    boxes_to_plot, lines_to_plot = [], []
    if family.children:
        boxes_to_plot, lines_to_plot, page_info = plot_all_children(family, page_info, marriage_box_position,
                                                                    column_index, family_number)

    if family.one_child_already_plotted:
        vertical_line_x = page_info.column_x[column_index - 1] + page_info.stride[0] / 2. + page_info.indentation
        # add indentation
        if family_number > 0:
            vertical_line_x -= page_info.indentation

        x_, y_ = marriage_box_position.x, marriage_box_position.y

        if not family.children:
            # line from marriage box to vertical
            lines_to_plot.append(LinePlotInfo((x_, y_), (vertical_line_x, y_)))

        # vertical line up to main person
        top_y = page_info.margin[1] + page_info.box_size[1] / 2.
        lines_to_plot.append(LinePlotInfo((vertical_line_x, y_), (vertical_line_x, top_y)))

        # Line from vertical to main person
        x = page_info.column_x[column_index]
        lines_to_plot.append(LinePlotInfo((vertical_line_x, top_y), (x, top_y)))

    return boxes_to_plot, lines_to_plot, page_info


def plot_all_children(family: Family, page_info: PageInfo, marriage_box_position,
                      column_index: int, family_number: int):
    """ Add lines and boxes to plot for the children of a family.

    Lines:
    - Add one horizontal line from the marriage box to the vertical line
    - For each child, add a horizontal line from the vertical line to its box
    - Add a vertical line
    """

    boxes_to_plot, lines_to_plot = [], []
    vertical_line_x = page_info.column_x[column_index - 1] + page_info.stride[0] / 2. + page_info.indentation

    # add indentation
    if family_number > 0:
        vertical_line_x -= page_info.indentation

    # line from marriage box to vertical
    x_, y_ = marriage_box_position.x, marriage_box_position.y
    lines_to_plot.append(LinePlotInfo((x_, y_), (vertical_line_x, y_)))

    min_y, max_y = marriage_box_position.y, marriage_box_position.y
    for child in family.children:
        plot_info_child, page_info = add_person_box(child, column_index, page_info)
        page_info.column_top_position[column_index] += page_info.gap[1]
        boxes_to_plot += [plot_info_child]

        start = (vertical_line_x, plot_info_child.y)
        end = (plot_info_child.x, plot_info_child.y)
        lines_to_plot.append(LinePlotInfo(start, end))

        if min_y > plot_info_child.y:
            min_y = plot_info_child.y
        if max_y < plot_info_child.y:
            max_y = plot_info_child.y

    # vertical line
    start = (vertical_line_x, max_y)
    end = (vertical_line_x, min_y)
    lines_to_plot.append(LinePlotInfo(start, end))

    return boxes_to_plot, lines_to_plot, page_info


def add_person_box(person: Person, column_index: int, page_info: PageInfo) -> Tuple[BoxPlotInfo, PageInfo]:
    lines = []
    box_height = page_info.box_size[1]

    if person:
        if page_info.minimize_y_or_x == 'x':
            box_height, lines = _get_lines_for_person_box_minimizing_x(box_height, person, page_info)

        else:
            fn, ln = _get_names(person)
            text = '{} {}'.format(fn, ln)
            line1 = TextInfo(text, page_info.font_size_large, bold=True)

            bds, bdd, bp = _get_birth_details(person)
            text = pu.get_string_for_event(bds, bdd, bp, 'b.')
            line2 = TextInfo(text, page_info.font_size_small)

            dds, ddd, dp = _get_death_details(person)
            text = pu.get_string_for_event(dds, ddd, dp, 'd.')
            line3 = TextInfo(text, page_info.font_size_small)
            lines = [line1, line2, line3]

    x = page_info.column_x[column_index]
    y = page_info.column_top_position[column_index] + box_height / 2.
    page_info.column_top_position[column_index] += box_height

    plot_info = BoxPlotInfo(x, y, page_info.box_size[0], box_height, lines=lines)

    return plot_info, page_info


def _get_lines_for_person_box_minimizing_x(box_height, person: Person, page_info: PageInfo):
    fn, ln = _get_names(person)
    line1, line2 = write_on_one_or_two_lines(page_info.box_size[0], fn, ln, True, page_info.font_size_large)

    bds, bdd, bp = _get_birth_details(person)
    text1, text2 = pu.get_two_line_string_for_event(bds, bdd, bp, 'b.')
    line3, line4 = write_on_one_or_two_lines(page_info.box_size[0], text1, text2, False, page_info.font_size_small)

    dds, ddd, dp = _get_death_details(person)
    text1, text2 = pu.get_two_line_string_for_event(dds, ddd, dp, 'd.')
    line5, line6 = write_on_one_or_two_lines(page_info.box_size[0], text1, text2, False, page_info.font_size_small)

    lines = [line1, line2, line3, line4, line5, line6]

    leng = len([x for x in lines if x.text])
    if leng < 6:
        box_height = box_height * ((leng / 6) + 0.1)

    return box_height, lines


def write_on_one_or_two_lines(x_box_size: float, text1: str, text2: str, bold: bool, fontsize: int) -> (
        TextInfo, TextInfo):
    if not text2:
        return TextInfo(text1, fontsize, bold=bold), TextInfo(text2, fontsize, bold=bold)

    leng = _get_estimated_length_of_text_in_inches(text1 + ' ' + text2, fontsize)
    if leng <= x_box_size:
        # Can fit on one line
        line1 = TextInfo(text1 + ' ' + text2, fontsize, bold=bold)
        line2 = TextInfo('', fontsize, bold=bold)
    else:
        line1 = TextInfo(text1, fontsize, bold=bold)
        line2 = TextInfo(text2, fontsize, bold=bold)
    return line1, line2


def _get_names(person: Person) -> (str, str):
    fn, ln = '', ''
    if person.first_name:
        fn = person.first_name
    if person.last_name:
        ln = person.last_name
    return fn, ln


def _get_estimated_length_of_text_in_inches(text: str, font_size: int) -> float:
    """
    13 Letters at font size 9 takes 0.966 inches
    14 Letters at font size 8 tales 0.9 inches
    """
    font_size_to_letter_width = {
        9: 0.0743,  # inches
        8: 0.0642
    }
    if font_size in font_size_to_letter_width:
        width_per_letter = font_size_to_letter_width[font_size]
    else:
        width_per_letter = font_size_to_letter_width[9]

    leng = len(text)
    return leng * width_per_letter


def _get_birth_details(person: Person) -> Tuple:
    return person.birth_date_str, person.birth_date, person.birth_place


def _get_death_details(person: Person) -> Tuple:
    return person.death_date_str, person.death_date, person.death_place


def _get_marriage_details(family: Family) -> Tuple:
    return family.marriage_date_str, family.marriage_date, family.marriage_place


def add_marriage_box(family: Family, column_index: int, page_info: PageInfo) -> Tuple[BoxPlotInfo, PageInfo]:
    if page_info.minimize_y_or_x == 'x':
        mds, mdd, mp = _get_marriage_details(family)
        text1, text2 = pu.get_two_line_string_for_event(mds, mdd, mp, 'm.')
        box_size, fontsize = page_info.box_size[0], page_info.font_size_small
        line1, line2 = write_on_one_or_two_lines(box_size, text1, text2, False, fontsize)
        lines = [line1, line2]
    else:
        mds, mdd, mp = _get_marriage_details(family)
        text = pu.get_string_for_event(mds, mdd, mp, 'm.')
        lines = [TextInfo(text, page_info.font_size_small)]

    # fix size of marriage box here for now
    if page_info.minimize_y_or_x == 'x':
        # Only make box as high as it needs to be
        leng = len([x for x in lines if x.text])
        if leng == 0:
            box_height = (page_info.font_size_small / DPI) * 0.2 + 0.1
        elif leng == 1:
            box_height = (page_info.font_size_small / DPI) + 0.1
        else:
            box_height = (page_info.font_size_small / DPI) * 2 + 0.1
    else:
        box_height = page_info.font_size_small / DPI + 0.1

    x = page_info.column_x[column_index] + page_info.indentation
    y = page_info.column_top_position[column_index] + box_height / 2.
    page_info.column_top_position[column_index] += box_height

    plot_info = BoxPlotInfo(x, y, page_info.box_size[0], box_height, lines)

    return plot_info, page_info


def who_gets_plotted_on_top(family: Family) -> Tuple[Person, Person]:
    """ Which parent goes on top? """
    if family.father_already_plotted:  # mother
        spouse1, spouse2 = family.parent2, None
    elif family.mother_already_plotted:
        spouse1, spouse2 = family.parent1, None
    else:
        if family.father_plotted_top:
            spouse1, spouse2 = family.parent1, family.parent2
        else:
            spouse2, spouse1 = family.parent1, family.parent2
    return spouse1, spouse2
