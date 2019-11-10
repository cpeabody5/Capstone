default:
	gcc -o a.out fft.c test.c
plot:
	gnuplot plot_data.gplot && open fft_plot.png
clean:
	rm *.out
clean_all: clean
	rm *.png */RES
