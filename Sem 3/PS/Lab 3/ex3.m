clearvars
p=10
while p>0.05
    p=input("Enter the probability of succes(0.05<p): ");
end

for n=30:5:100
    k=0:n;
    p1=binopdf(k,n,p);
    p2=poisspdf(k,n*p);
    plot(k,p1,'*',k,p2,'o')
    title(['n = ',num2str(n)])
    legend('Binomial','Normal')
    pause(0.5)
end