clear all;
clc;

n=input("Number of trials: ");
p=input("Probability of success: ");

k=0:n;
px = binopdf(k,n,p)
kr=0:0.01:n;
fx=binocdf(kr,n,p);

plot(k,px,"*")

hold on;

plot(kr,fx,"");

hold off;

title("The Bionmial model");
legend("pdf","cdf");

%disttool 