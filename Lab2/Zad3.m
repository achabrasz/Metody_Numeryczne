a = 4;
r_max = 2;
n_max = 200;
[circles, index_number, circle_areas] = generate_circles(a, r_max, n_max);
plot_circle_areas(circle_areas);