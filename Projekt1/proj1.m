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

x=[];
y=[];
z=[];

n=[];
e=[];
u=[];

nr=[];

A=[];
s=[];
zz=[];

for id = 1:length(phi)
    tempNeu=geo2neu(phi(id), lambda(id), h(id), phiB, lambdaB, hB, a, e2);
    [x(id),y(id),z(id)]=geo2xyz(phi(id), lambda(id), h(id), a, e2);
    n(id)=tempNeu(1);
    e(id)=tempNeu(2);
    u(id)=tempNeu(3);
    nr(id)=id;
    
    A(id)=atand(e(id)/n(id));
    if(n(id)<0 && e(id)>0)
        A(id)=A(id)+180;
    elseif(n(id)<0 && e(id)<0)
        A(id)=A(id)+180;
    else
        A(id)=A(id)+360;
    end
    if(A(id)>360)
        A(id)=A(id)-360;
    end
    if(A(id)<0)
        A(id)=A(id)+360;
    end
    
    s(id)=sqrt(n(id)^2+e(id)^2+u(id)^2);
    z(id)=acosd(u(id)/s(id));
end

figure(1)
plot3(n,e,u);
title('n e u')

figure(2)
plot3(x,y,z);
title('x y z')

figure(3)
plot(nr,h)
title('nr,h')

figure(4)
plot(nr,u)
title('nr,u)')

figure(5)
geoscatter(phi,lambda,5, 'ro');
title('geoscatter')


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
