from unittest import TestCase

import matplotlib.pyplot as plt

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
        # Plot a square, 1x1 on a 3x3 canvas with top left corner being at (1,1)
        pl.plot_rectangle(dimensions, fig)

        canvas.draw()       # draw the canvas, cache the renderer
        width, height = fig.get_size_inches() * fig.get_dpi()
        width, height = int(width), int(height)
        img = np.fromstring(canvas.tostring_rgb(), dtype='uint8').reshape(height, width, 3)
        image = rgb2gray(img )
        # plt.imshow(image)
        # plt.show()
        h, w = image.shape

        # Get top third of image
        top_strip = image[:int(h/3-2), :]
        self.assertTrue(np.min(top_strip) > 254)  # Should be all white
        bottom_strip = image[int(2*h/3+100):, :]  # There is a shadow that extends a bit below the box
        self.assertTrue(np.min(bottom_strip) > 254)  # Should be all white

        left = image[:, :int(h/3-2)]
        self.assertTrue(np.min(left) > 254, 'left strip')  # Should be all white