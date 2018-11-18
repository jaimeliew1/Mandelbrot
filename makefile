DEF = $(wildcard *.txt)
GIF = $(DEF:.txt=.gif)

all: $(GIF)

%.gif: %.txt
	echo Making $<
	python mandlebrot.py $(shell cat $<)
	ffmpeg -y -f image2 -i _temp/mandelbrot%03d.png $@
	rm _temp/*.png
