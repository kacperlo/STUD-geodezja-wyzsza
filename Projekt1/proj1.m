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