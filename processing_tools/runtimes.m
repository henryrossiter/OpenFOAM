gridN = [20, 40, 80, 160];
simTime = [1.362, 2.708, 4.525, 9.094];
gridNN = [400, 1600, 6400, 25600];
slopeEst = zeros(3);

for i = 1:3
       slope = (simTime(i+1) - simTime(i))/(gridNN(i+1) - gridNN(i));
       slopeEst(i) = slope;
end

alpha = mean(slopeEst, 'all')

figure
plot(log(gridNN), log(simTime))
title("C vs. N log-log plot")
xlabel("log(NxNy = number of grid points)")
ylabel("log(C = execution time of simulation)")
