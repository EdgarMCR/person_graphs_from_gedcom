from unittest import TestCase

from src.constants import Person, Family, Dimensions
import src.plotting.plotting as pl
import src.plotting.utility as pu

import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])


class TestUtility(TestCase):
    def test_plot_rectangle(self):

        fig = Figure()
        canvas = FigureCanvas(fig)

        dimensions = Dimensions((1, 1), 1, 1, (3, 3))
        pl.plot_rectangle(dimensions, fig)

        canvas.draw()       # draw the canvas, cache the renderer
        width, height = fig.get_size_inches() * fig.get_dpi()
        width, height = int(width), int(height)
        img = np.fromstring(canvas.tostring_rgb(), dtype='uint8').reshape(height, width, 3)
        image = rgb2gray(img )
        h, w = image.shape
        self.assertTrue(image[:int(h/3-2), :].all() == 255)

