clear; 
a=6378137; 
e2=0.00669437999013; 
%wsp samolotu 
macierzDane=load('daneMoje1.txt'); 
phi=macierzDane(:,1);  
lambda=macierzDane(:,2); 
h=macierzDane(:,3); 
%wsp lotniska 
phiB=38.774167;
lambdaB=-9.134167;
hB=114;


[x,y,z]=geo2xyz(1,1,1,a,e2);

%---Funkcje---
%Obliczanie x,y,z
function[x,y,z]=geo2xyz(phi,lambda,h,a,e2)
phiRad=deg2rad(phi);
lambdaRad=deg2rad(lambda);
N=a/sqrt(1-e2*sin(phiRad)^2);
x=(N+h)*cos(phiRad)*cos(lambdaRad);
y=(N+h)*cos(phiRad)*sin(lambdaRad);
z=(N*(1-e2)+h)*sin(phiRad);
end

