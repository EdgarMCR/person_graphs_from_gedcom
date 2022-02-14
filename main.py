import time
from pathlib import Path
from datetime import datetime as dt
from typing import List, Optional, Tuple

import matplotlib.pyplot as plt

from gedcom.element.individual import IndividualElement
from gedcom.element.family import FamilyElement
from gedcom.parser import Parser

from src.constants import Family, Person
import src.parse_gedcom as pg


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


def main():
    path = Path('FamilyTree_Dec2021.ged')
    root = pg.load_file(path)
    fn, ln = 'Magdalena', 'Sadowska'
    person = pg.get_person(fname=fn, lname=ln, root_child_elements=root)
    # try_out_parser(path)
    # create_mini_graph(fn, ln, path)


if __name__ == "__main__":
    ss = dt.now().strftime('%H:%M:%S'); start_time = time.time()
    main()
    es = dt.now().strftime('%H:%M:%S'); l = ''.join(['-']*37); elapsed = time.time() - start_time
    print("\n%s\n-------- %s - %s --------\n--------- % 9.3f seconds ---------\n%s" % (l, ss, es, elapsed, l))
    