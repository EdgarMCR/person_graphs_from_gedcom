from unittest import TestCase

from datetime import datetime as dt

from src.constants import Person, Family, Dimensions, PageInfo, BoxPlotInfo, TextInfo
import src.plotting.plotting_position as pp
import src.plotting.utility as pu


class Test(TestCase):
    def test_1(self):
        """ No Children"""
        main = Person('Firstname', 'Lastname', birth_date=dt(1970, 1, 1), birth_place='Hamburg, DE',
                      death_date=dt(1970, 1, 1), death_place='Fultonham, NY, USA')

        page_info = PageInfo(page_width=10, page_height=None, margin=(0.05, 0.05), gap=(0.5, 0.2), minimum_gap_y=0.05)
        page_info = pp.calculate_box_page_and_column(page_info)

        column_index, family_number = 2, 0
        marriage_box_position = BoxPlotInfo(x=5, y=2, w=2, h=2, lines=['marriage box'])
        family = Family(parent1=None, parent2=main, children=[], father_plotted_top=False)
        boxes_to_plot, lines_to_plot, page_info = pp.plot_children(
            family, page_info, column_index, marriage_box_position, family_number)

        self.assertEqual(0, len(boxes_to_plot))
        self.assertEqual(0, len(lines_to_plot))

    def test_2(self):
        """ 1 Children"""
        main = Person('Firstname', 'Lastname', birth_date=dt(1970, 1, 1), birth_place='Hamburg, DE',
                      death_date=dt(1970, 1, 1), death_place='Fultonham, NY, USA')

        child = Person('Child', 'Lastname', birth_date=dt(1980, 1, 1), birth_place='Hamburg, DE',
                       death_date=dt(1970, 1, 1), death_place='Fultonham, NY, USA')

        page_info = PageInfo(page_width=10, page_height=None, margin=(0.05, 0.05), gap=(0.5, 0.2), minimum_gap_y=0.05)
        page_info = pp.calculate_box_page_and_column(page_info)

        column_index, family_number = 2, 0
        marriage_box_position = BoxPlotInfo(x=5, y=2, w=2, h=2, lines=['marriage box'])
        family = Family(parent1=None, parent2=main, children=[child], father_plotted_top=False)
        boxes_to_plot, lines_to_plot, page_info = pp.plot_children(
            family, page_info, column_index, marriage_box_position, family_number)

        self.assertEqual(1, len(boxes_to_plot))

        self.assertEqual(3, len(lines_to_plot))

        # Line from marriage box to vertical line
        line = lines_to_plot[0]
        start = (5, 2)
        end = (6.833333333333333, 2)
        self.assertEqual(start, line.start, 'line 0 start')
        self.assertEqual(end, line.end, 'line 0 end')

        # Line from vertical line to child box
        line = lines_to_plot[1]
        start = (6.833333333333333, 0.28055555555555556)
        end = (8.466666666666667, 0.28055555555555556)
        self.assertEqual(start, line.start)
        self.assertEqual(end, line.end)

        # Vertical line
        line = lines_to_plot[2]
        # If the order of start and end changes, need to sort lines and line start and end before returning
        end = (6.833333333333333, 0.28055555555555556)
        start = (6.833333333333333, 2)
        self.assertEqual(start, line.start, 'Vertical Line Start')
        self.assertEqual(end, line.end, 'Vertical Line End')


    def test_3(self):
        """ 1 Chil, already plotted"""
        main = Person('Firstname', 'Lastname', birth_date=dt(1970, 1, 1), birth_place='Hamburg, DE',
                      death_date=dt(1970, 1, 1), death_place='Fultonham, NY, USA')

        child = Person('Child', 'Lastname', birth_date=dt(1980, 1, 1), birth_place='Hamburg, DE',
                       death_date=dt(1970, 1, 1), death_place='Fultonham, NY, USA')

        page_info = PageInfo(page_width=10, page_height=5, margin=(0.05, 0.05), gap=(0.5, 0.2), minimum_gap_y=0.05)
        page_info = pp.calculate_box_page_and_column(page_info)

        column_index, family_number = 2, 0
        marriage_box_position = BoxPlotInfo(x=5, y=2, w=2, h=2, lines=[TextInfo('Marriage Box', 12)])
        family = Family(parent1=None, parent2=main, children=[child], father_plotted_top=False,
                        one_child_already_plotted=True)
        boxes_to_plot, lines_to_plot, page_info = pp.plot_children(
            family, page_info, column_index, marriage_box_position, family_number)

        # import matplotlib.pylab as plt
        # import src.plotting.plot_with_matplotlib as pwm
        #
        # boxes_to_plot, lines_to_plot, page_info = pp.move_origin_from_bottom_to_top_of_page(boxes_to_plot, lines_to_plot,
        #                                                                                  page_info)
        # pwm.plot_on_figure(page_info, boxes_to_plot, lines_to_plot)
        # plt.show()

        self.assertEqual(1, len(boxes_to_plot))
        # self.assertEqual(3, len(lines_to_plot))  #What is going on here?
