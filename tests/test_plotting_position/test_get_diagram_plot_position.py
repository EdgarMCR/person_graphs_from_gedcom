from unittest import TestCase

from datetime import datetime as dt

from src.constants import Person, Family, Dimensions, PageInfo
import src.plotting.plotting_position as pp
import src.plotting.utility as pu


class Test(TestCase):
    def test_1(self):

        main = Person('Firstname', 'Lastname', dt(1970, 1, 1), 'Hamburg, DE', dt(1970, 1, 1), 'Fultonham, NY, USA')

        page_info = PageInfo(page_width=10, page_height=None, margin=(0.05, 0.05), gap=(0.5, 0.2), minimum_gap_y=0.05)

        family_parents =  None  # Family(father=None, mother=None, children=[])
        family = Family(father=None, mother=main, children=[], father_plotted_top=False)
        boxes_to_plot, lines_to_plot, page_info = pp.get_diagram_plot_position(page_info, family_parents,
                                                                               families_person=[family])

        self.assertEqual(1, len(boxes_to_plot))
        self.assertTrue(main.first_name in boxes_to_plot[0].lines[0].text)
        self.assertEqual(5, boxes_to_plot[0].x)
        self.assertEqual(0, len(lines_to_plot))

    def test_2(self):
        page_info = PageInfo(page_width=10, page_height=None, margin=(0.05, 0.05), gap=(0.5, 0.2), minimum_gap_y=0.05)
        main = Person('Firstname', 'Lastname', dt(1970, 1, 1), 'Hamburg, DE', dt(1970, 1, 1), 'Fultonham, NY, USA')
        spouse = Person('Spouse', 'Lastname', dt(1970, 1, 1), 'Hamburg, DE', dt(1970, 1, 1), 'Fultonham, NY, USA')

        family_parents = Family(None, None, [])
        family_parents.one_child_already_plotted = True
        family = Family(spouse, main, [], dt(1980, 1, 1), 'Someplace, PL',one_child_already_plotted=False)
        boxes_to_plot, lines_to_plot, page_info = pp.get_diagram_plot_position(page_info, family_parents,
                                                                               families_person=[family])

        self.assertEqual(6, len(boxes_to_plot))
        self.assertTrue(main.first_name in boxes_to_plot[0].lines[0].text)
        self.assertEqual(5, boxes_to_plot[0].x)
        self.assertAlmostEqual(1.2,  boxes_to_plot[0].y, places=2, msg='y position of main person')
        self.assertAlmostEqual(0.84,  boxes_to_plot[1].y, places=2, msg='y position of main person marriage box')
        self.assertAlmostEqual(0.48,  boxes_to_plot[2].y, places=2, msg='y position of main person spouse')

        self.assertEqual(5, len(lines_to_plot))

    def test_3(self):
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

        self.assertEqual(6, len(boxes_to_plot))
        self.assertTrue(main.first_name in boxes_to_plot[0].lines[0].text)
        self.assertEqual(5, boxes_to_plot[0].x)
        self.assertAlmostEqual(1.2,  boxes_to_plot[0].y, places=2, msg='y position of main person')
        self.assertAlmostEqual(0.84,  boxes_to_plot[1].y, places=2, msg='y position of main person marriage box')
        self.assertAlmostEqual(0.48,  boxes_to_plot[2].y, places=2, msg='y position of main person spouse')

        self.assertEqual(5, len(lines_to_plot))

    def test_5(self):
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

        self.assertEqual(14, len(boxes_to_plot))
        self.assertTrue(main.first_name in boxes_to_plot[0].lines[0].text)
        self.assertEqual(5, boxes_to_plot[0].x)
        self.assertAlmostEqual(4.366,  boxes_to_plot[0].y, places=2, msg='y position of main person')
        self.assertAlmostEqual(4.008,  boxes_to_plot[1].y, places=2, msg='y position of main person marriage box')
        self.assertAlmostEqual(3.65,  boxes_to_plot[2].y, places=2, msg='y position of main person spouse')

        self.assertEqual(16, len(lines_to_plot))

    def test_6(self):
        page_info = PageInfo(page_width=10, page_height=None, margin=(0.05, 0.05), gap=(0.5, 0.2), minimum_gap_y=0.05)
        main = Person('Firstname', 'Lastname', dt(1970, 1, 1), 'Hamburg, DE', dt(1970, 1, 1), 'Fultonham, NY, USA')
        spouse = Person('Spouse', 'Lastname', dt(1970, 1, 1), 'Hamburg, DE', dt(1970, 1, 1), 'Fultonham, NY, USA')

        mother = Person('Parent1', 'Lastname', dt(1950, 1, 1), 'Hamburg, DE', dt(1950, 1, 1), 'Fultonham, NY, USA')
        father = Person('Parent2', 'Lastname', dt(1950, 1, 1), 'Hamburg, DE', dt(1950, 1, 1), 'Fultonham, NY, USA')

        p = Person('Child1', 'Lastname', dt(1950, 1, 1), 'Hamburg, DE', dt(1950, 1, 1), 'Fultonham, NY, USA')
        p2 = Person('Child2', 'Lastname', dt(1951, 1, 1), 'Hamburg, DE', dt(1950, 1, 1), 'Fultonham, NY, USA')
        p3 = Person('Child3', 'Lastname', dt(1952, 1, 1), 'Hamburg, DE', dt(1950, 1, 1), 'Fultonham, NY, USA')

        spouse2 = Person('Spouse2', 'Lastname', dt(1970, 1, 1), 'Hamburg, DE', dt(1970, 1, 1), 'Fultonham, NY, USA')

        p4 = Person('Child4', 'Lastname', dt(1950, 1, 1), 'Hamburg, DE', dt(1950, 1, 1), 'Fultonham, NY, USA')
        p5 = Person('Child5', 'Lastname', dt(1951, 1, 1), 'Hamburg, DE', dt(1950, 1, 1), 'Fultonham, NY, USA')

        person = Person('Sibling1', 'Lastname', dt(1950, 1, 1), 'Hamburg, DE', dt(1950, 1, 1), 'Fultonham, NY, USA')
        person2 = Person('Sibling2', 'Lastname', dt(1951, 1, 1), 'Hamburg, DE', dt(1950, 1, 1), 'Fultonham, NY, USA')
        person3 = Person('Siblings3', 'Lastname', dt(1952, 1, 1), 'Hamburg, DE', dt(1950, 1, 1), 'Fultonham, NY, USA')
        person4 = Person('Siblings4', 'Lastname', dt(1953, 1, 1), 'Hamburg, DE', dt(1950, 1, 1), 'Fultonham, NY, USA')
        person5 = Person('Siblings5', 'Lastname', dt(1954, 1, 1), 'Hamburg, DE', dt(1950, 1, 1), 'Fultonham, NY, USA')

        family_parents = Family(father, mother, [person, person2, person3, person4, person5], dt(1980, 1, 1),
                                'Someplace, PL', one_child_already_plotted=True)
        family = Family(spouse, main, [p, p2, p3], dt(1980, 1, 1), 'Someplace, PL',
                        one_child_already_plotted=False)
        family2 = Family(spouse2, main, [p4, p5], dt(1990, 1, 1), 'Someplace, PL',
                        one_child_already_plotted=False)
        boxes_to_plot, lines_to_plot, page_info = pp.get_diagram_plot_position(page_info, family_parents,
                                                                               families_person=[family, family2])

        self.assertEqual(18, len(boxes_to_plot))
        self.assertTrue(main.first_name in boxes_to_plot[0].lines[0].text)
        self.assertEqual(5, boxes_to_plot[0].x)
        self.assertAlmostEqual(5.233,  boxes_to_plot[0].y, places=2, msg='y position of main person')

        self.assertEqual(21, len(lines_to_plot))
