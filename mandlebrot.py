# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 19:37:33 2018

@author: J

ffmpeg -f image2 -i mandelbrot%03d.png -vf scale=500x500 out4.gif
ffmpeg -f image2 -i mandelbrot%03d.png  out6.gif
"""
import sys
import numpy as np
import matplotlib.pyplot as plt
from contextlib import contextmanager

interp = 'bilinear'
N_max = 400
nx = 1000

#x = np.linspace(-2, 1, nx)
#y = np.linspace(-1.5, 1.5, ny)
#X, Y, R = -0.925, -0.266, 0.032
#X, Y, R = -0.16, 1.0405, 0.026
#X, Y, R = -0.745428, 0.113009, 3e-5
#X, Y, R = -0.748, 0.1, 0.0014
'''
-1.25066 0.02012 1.7e-4

'''


def mandelbrot(X, Y, R, nx, N_max):
    x = np.linspace(X - R, X + R, nx)
    y = np.linspace(Y - R, Y + R, nx)
    c = x[:,np.newaxis] + 1j*y[np.newaxis,:]
    z = c
    for j in range(N_max):
        z = z**2 + c
        yield abs(z) < 2



@contextmanager
def make_image(idx):
    plt.figure(figsize=[7,7])

    yield plt.gca()
    plt.axis('off')
    plt.savefig('_temp/mandelbrot{:03d}.png'.format(idx), dpi=200)
    plt.close()
    #plt.show()
    #print()



if __name__ == '__main__':

    X, Y, R, nx, Nmax = [float(arg) for arg in sys.argv[1:]]
    image = np.zeros([nx, nx])
    idx = 0
    for j, mand in enumerate(mandelbrot(X, Y, R, nx, N_max)):
        image += np.array(mand, dtype=float)*j/N_max
        if all(x for x in mand.ravel()):
            continue
        with make_image(idx) as ax:
            ax.imshow(image.T, cmap='nipy_spectral_r', interpolation=interp)
        print(f'\r{j}/{N_max}', end='')
        idx += 1

    with open('_temp/complete.txt', 'w') as f:
        f.write('complete')
