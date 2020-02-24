x = linspace(0,.1,20);
Tau = zeros(1,length(x));
data_95 = importdata('center_cavity_U_y=.95_re=500.xy');
data_99 = importdata('center_cavity_U_y=.99_re=500.xy');
U_95 = data_95(:,5);
U_99 = data_99(:,5);
re = [10, 50, 100, 500];
formatspecs_95 = "center_cavity_U_y=.95_re=%d%s";
formatspecs_99 = "center_cavity_U_y=.99_re=%d%s";
filetype = '.xy';

for j = 1:4
    Re = re(j);
    filename_95 = sprintf(formatspecs_95,Re,filetype);
    filename_99 = sprintf(formatspecs_99,Re,filetype);
    data_95 = importdata(filename_95);
    data_99 = importdata(filename_99);
    U_95 = data_95(:,5);
    U_99 = data_99(:,5);
    for i = 1:length(x)
        Tau(j,i) = (U_99(i)-U_95(i))/(0.04); 
    end   
end

    figure
    plot((x.*10), Tau(1,:))
    title("Stress along cavity lid, variable Re")
    xlabel("X (m)")
    ylabel("Tau (N/m)")


