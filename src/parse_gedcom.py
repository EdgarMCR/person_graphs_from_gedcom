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
DIVORCE = 'DIV '
DEATH = 'DEAT' # The event when mortal life terminates.
FAMILY_CHILD = 'FAMC'
FAMILY_SPOUSE = 'FAMS'
SEX = 'SEX'
HUSBAND = 'HUSB'
WIFE = 'WIFE'
CHILD = 'CHIL'


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


def get_person_by_name(fname: str, lname: str, root_child_elements) -> Optional[Person]:
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
                break
    return person


def get_person(pointer: str, root_child_elements) -> Optional[Person]:
    person = None
    # Iterate through all root child elements
    for element in root_child_elements:
        # Is the "element" an actual "IndividualElement"?
        # (Allows usage of extra functions such as "surname_match" and "get_name".)
        if isinstance(element, IndividualElement):
            if element.get_pointer() == pointer:
                person = convert_gedcom_to_person(element)
                break
    return person


def convert_gedcom_to_person(element: IndividualElement) -> Person:
    person = Person()
    person.first_name, person.last_name = element.get_name()

    person.birth_place, person.birth_date = get_event_place_and_date(BIRTH, element)
    person.death_place, person.death_date = get_event_place_and_date(DEATH, element)

    person.sex = get_element_value(SEX, element)

    person.gedcom_element = element
    return person


def get_family_element(id: str, root_child_elements) -> Optional[FamilyElement]:
    family = None
    # Iterate through all root child elements
    for element in root_child_elements:
        if isinstance(element, FamilyElement):
            if element.get_pointer() == id:
                family = element
                break
    return family


def get_event_place_and_date(tag: str, element: Element) -> Tuple[Optional[str], Optional[dt]]:
    place, d = None, None
    event = get_child_element(tag, element)
    if event:
        place = get_element_value(PLACE, event)
        date = get_element_value(DATE, event)
        if date:
            d = dt.strptime(date, '%d %b %Y')
    return place, d


def get_child_element(tag: str, element: Element) -> Optional[Element]:
    val = None
    for ele in element.get_child_elements():
        if tag == ele.get_tag():
            val = ele
            break
    return val


def get_child_element_values(tag: str, element: IndividualElement) -> List[Element]:
    val = []
    for ele in element.get_child_elements():
        if tag == ele.get_tag():
            val.append(ele.get_value())
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


def get_all_families_for_individual(person: IndividualElement, root) -> Tuple[Family, List[Family]]:
    parent_family = get_family_for_individual(person, root, True)
    if parent_family:
        parent_family = parent_family[0]
    families = get_family_for_individual(person, root, False)
    for ii in range(1, len(families)):
        families[ii].one_child_already_plotted = True
    return parent_family, families

def get_family_for_individual(person: IndividualElement, root, person_is_child: bool) -> List[Family]:
    families = []
    if person_is_child:
        tag = FAMILY_CHILD
    else:
        tag = FAMILY_SPOUSE

    family_eles = []
    for ele in person.get_child_elements():
        if tag == ele.get_tag():
            family_eles.append(ele.get_value())

    for fam in family_eles:
        fam_ele = get_family_element(fam, root)
        if not fam_ele:
            continue

        parents, children = get_people_in_family(fam_ele, root)

        # TODO: Plotting is still too tightly coupled - the second parent is at the centre of the plot
        p1, p2 = None, None
        if parents[0].gedcom_element.get_pointer() == person.get_pointer():
            p2 = parents[0]
            if len(parents) > 1:
                p1 = parents[1]
        else:
            p1 = parents[0]
            if len(parents) > 1:
                p2 = parents[1]
        marriage_place, marriage_date = get_event_place_and_date(MARRIAGE, fam_ele)
        divorce_place, divorce_date = get_event_place_and_date(DIVORCE, fam_ele)

        fam = Family(parent1=p1, parent2=p2, children=children, marriage_place=marriage_place,
                     marriage_date=marriage_date, divorce_place=divorce_place, divorce_date=divorce_date)
        families.append(fam)
    return families


def get_people_in_family(family_ele: FamilyElement, root) -> Tuple[List[Person], List[Person]]:
    parents, children = [], []

    husband_pt = get_child_element(HUSBAND, family_ele)
    if husband := get_person(husband_pt.get_value(), root):
        parents.append(husband)
    wife_pt = get_child_element(WIFE, family_ele)
    if wife := get_person(wife_pt.get_value(), root):
        parents.append(wife)

    children_pts = get_child_element_values(CHILD, family_ele)
    for ch_pt in children_pts:
        children.append(get_person(ch_pt, root))

    return parents, children
