default:
	gcc -o a.out fft.c test.c
plot:
	gnuplot plot_data.plg
clean:
	rm -f *.out
clean_all: clean
	rm -f *.png data/* plots/*
