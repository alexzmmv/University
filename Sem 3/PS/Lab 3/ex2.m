clearvars
p=0
while p<0.05 || p>0.95
    p=input("Enter the probability of succes(0.05<p<0.95): ");
end

for n=0:5:100
    k=0:n;
    p1=binopdf(k,n,p);
    kreal=0:0.01:n;
    p2=normpdf(kreal,n*p,sqrt(n*p*(1-p)));
    plot(k,p1,'*',kreal,p2)
    title(['n = ',num2str(n)])
    legend('Binomial','Normal')
    pause(0.5)
end