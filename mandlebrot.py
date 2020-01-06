# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 19:37:33 2018

@author: Jaime Liew
"""
import numpy as np
import matplotlib.pyplot as plt
from moviepy.editor import VideoClip
from moviepy.video.io.bindings import mplfig_to_npimage


def mandelbrot(X, Y, width, nx):
    """
    Yields the Mandelbrot set at each iteration, centered at X, Y.

    args:
        X (float): X (real) coordinate of interest.
        Y (float): Y (imaginary) coordinate of interest.
        width (float): Frame width.
        nx (int): X and Y discretization.
    Yields:
        Mand (nx x nx array): Mandelbrot set for the next iteration.
    """

    x = np.linspace(X - width, X + width, nx)
    y = np.linspace(Y - width, Y + width, nx)
    c = x[:, np.newaxis] + 1j * y[np.newaxis, :]
    z = c

    z = z ** 2 + c
    mand = abs(z) < 2

    while mand.all():
        z = z ** 2 + c
        mand = abs(z) < 2

    yield mand

    while True:
        z = z ** 2 + c
        mand = abs(z) < 2
        yield mand


class MandelbrotImage(object):
    """
     Class that creates an animated gif of the mandelbrot set at a given
     location.
    """

    def __init__(self, x, y, width, duration, figsize=4, nx=500, fps=20):
        """
        args:
            X (float): X (real) coordinate of interest.
            Y (float): Y (imaginary) coordinate of interest.
            width (float): Frame width.
            duration (float): GIF duration in seconds.
            figsize (float): figure side length (default=4).
            nx (int): X and Y discretisation (default=500).
            fps (int): frames per second.
        """
        self.mandelbrot_gen = mandelbrot(x, y, width, nx=nx)
        self.duration = duration
        self.figsize = figsize
        self.fps = fps
        self.image = np.zeros((nx, nx))

    def iterate(self, t):
        """
            Performs one iteration of the Mandelbrot calculation and returns the
            figure plotting the cumulative iterations.
        """
        mand = next(self.mandelbrot_gen)
        self.image += np.array(mand, dtype=float) * t / self.duration

        fig = plt.figure(figsize=(self.figsize, self.figsize))
        plt.imshow(self.image.T,
                   cmap='nipy_spectral_r',
                   interpolation='bilinear')
        plt.axis('off')
        return fig

    def make_gif(self, file_name):
        def make_frame(t):
            fig = self.iterate(t)
            img = mplfig_to_npimage(fig)
            plt.close(fig)
            return img

        animation = VideoClip(make_frame, duration=self.duration)
        animation.write_gif(file_name, fps=self.fps)


def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    demo_or_manual = parser.add_mutually_exclusive_group()

    demo_or_manual.add_argument("--demo", action="store_true")

    manual = demo_or_manual.add_argument_group()

    manual.add_argument("-f", "--file_name", dest="file_name", default="mandelbrot.gif",
                        help="Output file name.")
    manual.add_argument("-d", "--dims", dest="dims", type=int, default=500,
                        help="Output image width (and height).")
    manual.add_argument("-x", dest="x", default=-0.235125, type=float,
                        help="Center of Mandlebrot image in x.")
    manual.add_argument("-y", dest="y", default=0.827215, type=float,
                        help="Center of Mandlebrot image in y.")
    manual.add_argument("-w", "--width", dest="width", default=4.0E-5, type=float,
                        help="Width of Mandelbrot image in xy plane.")
    manual.add_argument("-s", "--seconds", dest="seconds", default=10, type=float,
                        help="Duration of gif in seconds.")
    manual.add_argument("--fps", dest="fps", default=20, type=int,
                        help="Frames per second for the output gif.")

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    if args.demo:
        params = {  # filename: (X, Y, R, duration)
            'out1.gif': (-0.235125, 0.827215, 4.0E-5, 10),
            'out2.gif': (-0.925, -0.266, 0.032, 10),
            'out3.gif': (-0.745428, 0.113009, 3e-5, 10),
            'out4.gif': (-0.748, 0.1, 0.0014, 20),
        }

        for filename, (X, Y, R, duration) in params.items():
            mandelbrot_gif = MandelbrotImage(X, Y, R, duration)
            mandelbrot_gif.make_gif(filename)
    else:
        mandelbrot_gif = MandelbrotImage(args.x, args.y, args.width, args.seconds, 4, args.dims, args.fps)
        mandelbrot_gif.make_gif(args.file_name)
