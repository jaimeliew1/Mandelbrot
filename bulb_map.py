from mandlebrot import mandelbrot
import matplotlib.pyplot as plt
from moviepy.editor import VideoClip
from moviepy.video.io.bindings import mplfig_to_npimage
import numpy as np


def CtoB(Zc):
    Zb = (Zc**2 + 2j*Zc - 1)/(Zc**2 + 1)
    return Zb

def BtoA(Zb):
    Za = Zb/2*(1 - Zb/2)
    return Za


def mandelbrot(c):
    """
    Yields the Mandelbrot set at each iteration.

    args:
        c (nx x nx array):
    Yields:
        Mand (nx x nx array): Mandelbrot set for the next iteration.
    """

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

    def __init__(self, N, duration, nxpb=500, fps=20):
        """
        args:
            N (int): number of bulbs
            duration (float): GIF duration in seconds.
            nxpb (int): X discretisation per bulb (default=500).
            fps (int): frames per second.
        """

        xC = np.linspace(0, 1/np.tan(np.pi/N), N*nxpb)
        yC = np.linspace(0, 1/3, nxpb)
        cC = xC[:, np.newaxis] + 1j * yC[np.newaxis, :]
        cB = CtoB(cC)
        cA = BtoA(cB)
        self.mandelbrot_gen = mandelbrot(cA)

        self.duration = duration
        self.fps = fps
        self.image = np.zeros(cA.shape)

    def iterate(self, t):
        """
            Performs one iteration of the Mandelbrot calculation and returns the
            figure plotting the cumulative iterations.
        """
        mand = next(self.mandelbrot_gen)
        self.image += np.array(mand, dtype=float) * t / self.duration

        fig = plt.figure()
        plt.imshow(np.flipud(self.image.T),
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


if __name__ == '__main__':

    mandelbrot_gif = MandelbrotImage(20, 10, nxpb=500)
    mandelbrot_gif.make_gif('transform.gif')
    # N = 20 # Max bulb number
    # N_iter = 100
    # xC = np.linspace(0, 1/np.tan(np.pi/N), 10000)
    # yC = np.linspace(0, 1/3, 1000)
    # cC = xC[:, np.newaxis] + 1j * yC[np.newaxis, :]
    # cB = CtoB(cC)
    # cA = BtoA(cB)
    # mandelbrot_gen = mandelbrot(cA)
    # image = np.zeros(cC.shape)
    # for i in range(N_iter):
    #     mand = next(mandelbrot_gen)
    #     image += np.array(mand, dtype=float) * i/ N_iter
    #
    # fig = plt.figure()
    # plt.imshow(np.flipud(image.T),
    #            cmap='nipy_spectral_r',
    #            interpolation='bilinear')
    # plt.axis('off')
    # plt.show()
    #
    # X, Y, width, nx = 0, 0, 2, 500
    # mandelbrot_gen = mandelbrot(X, Y, width, nx)
    # for i in range(20):
    #     next(mandelbrot_gen)
    #
    # mand = next(mandelbrot_gen)
    #
    # x = np.linspace(X - width, X + width, nx)
    # y = np.linspace(Y - width, Y + width, nx)
    # c = x[:, np.newaxis] + 1j * y[np.newaxis, :]
    # c2 = 1-np.sqrt(1 - 4*c)
    #
    # plt.contourf(c2.real, c2.imag, mand,
    #            cmap='nipy_spectral_r',
    #            interpolation='bilinear')
    #
    # for i in [2, 3, 4]:
    #     x, y = np.cos(2*np.pi/i), np.sin(2*np.pi/i)
    #     plt.plot([0, x], [0, y], '--k', lw=1)
    # plt.show()
