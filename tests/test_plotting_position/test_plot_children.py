from unittest import TestCase

from datetime import datetime as dt

from src.constants import Person, Family, Dimensions, PageInfo
import src.plotting.plotting_position as pp
import src.plotting.utility as pu


class Test(TestCase):
    def test_1(self):
        main = Person('Firstname', 'Lastname', birth_date=dt(1970, 1, 1), birth_place='Hamburg, DE',
                      death_date=dt(1970, 1, 1), death_place='Fultonham, NY, USA')

        page_info = PageInfo(page_width=10, page_height=None, margin=(0.05, 0.05), gap=(0.5, 0.2), minimum_gap_y=0.05)

        column_index, marriage_box_position, family_number = 2, None, 0
        family = Family(parent1=None, parent2=main, children=[], father_plotted_top=False)
        boxes_to_plot, lines_to_plot, page_info = pp.plot_children(
            family, page_info, column_index, marriage_box_position, family_number)

        # self.assertEqual(1, len(boxes_to_plot))
        # self.assertTrue(main.first_name in boxes_to_plot[0].lines[0].text)
        # self.assertEqual(5, boxes_to_plot[0].x)
        # self.assertEqual(0, len(lines_to_plot))
