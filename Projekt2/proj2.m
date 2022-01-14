clear;

re=4.5986775;
de=16.50930277777778;

hours=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23];

lambda=[37,37,37];
phi=[75,0,-75];

A=[];
Z=[];

x=[];
y=[];
z=[];

[xs,ys,zs] = sphere;      %# Makes a 21-by-21 point sphere
r = 1;                 %# A radius value

%-----PÓŁNOCNA-----
for i=1:24
    A(i) = countA(katgodz(2021,05,13,i-1,lambda(1),re),phi(1),de);
    Z(i) = countZ(katgodz(2021,05,13,i-1,lambda(1),re),phi(1),de);
    x(i) = 1*sind(Z(i))*cosd(A(i));
    y(i) = 1*sind(Z(i))*sind(A(i));
    z(i) = 1*cosd(Z(i));
end

figure(1)
plot(hours,Z)
title('Wykres zależności wysokości zenitalnej od czasu (półkula północna)')
xlabel('Czas [h]');
xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, ...
13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]);
ylabel('Wysokość nad horyzontem [°]');

figure(2)
plot(hours,A)
title('Wykres zależności azymutu od czasu (półkula północna)')
xlabel('Czas [h]');
xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, ...
13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]);
ylabel('Azymut [°]');

figure(7)
hSurface=surf(r.*xs,r.*ys,r.*zs);        %# Make the scaling on the x, y, and z axes equal
shading interp
hold on;
set(hSurface,'FaceColor',[0 1 0], ...
      'FaceAlpha',0.5,'FaceLighting','gouraud','EdgeColor','none')
plot3(x,y,z,'o');
hold off;



%-----RÓWNIK-----
for i=1:24
    A(i) = countA(katgodz(2021,05,13,i-1,lambda(2),re),phi(2),de);
    Z(i) = countZ(katgodz(2021,05,13,i-1,lambda(2),re),phi(2),de);
    x(i) = 1*sind(Z(i))*cosd(A(i));
    y(i) = 1*sind(Z(i))*sind(A(i));
    z(i) = 1*cosd(Z(i));
end

figure(3)
plot(hours,Z)
title('Wykres zależności wysokości zenitalnej od czasu (równik)')
xlabel('Czas [h]');
xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, ...
13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]);
ylabel('Wysokość nad horyzontem [°]');

figure(4)
plot(hours,A)
title('Wykres zależności azymutu od czasu (równik)')
xlabel('Czas [h]');
xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, ...
13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]);
ylabel('Azymut [°]');

figure(8)
hSurface=surf(r.*xs,r.*ys,r.*zs);        %# Make the scaling on the x, y, and z axes equal
shading interp
hold on;
set(hSurface,'FaceColor',[0 1 0], ...
      'FaceAlpha',0.5,'FaceLighting','gouraud','EdgeColor','none')
plot3(x,y,z,'o');
hold off;

%-----POŁUDNIOWA-----
for i=1:24
    A(i) = countA(katgodz(2021,05,13,i-1,lambda(3),re),phi(3),de);
    Z(i) = countZ(katgodz(2021,05,13,i-1,lambda(3),re),phi(3),de);
    x(i) = 1*sind(Z(i))*cosd(A(i));
    y(i) = 1*sind(Z(i))*sind(A(i));
    z(i) = 1*cosd(Z(i));
end

figure(5)
plot(hours,Z)
title('Wykres zależności wysokości zenitalnej od czasu (półkula południowa)')
xlabel('Czas [h]');
xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, ...
13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]);
ylabel('Wysokość nad horyzontem [°]');

figure(6)
plot(hours,A)
title('Wykres zależności azymutu od czasu (półkula południowa)')
xlabel('Czas [h]');
xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, ...
13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]);
ylabel('Azymut [°]');

figure(9)
hSurface=surf(r.*xs,r.*ys,r.*zs);        %# Make the scaling on the x, y, and z axes equal
shading interp
hold on;
set(hSurface,'FaceColor',[0 1 0], ...
      'FaceAlpha',0.5,'FaceLighting','gouraud','EdgeColor','none')
plot3(x,y,z,'o');
hold off;

%----------------------------------------------------------






%----------------------------------------------------------

function [t] = katgodz(y,m,d,h,lambda,re)
    jd = juliandate(datetime(y,m,d));
    g = GMST(jd); %stopnie
    UT1 = h*1.002737909350795; %godziny
    %obliczenie czasu gwiazdowego(w stopniach)
    S = UT1*15 + lambda + g;
    %obliczenie kąta godzinnego(w stopniach)
    t = S - re*15;
    
    if t > 360
        t = t - 360;
    end
end 

function g = GMST(jd)
    T = (jd-2451545)/36525;
    g=280.46061837 + 360.98564736629*(jd-2451545)+0.000387933*T.^2-T.^3/38710000;
    g= mod(g,360); 
end

%Odleglosc zenitalna
function [z] = countZ(t,phi,de)
    z = acosd(sind(phi)*sind(de)+cosd(phi)*cosd(de)*cosd(t));
end

%Obliczanie azymutu
function A=countA(t,phi,delta)
  licznik=(-cosd(delta)*sind(t));
  mianownik=(cosd(phi)*sind(delta)-sind(phi)*cosd(delta)*cosd(t));
  A=atan2d(licznik, mianownik);
  if A > 360
      A = A - 360;
  elseif A < 0
      A = A + 360;
  end
end

