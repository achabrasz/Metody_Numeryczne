a = 4;
r_max = 2;
n_max = 200;
[circles, index_number, circle_areas, rand_counts, counts_mean] = generate_circles(a, r_max, n_max);
plot_counts_mean(counts_mean);