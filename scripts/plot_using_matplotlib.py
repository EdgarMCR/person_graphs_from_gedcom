import os
import time
import logging
from copy import deepcopy as dc
from datetime import datetime as dt
from typing import Tuple, Optional
from dataclasses import dataclass

import matplotlib.pylab as plt
import matplotlib.patches as patches

from src.constants import Person, Family, Dimensions, PageInfo
import src.plotting.plotting as  pl
import src.plotting.plotting_position as pp
import src.plotting.plot_with_matplotlib as pwm


def tried_with_matplotlib():
    num_people = 5
    margin, hm = 0.05, 0.1
    w, h = 8.25, (8.25 / 4) * num_people + margin * 2
    box_w, box_h, gap_h = 2.2, 0.5, 0.4

    col1, col2, col3 = hm + box_w/2, w / 2, w - hm - box_w/2
    rows = [h - box_h / 2 - margin - (box_h + gap_h) * ii for ii in range(10)]

    fig = plt.figure(figsize=(w, h))

    main = Person('Firstname', 'Lastname', dt(1970, 1, 1), 'Hamburg, DE', dt(1970, 1, 1), 'Fultonham, NY, USA')
    dimensions = Dimensions((col2, rows[0]), box_w, box_h, (w, h))
    # plot_box(dimensions, main, fig)
    spouse = Person('Spouse', 'Lastname', dt(1970, 1, 1), 'Hamburg, DE', dt(1970, 1, 1), 'Fultonham, NY, USA')

    mother = Person('Parent1', 'Lastname', dt(1950, 1, 1), 'Hamburg, DE', dt(1950, 1, 1), 'Fultonham, NY, USA')
    dimensions = Dimensions((col1, rows[0]), box_w, box_h, (w, h))
    # plot_box(dimensions, mother, fig)

    father = Person('Parent2', 'Lastname', dt(1950, 1, 1), 'Hamburg, DE', dt(1950, 1, 1), 'Fultonham, NY, USA')
    dimensions = Dimensions((col1, rows[1]), box_w, box_h, (w, h))
    # plot_box(dimensions, father, fig)

    p = Person('Child1', 'Lastname', dt(1950, 1, 1), 'Hamburg, DE', dt(1950, 1, 1), 'Fultonham, NY, USA')
    p2 = Person('Child2', 'Lastname', dt(1951, 1, 1), 'Hamburg, DE', dt(1950, 1, 1), 'Fultonham, NY, USA')
    p3 = Person('Child3', 'Lastname', dt(1952, 1, 1), 'Hamburg, DE', dt(1950, 1, 1), 'Fultonham, NY, USA')

    person = Person('Sibling1', 'Lastname', dt(1950, 1, 1), 'Hamburg, DE', dt(1950, 1, 1), 'Fultonham, NY, USA')
    person2 = Person('Sibling2', 'Lastname', dt(1951, 1, 1), 'Hamburg, DE', dt(1950, 1, 1), 'Fultonham, NY, USA')
    person3 = Person('Siblings3', 'Lastname', dt(1952, 1, 1), 'Hamburg, DE', dt(1950, 1, 1), 'Fultonham, NY, USA')
    person4 = Person('Siblings4', 'Lastname', dt(1953, 1, 1), 'Hamburg, DE', dt(1950, 1, 1), 'Fultonham, NY, USA')
    person5 = Person('Siblings5', 'Lastname', dt(1954, 1, 1), 'Hamburg, DE', dt(1950, 1, 1), 'Fultonham, NY, USA')
    dimensions = Dimensions((col3, rows[0]), box_w, box_h, (w, h))
    # plot_box(dimensions, person, fig)

    family = Family(father, mother, [person, person2, person3, person4, person5], dt(1980, 1, 1), 'Someplace, PL',
                    one_child_already_plotted=True)
    stride = (col2-col1), rows[0] - rows[1]
    dimensions = Dimensions((col1, rows[0]), box_w, box_h, (w, h))
    pl.plot_family(stride, dimensions, family, h-margin, fig)

    family = Family(spouse, main, [p, p2, p3], dt(1980, 1, 1), 'Someplace, PL',
                    one_child_already_plotted=False)
    dimensions = Dimensions((col2, rows[0]), box_w, box_h, (w, h))
    pl.plot_family(stride, dimensions, family, h-margin, fig, indent_spouse=1)

    plt.show()

def try_2():
    main = Person('Firstname', 'Lastname', dt(1970, 1, 1), 'Hamburg, DE', dt(1970, 1, 1), 'Fultonham, NY, USA')

    page_info = PageInfo(page_width=10, page_height=None, margin=(0.05, 0.05), gap=(0.5, 0.2), minimum_gap_y=0.05)

    family_parents = Family(parent1=None, parent2=None, children=[])
    family = Family(parent1=None, parent2=main, children=[], father_plotted_top=False)
    boxes_to_plot, lines_to_plot, page_info = pp.get_diagram_plot_position(page_info, family_parents,
                                                                           families_person=[family])
    fig = pwm.plot_on_figure(page_info, boxes_to_plot, lines_to_plot)
    plt.show()


def try_3():
    page_info = PageInfo(page_width=10, page_height=None, margin=(0.05, 0.05), gap=(0.5, 0.2), minimum_gap_y=0.05)
    main = Person('Firstname', 'Lastname', dt(1970, 1, 1), 'Hamburg, DE', dt(1970, 1, 1), 'Fultonham, NY, USA')
    spouse = Person('Spouse', 'Lastname', dt(1970, 1, 1), 'Hamburg, DE', dt(1970, 1, 1), 'Fultonham, NY, USA')

    mother = Person('Parent1', 'Lastname', dt(1950, 1, 1), 'Hamburg, DE', dt(1950, 1, 1), 'Fultonham, NY, USA')
    father = Person('Parent2', 'Lastname', dt(1950, 1, 1), 'Hamburg, DE', dt(1950, 1, 1), 'Fultonham, NY, USA')

    family_parents = Family(father, mother, [], dt(1980, 1, 1), 'Someplace, PL',
                            one_child_already_plotted=True)
    family = Family(spouse, main, [], dt(1980, 1, 1), 'Someplace, PL',
                    one_child_already_plotted=False)
    boxes_to_plot, lines_to_plot, page_info = pp.get_diagram_plot_position(page_info, family_parents,
                                                                               families_person=[family])
    fig = pwm.plot_on_figure(page_info, boxes_to_plot, lines_to_plot)
    plt.show()

def try_4():
    page_info = PageInfo(page_width=10, page_height=None, margin=(0.05, 0.05), gap=(0.5, 0.2), minimum_gap_y=0.05)
    main = Person('Firstname', 'Lastname', dt(1970, 1, 1), 'Hamburg, DE', dt(1970, 1, 1), 'Fultonham, NY, USA')
    spouse = Person('Spouse', 'Lastname', dt(1970, 1, 1), 'Hamburg, DE', dt(1970, 1, 1), 'Fultonham, NY, USA')

    mother = Person('Parent1', 'Lastname', dt(1950, 1, 1), 'Hamburg, DE', dt(1950, 1, 1), 'Fultonham, NY, USA')
    father = Person('Parent2', 'Lastname', dt(1950, 1, 1), 'Hamburg, DE', dt(1950, 1, 1), 'Fultonham, NY, USA')

    p = Person('Child1', 'Lastname', dt(1950, 1, 1), 'Hamburg, DE', dt(1950, 1, 1), 'Fultonham, NY, USA')
    p2 = Person('Child2', 'Lastname', dt(1951, 1, 1), 'Hamburg, DE', dt(1950, 1, 1), 'Fultonham, NY, USA')
    p3 = Person('Child3', 'Lastname', dt(1952, 1, 1), 'Hamburg, DE', dt(1950, 1, 1), 'Fultonham, NY, USA')

    person = Person('Sibling1', 'Lastname', dt(1950, 1, 1), 'Hamburg, DE', dt(1950, 1, 1), 'Fultonham, NY, USA')
    person2 = Person('Sibling2', 'Lastname', dt(1951, 1, 1), 'Hamburg, DE', dt(1950, 1, 1), 'Fultonham, NY, USA')
    person3 = Person('Siblings3', 'Lastname', dt(1952, 1, 1), 'Hamburg, DE', dt(1950, 1, 1), 'Fultonham, NY, USA')
    person4 = Person('Siblings4', 'Lastname', dt(1953, 1, 1), 'Hamburg, DE', dt(1950, 1, 1), 'Fultonham, NY, USA')
    person5 = Person('Siblings5', 'Lastname', dt(1954, 1, 1), 'Hamburg, DE', dt(1950, 1, 1), 'Fultonham, NY, USA')

    family_parents = Family(father, mother, [person, person2, person3, person4, person5], dt(1980, 1, 1),
                            'Someplace, PL', one_child_already_plotted=True)
    family = Family(spouse, main, [p, p2, p3], dt(1980, 1, 1), 'Someplace, PL',
                    one_child_already_plotted=False)
    boxes_to_plot, lines_to_plot, page_info = pp.get_diagram_plot_position(page_info, family_parents,
                                                                           families_person=[family])
    fig = pwm.plot_on_figure(page_info, boxes_to_plot, lines_to_plot)
    plt.show()


def try_5():
    page_info = PageInfo(page_width=10, page_height=None, margin=(0.05, 0.05), gap=(0.5, 0.15), minimum_gap_y=0.05)
    main = Person('Firstname', 'Lastname', dt(1970, 1, 1), 1970, 'Hamburg, DE', dt(1970, 1, 1), 1970, 'Fultonham, NY, USA')
    spouse = Person('Spouse', 'Lastname', dt(1970, 1, 1), 1970, 'Hamburg, DE', dt(1970, 1, 1), 1970, 'Fultonham, NY, USA')

    mother = Person('Parent1', 'Lastname', dt(1950, 1, 1), 1970, 'Hamburg, DE', dt(1950, 1, 1), 1970, 'Fultonham, NY, USA')
    father = Person('Parent2', 'Lastname', dt(1950, 1, 1), 1970, 'Hamburg, DE', dt(1950, 1, 1), 1970, 'Fultonham, NY, USA')

    p = Person('Child1', 'Lastname', dt(1950, 1, 1),  1970,'Hamburg, DE', dt(1950, 1, 1), 1970, 'Fultonham, NY, USA')
    p2 = Person('Child2', 'Lastname', dt(1951, 1, 1), 1970, 'Hamburg, DE', dt(1950, 1, 1), 1970, 'Fultonham, NY, USA')
    p3 = Person('Child3', 'Lastname', dt(1952, 1, 1), 1970, 'Hamburg, DE', dt(1950, 1, 1), 1970, 'Fultonham, NY, USA')

    spouse2 = Person('Spouse2', 'Lastname', dt(1970, 1, 1), 1970, 'Hamburg, DE', dt(1970, 1, 1), 1970, 'Fultonham, NY, USA')

    p4 = Person('Child4', 'Lastname', dt(1950, 1, 1), 1970, 'Hamburg, DE', dt(1950, 1, 1), 1970, 'Fultonham, NY, USA')
    p5 = Person('Child5', 'Lastname', dt(1951, 1, 1), 1970, 'Hamburg, DE', dt(1950, 1, 1), 1970, 'Fultonham, NY, USA')

    person = Person('Sibling1', 'Lastname', dt(1950, 1, 1), 1970, 'Hamburg, DE', dt(1950, 1, 1), 1970, 'Fultonham, NY, USA')
    person2 = Person('Sibling2', 'Lastname', dt(1951, 1, 1), 1970, 'Hamburg, DE', dt(1950, 1, 1), 1970, 'Fultonham, NY, USA')
    person3 = Person('Siblings3', 'Lastname', dt(1952, 1, 1), 1970, 'Hamburg, DE', dt(1950, 1, 1), 1970, 'Fultonham, NY, USA')
    person4 = Person('Siblings4', 'Lastname', dt(1953, 1, 1), 1970, 'Hamburg, DE', dt(1950, 1, 1), 1970, 'Fultonham, NY, USA')
    person5 = Person('Siblings5', 'Lastname', dt(1954, 1, 1), 1970, 'Hamburg, DE', dt(1950, 1, 1), 1970, 'Fultonham, NY, USA')

    family_parents = Family(father, mother, [person, person2, person3, person4, person5], dt(1980, 1, 1),
                            'Someplace, PL', one_child_already_plotted=True)
    family = Family(spouse, main, [p, p2, p3], dt(1980, 1, 1), 'Someplace, PL',
                    one_child_already_plotted=False)
    family2 = Family(spouse2, main, [p4, p5], dt(1990, 1, 1), 'Someplace, PL',
                     one_child_already_plotted=False)
    boxes_to_plot, lines_to_plot, page_info = pp.get_diagram_plot_position(page_info, family_parents,
                                                                           families_person=[family, family2])
    fig = pwm.plot_on_figure(page_info, boxes_to_plot, lines_to_plot)
    plt.show()


def main():
    logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)s %(message)s', datefmt='%H:%M:%S',
                        level=logging.INFO)
    logging.getLogger().setLevel(logging.INFO)
    # tried_with_matplotlib()
    try_5()


if __name__ == "__main__":
    start_time = time.time()  # pylint: disable=C0103
    main()
    print("Ran %s in %.3f seconds" % (os.path.basename(__file__), time.time() - start_time))
