# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 19:37:33 2018

@author: Jaime Liew
"""
import numpy as np
import matplotlib.pyplot as plt
from moviepy.editor import VideoClip
from moviepy.video.io.bindings import mplfig_to_npimage


def mandelbrot(X, Y, R, nx):
    '''
    Yields the Mandelbrot set at each iteration at a given location.

    args:
        X (float): X (real) coordinate of interest.
        Y (float): Y (imaginary) coordinate of interest.
        R (float): Frame 'radius'.
        nx (int): X and Y discretisation.
    Yields:
        Mand (nx x nx array): Mandelbrot set for the next iteration.
    '''

    x = np.linspace(X - R, X + R, nx)
    y = np.linspace(Y - R, Y + R, nx)
    c = x[:, np.newaxis] + 1j * y[np.newaxis, :]
    z = c
    while True:
        z = z**2 + c
        mand = abs(z) < 2

        # Ignore initial 'blank' iterations.
        if all(x for x in mand.ravel()):
            continue
        else:
            yield mand


class Mandelbrot_image(object):
    '''
     Class that creates an animated gif of the mandelbrot set at a given
     location.
    '''
    def __init__(self, X, Y, R, T_max, figsize=4, nx=500):
        '''
        args:
            X (float): X (real) coordinate of interest.
            Y (float): Y (imaginary) coordinate of interest.
            R (float): Frame 'radius'.
            T_max (float): GIF length in seconds.
            figsize (float): figure side length (default=4).
            nx (int): X and Y discretisation (default=500).
        '''
        self.mandelbrot_gen = mandelbrot(X, Y, R, nx=nx)
        self.T_max = T_max
        self.figsize = figsize
        self.image = np.zeros([nx, nx])

    def iterate(self, t):
        '''
            Performs one iteration of the Mandelbrot calculation and returns the
            figure plotting the cumulative iterations.
        '''
        mand = next(self.mandelbrot_gen)
        self.image += np.array(mand, dtype=float) * t / self.T_max

        fig = plt.figure(figsize=[self.figsize, self.figsize])
        plt.imshow(self.image.T,
                   cmap='nipy_spectral_r',
                   interpolation='bilinear')
        plt.axis('off')
        return fig

    def make_gif(self, filename):
        def make_frame(t):
            fig = self.iterate(t)
            return mplfig_to_npimage(fig)

        animation = VideoClip(make_frame, duration=self.T_max)
        animation.write_gif(filename, fps=20)


if __name__ == '__main__':
    params = { # filename: (X, Y, R, T_max)
        'out1.gif': (-0.235125, 0.827215, 4.0E-5, 10),
        'out2.gif': (-0.925, -0.266, 0.032, 10),
        'out3.gif': (-0.745428, 0.113009, 3e-5, 10),
        'out4.gif': (-0.748, 0.1, 0.0014, 20),
    }

    for filename, (X, Y, R, T_max) in params.items():
        mandelbrot_gif = Mandelbrot_image(X, Y, R, T_max)
        mandelbrot_gif.make_gif(filename)
