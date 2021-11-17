clear; 
a=6378137; 
e2=0.00669437999013; 
%wsp samolotu 
macierzDane=load('daneMoje2.txt'); 
phi=macierzDane(:,1);  
lambda=macierzDane(:,2); 
h=macierzDane(:,3); 
%wsp lotniska 
phiB=38.774167;
lambdaB=-9.134167;
hB=114;


[x,y,z]=geo2xyz(1,1,1,a,e2);

%---Funkcje---
%Obliczanie xyz
function[x,y,z]=geo2xyz(phi,lambda,h,a,e2)
    N=a/sqrt(1-e2*sind(phi)^2);
    x=(N+h)*cosd(phi)*cosd(lambda);
    y=(N+h)*cosd(phi)*sind(lambda);
    z=(N*(1-e2)+h)*sind(phi);
end
%Obliczanie delt
function[deltas]=countDelta(x1, y1, z1, x2, y2, z2)
    deltas=[x1-x2;
        y1-y2;
        z1-z2];
end
%Obliczanie neu
function[neu]=geo2neu(phi, lambda, h, phiB, lambdaB, hB, a, e2)
    R=[-sind(phiB)*cosd(lambdaB) -sind(lambdaB) cosd(phiB)*cosd(lambdaB);
        -sind(phiB)*sind(lambdaB) cosd(lambdaB) cosd(phiB)*sind(lambdaB);
        cosd(phiB) 0 sind(phiB)];
    
    [x,y,z]=geo2xyz(phi,lambda,h,a,e2);
    [xb,yb,zb]=geo2xyz(phiB,lambdaB,hB,a,e2);
    
    deltas=countDelta(x,y,z,xb,yb,zb);
    neu=R'*deltas;
end
