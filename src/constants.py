from datetime import datetime as dt
from dataclasses import dataclass, field
from typing import Optional, List, Tuple


class Sex:
    male = 'M'
    female = 'F'


@dataclass
class Person:
    first_name: str = ''
    last_name: str = ''

    birth_date: Optional[dt] = None
    birth_date_year: Optional[int] = None
    birth_place: str = ''

    death_date: Optional[dt] = None
    death_date_year: Optional[int] = None
    death_place: str = ''

    sex: Optional[Sex] = None

    gedcom_element = None

    parent_family: Optional[object] = None
    families: List = field(default_factory=list)


@dataclass
class Family:
    parent1: Optional[Person]
    parent2: Optional[Person]

    children: List[Person]

    marriage_date: Optional[dt] = None
    marriage_date_year: Optional[int] = None
    marriage_place: str = ''

    divorce_date: Optional[dt] = None
    divorce_date_year: Optional[int] = None
    divorce_place: str = ''

    # TODO: this shouldn't really be part of this dataclase - keep data and plotting separate!
    one_child_already_plotted: bool = False
    child_already_plotted_position: Tuple[float, float] = (0, 0)

    father_plotted_top: bool = False

    father_already_plotted: bool = False
    mother_already_plotted: bool = False
    spouse_already_plotted_position: Tuple[float, float] = (0, 0)

    gedcom_element = None


@dataclass
class Dimensions:
    position: Tuple[float, float]
    width: float
    height: float
    page_size: Tuple[float, float]


@dataclass
class TextInfo:
    text: str
    font_size: float


@dataclass
class BoxPlotInfo:
    x: float
    y: float
    w: float  # width
    h: float  # height

    lines: List[TextInfo]


@dataclass
class LinePlotInfo:
    start: Tuple[float, float]
    end: Tuple[float, float]
    width: float = 0.001


@dataclass
class PageInfo:
    page_width: float
    page_height: Optional[float]

    margin: Tuple[float, float]
    gap: Tuple[float, float]
    minimum_gap_y: float

    indentation: float = 0.1
    font_size_large: int = 12
    font_size_small: int = 6

    # to be used internally, should I split this into another class?
    dpi: float = 72.
    box_size: Tuple[float, float] = (0, 0)
    stride: Tuple[float, float] = (0, 0)
    num_cols: int = 3
    column_top_position: List = field(default_factory=lambda: [0, 0, 0])
    column_x: List = field(default_factory=lambda: [0, 0, 0])





