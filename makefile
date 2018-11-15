.PHONY all

all: out.gif

out.gif: _temp/complete.txt
	ffmpeg -y -f image2 -i _temp/mandelbrot%03d.png out.gif
	rm _temp/*.png _temp/complete.txt

_temp/complete.txt:
	python mandlebrot.py -0.235125 0.827215 4.0E-5
