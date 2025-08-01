clear all;
clc;
%a
a=0:3;
b=binopdf(a,3,0.5);
a=[a;b]

%b
c=0:0.1:3;
d=binocdf(c,3,0.5);
plot(c,d,"--");
title("CDF 3 coin flip");
legend("BINOCDF");

%c
P_0=binocdf(0,3,0.5);
fprintf("c) \n P(X=0)= %.3f \n", P_0);  % Print the result

%d
% P(x<=2)=CDF(2)
% P(x<2)=1-CDF(2)
%
%...
