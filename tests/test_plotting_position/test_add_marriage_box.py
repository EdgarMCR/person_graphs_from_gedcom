from unittest import TestCase

from datetime import datetime as dt

from src.constants import Person, Family, Dimensions, PageInfo, BoxPlotInfo, TextInfo
import src.plotting.plotting_position as pp
import src.plotting.utility as pu


class Test(TestCase):
    def test_1(self):
        """ No text"""
        main = Person('Firstname', 'Lastname', birth_date=dt(1970, 1, 1), birth_place='Hamburg, DE',
                      death_date=dt(1970, 1, 1), death_place='Fultonham, NY, USA')
        spouse = Person('Spouse', 'Lastname', birth_date=dt(1970, 1, 1), birth_place='DE',
                      death_date=dt(1980, 1, 1), death_place='NY, USA')

        family = Family(main, spouse, [])
        page_info = PageInfo(page_width=10, page_height=None, margin=(0.05, 0.05), gap=(0.5, 0.2), minimum_gap_y=0.05,
                             minimize_y_or_x='x')
        page_info = pp.calculate_box_page_and_column(page_info)

        plot_info, _ = pp.add_marriage_box(family, 1, page_info)

        self.assertEqual(5.1, plot_info.x)
        self.assertAlmostEqual(0.11, plot_info.y, delta=0.01)
        self.assertAlmostEqual(2.96, plot_info.w, delta=0.01)
        self.assertAlmostEqual(0.12, plot_info.h, delta=0.01)

        page_info = PageInfo(page_width=10, page_height=None, margin=(0.05, 0.05), gap=(0.5, 0.2), minimum_gap_y=0.05,
                             minimize_y_or_x='y')
        page_info = pp.calculate_box_page_and_column(page_info)

        plot_info, page_info = pp.add_marriage_box(family, 1, page_info)

        self.assertEqual(5.1, plot_info.x)
        self.assertAlmostEqual(0.156, plot_info.y, delta=0.01)
        self.assertAlmostEqual(2.96, plot_info.w, delta=0.01)
        self.assertAlmostEqual(0.21, plot_info.h, delta=0.01)

    def test_2(self):
        """ short text only"""
        main = Person('Firstname', 'Lastname', birth_date=dt(1970, 1, 1), birth_place='Hamburg, DE',
                      death_date=dt(1970, 1, 1), death_place='Fultonham, NY, USA')
        spouse = Person('Spouse', 'Lastname', birth_date=dt(1970, 1, 1), birth_place='DE',
                      death_date=dt(1980, 1, 1), death_place='NY, USA')

        family = Family(main, spouse, [], marriage_place='Short', marriage_date_year=1900)
        page_info = PageInfo(page_width=10, page_height=None, margin=(0.05, 0.05), gap=(0.5, 0.2), minimum_gap_y=0.05,
                             minimize_y_or_x='x')
        page_info = pp.calculate_box_page_and_column(page_info)

        plot_info, page_info = pp.add_marriage_box(family, 1, page_info)

        self.assertEqual(5.1, plot_info.x)
        self.assertAlmostEqual(0.156, plot_info.y, delta=0.01)
        self.assertAlmostEqual(2.96, plot_info.w, delta=0.01)
        self.assertAlmostEqual(0.21, plot_info.h, delta=0.01)

        page_info = PageInfo(page_width=10, page_height=None, margin=(0.05, 0.05), gap=(0.5, 0.2), minimum_gap_y=0.05,
                             minimize_y_or_x='y')
        page_info = pp.calculate_box_page_and_column(page_info)

        plot_info, page_info = pp.add_marriage_box(family, 1, page_info)

        self.assertEqual(5.1, plot_info.x)
        self.assertAlmostEqual(0.156, plot_info.y, delta=0.01)
        self.assertAlmostEqual(2.96, plot_info.w, delta=0.01)
        self.assertAlmostEqual(0.21, plot_info.h, delta=0.01)

    def test_3(self):
        """ Long text """
        main = Person('Firstname', 'Lastname', birth_date=dt(1970, 1, 1), birth_place='Hamburg, DE',
                      death_date=dt(1970, 1, 1), death_place='Fultonham, NY, USA')
        spouse = Person('Spouse', 'Lastname', birth_date=dt(1970, 1, 1), birth_place='DE',
                      death_date=dt(1980, 1, 1), death_place='NY, USA')

        family = Family(main, spouse, [], marriage_place='Long Place Name here', marriage_date_str='01/01/1900')
        page_info = PageInfo(page_width=5, page_height=None, margin=(0.05, 0.05), gap=(0.5, 0.2), minimum_gap_y=0.05,
                             minimize_y_or_x='x')
        page_info = pp.calculate_box_page_and_column(page_info)

        plot_info, page_info = pp.add_marriage_box(family, 1, page_info)

        self.assertEqual(2.6, plot_info.x)
        self.assertAlmostEqual(0.211, plot_info.y, delta=0.01)
        self.assertAlmostEqual(1.3, plot_info.w, delta=0.01)
        self.assertAlmostEqual(0.322, plot_info.h, delta=0.01)

        page_info = PageInfo(page_width=10, page_height=None, margin=(0.05, 0.05), gap=(0.5, 0.2), minimum_gap_y=0.05,
                             minimize_y_or_x='y')
        page_info = pp.calculate_box_page_and_column(page_info)

        plot_info, page_info = pp.add_marriage_box(family, 1, page_info)

        self.assertEqual(5.1, plot_info.x)
        self.assertAlmostEqual(0.156, plot_info.y, delta=0.01)
        self.assertAlmostEqual(2.96, plot_info.w, delta=0.01)
        self.assertAlmostEqual(0.21, plot_info.h, delta=0.01)

