import re
import math
import time
import logging
from pathlib import Path
from datetime import datetime as dt
from typing import List, Optional, Tuple
import unicodedata

import matplotlib.pyplot as plt

from gedcom.element.individual import IndividualElement
from gedcom.element.family import FamilyElement
from gedcom.parser import Parser

from src.constants import Family, Person, Dimensions, PageInfo, Sex
import src.parse_gedcom as pg
import src.summary_creator as sc
import src.plotting.plotting_position as pp
import src.plotting.plot_with_matplotlib as pwm
import src.plotting.utility as pu



# Initialize the parser
def try_out_parser(path: Path):
    gedcom_parser = Parser()

    # Parse your file
    gedcom_parser.parse_file(path)

    root_child_elements = gedcom_parser.get_root_child_elements()

    # Iterate through all root child elements
    for element in root_child_elements:

        # Is the "element" an actual "IndividualElement"? (Allows usage of extra functions such as "surname_match" and "get_name".)
        if isinstance(element, IndividualElement):

            # Get all individuals whose surname matches "Doe"
            if element.surname_match('Doe'):
                print('Doe!')
                
            # Unpack the name tuple
            (first, last) = element.get_name()

            # Print the first and last name of the found individual
            print(first + " " + last)


def load_file(path: Path):
    # Initialize the parser
    gedcom_parser = Parser()

    # Parse your file
    gedcom_parser.parse_file(path)

    root_child_elements = gedcom_parser.get_root_child_elements()
    return root_child_elements


def get_person(fname: str, lname: str, root_child_elements) -> List:
    result = []
    # Iterate through all root child elements
    for element in root_child_elements:

        # Is the "element" an actual "IndividualElement"? (Allows usage of extra functions such as "surname_match" and "get_name".)
        if isinstance(element, IndividualElement):
            # Unpack the name tuple
            (first, last) = element.get_name()
            if fname == first and lname == last:
                result.append(element)
    return result

PLACE = 'PLAC'
ADDRESS = 'ADDR'
DATE = 'DATE'  # The time of an event in a calendar format.
BIRTH = 'BIRT'  # The event of entering into life.
MARRIAGE = 'MARR'  # A legal, common-law or customary event of creating a family unit of a man and a woman as husband and wife.
DEATH = 'DEAT' # The event when mortal life terminates.
FAMILY_CHILD = 'FAMC'
FAMILY_SPOUSE = 'FAMS'


def get_family(person, rce, person_is_child: bool):
    fc = None
    if person_is_child:
        tag = FAMILY_CHILD
    else:
        tag = FAMILY_SPOUSE

    for ele in person.get_child_elements():
        if tag == ele.get_tag():
            fc = ele.get_value()

    parents, children = [], []
    if fc:
        for element in rce:
            if isinstance(element, IndividualElement):
                if element == person:
                    continue

                for ele in element.get_child_elements():
                    if FAMILY_CHILD == ele.get_tag() and fc == ele.get_value():
                        children.append(element)
                    elif FAMILY_SPOUSE == ele.get_tag() and fc == ele.get_value():
                        parents.append(element)
    return parents, children


def get_element_value(tag: str, element) -> Optional[str]:
    value = None
    for ele in element.get_child_elements():
        if tag == ele.get_tag():
            value = ele.get_value()
    return value


def get_description_of_event(element) -> str:
    output = ''
    if element:
        date = get_element_value(DATE, element)

        place = get_element_value(PLACE, element)
        if place and len(place) > 20:
            parts = place.split(',')
            if len(parts) > 2:
                place = ','.join(parts[-2:]).strip()

        if date:
            output = date

        if place:
            output += ' ' + place
    return output


def get_str_with_details(person: IndividualElement) -> Tuple[str]:
    fn, ln = person.get_name()
    name = '{} {}'.format(fn, ln)

    description = ''
    birth_event, death_event = None, None
    for ele in person.get_child_elements():
        if BIRTH == ele.get_tag():
            birth_event = ele
        elif DEATH == ele.get_tag():
            death_event = ele
    desc = get_description_of_event(birth_event)
    if desc:
        description += '\n' + desc

    desc = get_description_of_event(death_event)
    if desc:
        description += '\n' + desc

    return name, description
    
    
def create_mini_graph(fname: str, lname: str, path: Path):
    rce = load_file(path)
    person = get_person(fname, lname, rce)[0]

    parents, siblings = get_family(person, rce, person_is_child=True)
    spouse, children = get_family(person, rce, person_is_child=False)
    print([x.get_name() for x in parents])
    print([x.get_name() for x in spouse])
    print([x.get_name() for x in siblings])
    print([x.get_name() for x in children])

    name, description = get_str_with_details(person)
    print(description)

    fig, ax = plt.subplots()
    plt.axis([-10, 10, 0, 10])
    # these are matplotlib.patch.Patch properties
    props = dict(boxstyle='round', alpha=0.5)

    # place a text box in upper left in axes coords
    ax.text(0, 10, name, fontsize=14, ha='center', va='top', bbox=props)
    plt.show()

def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')


def plot_person_graph(person: Person, root, save_folder: Path):
    family_parents, families = pg.get_all_families_for_individual(person.gedcom_element, root)

    family_parents, families = pu.prepare_for_plotting(person, family_parents, families)
    page_info = PageInfo(page_width=9, page_height=None, margin=(0.05, 0.05), gap=(0.5, 0.15), minimum_gap_y=0.05,
                         font_size_large=10, font_size_small=9)
    boxes_to_plot, lines_to_plot, page_info = pp.get_diagram_plot_position(page_info, family_parents,
                                                                           families_person=families)
    fig = pwm.plot_on_figure(page_info, boxes_to_plot, lines_to_plot)
    fn, ln = person.first_name.split(' ')[0], person.last_name
    date = ''
    if person.birth_date:
        date = person.birth_date.strftime('%Y')
    if person.birth_date_year:
        date = person.birth_date_year
    save_name = '{}_{}_{}'.format(fn, ln, date)
    save_name = slugify(save_name, allow_unicode=False) + '.png'
    print("Saving as `{}`".format(save_name))
    plt.savefig(save_folder / save_name, dpi=150)
    plt.close(fig)


def plot_all_person_graphs(root, folder: Path):
    for element in root:
        if isinstance(element, IndividualElement):
            person = pg.convert_gedcom_to_person(element)
            if person.birth_date_year and person.birth_date_year < 1870:
                continue
            logging.info("Doing {} {}".format(person.first_name, person.last_name))
            plot_person_graph(person, root, folder)

            text = sc.get_summary_text(person, root) + '\n'
            print(text)
            with open(folder / 'summaries.txt', 'a', encoding='utf8') as f:
                f.write(text)


def main():
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
    path = Path('../Sofia.ged')
    root = pg.load_file(path)
    fn, ln = 'Magdalena', 'Sadowska'
    fn, ln = 'Irena', 'Solowij'
    # person = pg.get_person_by_name(fname=fn, lname=ln, root_child_elements=root)
    persons = pg.get_all_persons_by_name(fname=fn, lname=ln, root_child_elements=root)
    person = persons[0]
    folder = Path(r'E:\person_graphs')
    print(sc.get_summary_text(person, root))
    plot_person_graph(person, root, folder)


    # try_out_parser(path)
    # create_mini_graph(fn, ln, path)
    # plot_all_person_graphs(root, folder)


if __name__ == "__main__":
    ss = dt.now().strftime('%H:%M:%S'); start_time = time.time()
    main()
    es = dt.now().strftime('%H:%M:%S'); l = ''.join(['-']*37); elapsed = time.time() - start_time
    print("\n%s\n-------- %s - %s --------\n--------- % 9.3f seconds ---------\n%s" % (l, ss, es, elapsed, l))
    