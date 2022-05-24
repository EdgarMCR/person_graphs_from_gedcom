import re
import math
from datetime import datetime as dt
from typing import List, Optional, Tuple


from src.constants import Family, Person, Dimensions, PageInfo, Sex
import src.parse_gedcom as pg


def get_summary_text(person: Person, root) -> str:
    """
    Born 09/02/1981 in Szczecin, Poland. Married Edgar Häner at 29 and had a daughter at 29 and at 33.
    """
    text = ''
    name = person.first_name + ' ' + person.last_name
    text += get_even_text(name, 'was born', person.birth_date, person.birth_date_year, person.birth_place)
    text += ' ' + add_family_details(person, root)
    text += ' ' + get_even_text(person.first_name, 'died', person.death_date, person.death_date_year, person.death_place)
    text = text.replace('  ', ' ').replace(' .', '.')
    return text.strip()


def get_pronoun(person: Person):
    if person.sex == Sex.female:
        pronoun = 'She'
    else:
        pronoun = 'He'
    return pronoun


def get_pronoun_2(person: Person):
    if person.sex == Sex.female:
        pronoun = 'her'
    else:
        pronoun = 'him'
    return pronoun


def add_family_details(person: Person, root):
    text = ''
    pronoun = get_pronoun(person)
    name = person.first_name
    _, families = pg.get_all_families_for_individual(person.gedcom_element, root)
    for family in families:
        if family.parent1.gedcom_element.get_pointer() == person.gedcom_element.get_pointer():
            spouse = family.parent2
        else:
            spouse = family.parent1

        event = 'married'
        if spouse:
            event += ' {} {}'.format(spouse.first_name, spouse.last_name)
        mtext = get_even_text(name, event, family.marriage_date, family.marriage_date_year, family.marriage_place)
        text += mtext

        text += ' {} had {} children'.format(pronoun, len(family.children))
        if spouse is not None:
            if mtext:
                text += ' with {}'.format(get_pronoun_2(spouse))
            else:
                text += ' with {} {}'.format(spouse.first_name, spouse.last_name)

        if person.birth_date:
            have_children_date, ctext = False, ', aged '
            ages = []
            for child in family.children:
                if child.birth_date or child.birth_date_year:
                    have_children_date = True
                    if child.birth_date:
                        delta = child.birth_date - person.birth_date
                        ages.append(math.floor(delta.days/365))
            ages = sorted(ages)
            ages = [str(x) for x in ages]
            if len(ages) < 3:
                ctext = ctext + ' and '.join(ages) + '.'
            else:
                ctext = ctext + ', '.join(ages[:-2]) + ', ' + ' and '.join(ages[-2:]) + '. '
            if have_children_date:
                text += ctext
            else:
                text += '. '
        else:
            text += '. '
    return text


def get_even_text(pronoun: str, action: str, date: Optional[dt], date_year: Optional[int], place: Optional[str]) -> str:
    text = ''
    date_str = None
    if date:
        date_str = date.strftime('%d/%m/%Y')
    elif date_year:
        date_str = str(date_year)

    if date_str or place:
        text += '{} {} '.format(pronoun, action)
        if date_str:
            text += '{} '.format(date_str)
        if place:
            text += ' in {}. '.format(place)
        else:
            text += '. '
    return text.strip()


def get_birth_date(person: Person) -> Optional[str]:
    date_str = None
    if person.birth_date:
        date_str = person.birth_date.strftime('%d/%m/%Y')
    elif person.birth_date_year:
        date_str = str(person.birth_date_year)
    return date_str


def get_death_date(person: Person) -> Optional[str]:
    date_str = None
    if person.death_date:
        date_str = person.birth_date.strftime('%d/%m/%Y')
    elif person.death_date_year:
        date_str = str(person.birth_date_year)
    return date_str