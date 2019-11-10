# Set Terminal to PNG Output
set terminal png;
set output "fft_plot.png";

# Plot data from "RES"
plot "data/RES" using 1:2 with lines;
