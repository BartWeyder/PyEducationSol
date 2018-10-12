syms y(t);
ode = diff(y,t) == 0.3*t + y^2;
cond = y(0) == 0.4;
ySol(t) = dsolve(ode, cond);
double(ySol(0));
double(ySol(1));
double(ySol(1.980));
