clear all
close all
format compact

n_max = 200;
a = 4;
r_max = 2;



[circles, index_number] = generate_circles(a, r_max, n_max);
plot_circles(a, circles, index_number); 
%print -dpng zadanie1.png 

function [circles, index_number] = generate_circles(a, r_max, n_max)
index_number = 193373; % numer Twojego indeksu
L1 = 3;

circles = zeros(3,n_max);

for i = 1:n_max
    check = 0;
    while(check == 0)
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
    circles(:, i) = [R; X; Y];
end

end

function [circles, index_number] = plot_circles(a, circles, index_number)
figure;
hold on;
axis equal;
axis([0 a 0 a]);
for i = 1:size(circles, 2)
    plot_circle(circles(1, i), circles(2, i), circles(3, i));
    pause(0.1);
end


end