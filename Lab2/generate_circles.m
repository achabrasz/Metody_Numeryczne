function [circles, index_number, circle_areas, rand_counts, counts_mean] = generate_circles(a, r_max, n_max)
index_number = 193373; % numer Twojego indeksu
L1 = 3;

circles = zeros(3,n_max);
rand_counts = zeros(1,n_max);
counts_mean = zeros(1,n_max);

for i = 1:n_max
    check = 0;
    randCount = 0;
    while(check == 0)
        randCount = randCount + 1;
        R = rand * r_max;
        X = rand * (a - 2*R) + R;
        Y = rand * (a - 2*R) + R;
        check = 1;
        for j = 1:i
            dystans = sqrt((X-circles(2,j))^2+(Y-circles(3,j))^2);
            if dystans <= abs(R + circles(1,j))
                check = 0;
            end
        end
    end
    rand_counts(i) = randCount;
    circles(:, i) = [R; X; Y];
end
circle_areas_1 = zeros(n_max,1);
for i = 1:n_max
    circle_areas_1(i, :) = circles(1, i)^2*pi;
    counts_mean(i) = mean(rand_counts(1:i));
end
circle_areas = cumsum(circle_areas_1);
end