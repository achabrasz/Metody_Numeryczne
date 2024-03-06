function [numer_indeksu, Edges, I, B, A, b, r] = page_rank()
numer_indeksu = 193373;
L1 = 7;
L2 = 3;
kol = [1,2,3,4,5,6,7,8];
Edges = [1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 6, 6, 7, 8;
         4, 6, 3, 4, 5, 5, 6, 7, 5, 6, 8, 4, 6, 4, 7, 6, 1];
I = speye(8);
B = sparse(Edges(2,:), Edges(1,:), 1, 8, 8);
A = spdiags((sum(B).^-1)', 0, 8, 8);
b = ones(8,1);
for i = 1:8
    b(i,1) = (1 - 0.85)/8;
end
M = I - 0.85*B*A;
r = M\b;

end