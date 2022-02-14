import time
from pathlib import Path
from datetime import datetime as dt
from typing import List, Optional, Tuple

import matplotlib.pyplot as plt

from gedcom.element.individual import IndividualElement, Element
from gedcom.element.family import FamilyElement
from gedcom.parser import Parser

from src.constants import Family, Person

PLACE = 'PLAC'
ADDRESS = 'ADDR'
DATE = 'DATE'  # The time of an event in a calendar format.
BIRTH = 'BIRT'  # The event of entering into life.
MARRIAGE = 'MARR'  # A legal, common-law or customary event of creating a family unit of a man and a woman as husband and wife.
DEATH = 'DEAT' # The event when mortal life terminates.
FAMILY_CHILD = 'FAMC'
FAMILY_SPOUSE = 'FAMS'
SEX = 'SEX'


def load_file(path: Path):
    # Initialize the parser
    gedcom_parser = Parser()

    # Parse your file
    gedcom_parser.parse_file(path)

    root_child_elements = gedcom_parser.get_root_child_elements()
    return root_child_elements


def get_person_families(person: Person, root_child_elements) -> Tuple[Optional[Family], List[Family]]:
     parent_family, families = None, []

     return parent_family, families


def get_person(fname: str, lname: str, root_child_elements) -> Optional[Person]:
    person = None
    # Iterate through all root child elements
    for element in root_child_elements:

        # Is the "element" an actual "IndividualElement"?
        # (Allows usage of extra functions such as "surname_match" and "get_name".)
        if isinstance(element, IndividualElement):
            # Unpack the name tuple
            (first, last) = element.get_name()
            if fname == first and lname == last:
                person = convert_gedcom_to_person(element)
    return person


def convert_gedcom_to_person(element: IndividualElement) -> Person:
    person = Person()
    person.first_name, person.last_name = element.get_name()

    person.birth_place, person.birth_date = get_event_place_and_date(BIRTH, element)
    person.death_place, person.death_date = get_event_place_and_date(DEATH, element)

    person.sex = get_element_value(SEX, element)
    person.gedcom_element = element
    return person


def get_event_place_and_date(tag: str, element: IndividualElement) -> Tuple[Optional[str], Optional[dt]]:
    place, d = None, None
    event = get_event_element(tag, element)
    if event:
        place = get_element_value(PLACE, event)
        date = get_element_value(DATE, event)
        if date:
            d = dt.strptime(date, '%d %b %Y')
    return  place, d


def get_event_element(tag: str, element: IndividualElement) -> Optional[Element]:
    val = None
    for ele in element.get_child_elements():
        if tag == ele.get_tag():
            val = ele
            break
    return val


def get_element_value(tag: str, element) -> Optional[str]:
    value = None
    for ele in element.get_child_elements():
        if tag == ele.get_tag():
            value = ele.get_value()
            break
    return value


def get_element_values(tag: str, element) -> List[str]:
    values = []
    for ele in element.get_child_elements():
        if tag == ele.get_tag():
            values += [ele.get_value()]
    return values



def get_parent_family(person: IndividualElement, root, person_is_child: bool) -> Optional[Family]:
    tag = FAMILY_CHILD
    family = None
    for ele in person.get_child_elements():
        if tag == ele.get_tag():
            family = ele.get_value()


def get_people_in_family(person: IndividualElement, family: str, root) -> Tuple[List[Person], List[Person]]:
    parents, children = [], []
    if family:
        for element in root:
            if isinstance(element, IndividualElement):
                if element == person:
                    continue

                for ele in element.get_child_elements():
                    if FAMILY_CHILD == ele.get_tag() and family == ele.get_value():
                        children.append(convert_gedcom_to_person(element))
                    elif FAMILY_SPOUSE == ele.get_tag() and family == ele.get_value():
                        parents.append(convert_gedcom_to_person(element))

    return parents, children