%Diman Single run
%Diman Plots
%
% Cascade Prevention

%Threshold = 1
Cost_0_mon = textread('Result_Costs_Cascade_1.0_Thr_0.0_DesMon_360_N_1_repeat_.txt',' %f');
Power_0_mon = textread('Result_Power_Cascade_1.0_Thr_0.0_DesMon_360_N_1_repeat_.txt',' %f');

Cost_20_mon = textread('Result_Costs_Cascade_1.0_Thr_0.2_DesMon_360_N_1_repeat_.txt',' %f');
Power_20_mon = textread('Result_Power_Cascade_1.0_Thr_0.2_DesMon_360_N_1_repeat_.txt',' %f');

Cost_40_mon = textread('Result_Costs_Cascade_1.0_Thr_0.4_DesMon_360_N_1_repeat_.txt',' %f');
Power_40_mon = textread('Result_Power_Cascade_1.0_Thr_0.4_DesMon_360_N_1_repeat_.txt',' %f');

Cost_60_mon = textread('Result_Costs_Cascade_1.0_Thr_0.6_DesMon_360_N_1_repeat_.txt',' %f');
Power_60_mon = textread('Result_Power_Cascade_1.0_Thr_0.6_DesMon_360_N_1_repeat_.txt',' %f');

Cost_80_mon = textread('Result_Costs_Cascade_1.0_Thr_0.8_DesMon_360_N_1_repeat_.txt',' %f');
Power_80_mon = textread('Result_Power_Cascade_1.0_Thr_0.8_DesMon_360_N_1_repeat_.txt',' %f');

Cost_No_prev = textread('Result_Costs_No_control_Cascade_1.0_Thr_0.0_DesMon_360_N_1_repeat_.txt',' %f');
Power_No_prev = textread('Result_Power_No_Control_Cascade_1.0_Thr_0.0_DesMon_360_N_1_repeat_.txt',' %f');


x=0:100/360:100-100/360;
plot(x, abs(Power_0_mon), 'b')
xlabel('Percentage of Disruption');
ylabel('Total Power Delivered (pu)');
%No Cascade Prevention:
xlabel('Percentage of Disruption');
ylabel('Total Power Delivered (pu)');



hold on
plot(x, abs(Power_20_mon), 'r')
hold on
plot(x, abs(Power_40_mon), 'y')
hold on
plot(x, abs(Power_60_mon), 'c')
hold on
plot(x, abs(Power_80_mon), 'g')
hold on
plot(x, abs(Power_No_prev), 'k')

xlabel('Percentage of Disruption');
ylabel('Total Power Delivered (pu)');
legend('0% monitor disruption','20% monitor disruption','40% monitor disruption', '60% monitor disruption', '80% monitor disruption', 'No Cascade Prevention');
figure;
plot(x, abs(Cost_0_mon), 'b')
hold on 
plot(x, abs(Cost_20_mon), 'r')
hold on
plot(x, abs(Cost_40_mon), 'y')
hold on
plot(x, abs(Cost_60_mon), 'c')
hold on
plot(x, abs(Cost_80_mon), 'g')
hold on
plot(x, abs(Cost_No_prev), 'k')
xlabel('Percentage of Disruption');
ylabel('Total Cost');
%legend('Continuous Cascade Prevention','Discrete Power Optimization', 'No Cascade Prevention');
legend('0% monitor disruption','20% monitor disruption','40% monitor disruption', '60% monitor disruption', '80% monitor disruption', 'No Cascade Prevention');



