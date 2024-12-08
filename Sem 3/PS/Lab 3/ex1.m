clearvars


option=input("Enter the distr model (Normal, Student, chi2, Fisher): ", 's');
alfa=input("Enter alfa: ");
beta=input("Enter beta: ");	


switch option
    case 'Normal'
        fprintf("Normal distribution\n");
        mean=input("Enter the mean: ");
        std=input("Enter the standard deviation: ");
        ay1 = normcdf(0, mean, std);
        ay2 = 1-normcdf(0, mean, std);
        ay3 = normcdf(1, mean, std) - normcdf(-1, mean, std);
        ay4 = 1-(normcdf(1,mean,std)-normcdf(-1,mean,std));
        ay5=   norminv(alfa, mean, std);
        ay6=   norminv(1-beta, mean, std);
    case 'Student'
        fprintf("Student distribution\n");
        mean=input("Degree of freedom: ");
        ay1=tcdf(0, mean);
        ay2=1-tcdf(0,mean);
        ay3=tcdf(1,mean)-tcdf(-1,mean);
        ay4=1-(tcdf(1,mean)-tcdf(-1,mean));
        ay5=   tinv(alfa, mean);
        ay6=   tinv(1-beta, mean);
    case 'chi2'
        fprintf("Chi2 distribution\n");
        mean=input("Degree of freedom: ");
        ay1=chi2cdf(0, mean);
        ay2=1-chi2cdf(0,mean);
        ay3=chi2cdf(1,mean)-chi2cdf(-1,mean);
        ay4=1-(chi2cdf(1,mean)-chi2cdf(-1,mean));
        ay5=   chi2inv(alfa, mean);
        ay6=   chi2inv(1-beta, mean);
    case 'Fisher'
        fprintf("Fisher distribution\n");
        mean1=input("Degree of freedom 1: ");
        mean2=input("Degree of freedom 2: ");
        ay1=fcdf(0, mean1, mean2);
        ay2=1-fcdf(0,mean1,mean2);
        ay3=fcdf(1,mean1,mean2)-fcdf(-1,mean1,mean2);
        ay4=1-(fcdf(1,mean1,mean2)-fcdf(-1,mean1,mean2));
        ay5=   finv(alfa, mean1, mean2);
        ay6=   finv(1-beta, mean1, mean2);
    otherwise
        disp("Invalid option");
end

fprintf("a)\n");
fprintf("P(X<0) = %f\n", ay1);
fprintf("P(X>0) = %f\n", ay2);
fprintf("b)\n");
fprintf("P(-1<X<1) = %f\n", ay3);
fprintf("P(X<-1 or X>1) = %f\n", ay4);
fprintf("c)\n");
fprintf("X = %f\n", ay5);
fprintf("d)\n");
fprintf("X = %f\n", ay6);

