clear variables;
%a) bernoulie
clear variables;
S=input("What is the number of sim=");
p=input("prob of succes=");

U=rand(1,S);
X=U<p;
U_x=unique(X);
freq=hist(X,length(U_x))/S;
[U_x;freq]

 
%b) binomial
S=input("What is the number of sim=");
p=input("prob of succes=");
n=input("number of trials=")
U=rand(n,S);
X=sum(U<p);
X=X;
U_x=unique(X);
freq=hist(X,length(U_x));
B_x=[0:n];
B_y=binopdf(B_x,n,p);
plot(U_x,freq,"*",B_x,B_y,'o');

%c) geometric
S=input("What is the number of sim=");
p=input("prob of succes=");
freq=[]
for i=1:n
    genn=0
    num=0
    while genn~=0
        num=num+1;
        genn=rand(0,1)>p;
    end
    freq(i)=num;
end

%d) pascal

