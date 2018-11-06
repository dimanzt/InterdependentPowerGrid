%Result_Power_Cascade_0.4_Thr_0.0_DesMon_360_N_1_repeat_
%Result_Power_Cascade_0.4_Thr_0.4_DesMon_360_N_1_repeat_
%Diman Single run
%Diman Plots
%
% Cascade Prevention

%Cost = textread('Result_Costs_Cascade_0.4_Thr_0.0_DesMon_360_N_1_repeat_.txt',' %f');
%Power = textread('Result_Power_Cascade_0.4_Thr_0.0_DesMon_360_N_1_repeat_.txt',' %f');
Cost = textread('Result_Costs_Cascade_1.0_Thr_0.0_DesMon_360_N_10_repeat_.txt',' %f');
Power = textread('Result_Power_Cascade_1.0_Thr_0.0_DesMon_360_N_10_repeat_.txt',' %f');

Cost2 = textread('Result_Costs_Cascade_1.0_Thr_0.4_DesMon_360_N_10_repeat_.txt',' %f');
Power2 = textread('Result_Power_Cascade_1.0_Thr_0.4_DesMon_360_N_10_repeat_.txt',' %f');


%Cost2 = textread('Result_Costs_Cascade_0.4_Thr_0.4_DesMon_360_N_1_repeat_.txt',' %f');
%Power2 = textread('Result_Power_Cascade_0.4_Thr_0.4_DesMon_360_N_1_repeat_.txt',' %f');

x=0:100/360:100-100/360;
plot(x, abs(Power), 'b')
xlabel('Percentage of Disruption');
ylabel('Total Power Delivered (pu)');
%No Cascade Prevention:
xlabel('Percentage of Disruption');
ylabel('Total Power Delivered (pu)');

Cost3 = textread('Result_Costs_Cascade_0.4_Thr_0.4_DesMon_360_N_1_repeat_.txt',' %f');
Power3 = textread('Result_Power_Cascade_0.4_Thr_0.4_DesMon_360_N_1_repeat_.txt',' %f');


hold on
plot(x, abs(Power2), 'r')
hold on
plot(x, abs(Power3), 'g')

xlabel('Percentage of Disruption');
ylabel('Total Power Delivered (pu)');
legend('Continuous Cascade Prevention','Discrete Power Optimization', 'No Cascade Prevention');
figure;
plot(x, abs(Cost), 'b')
hold on 
plot(x, abs(Cost2), 'r')
hold on
plot(x, abs(Cost3), 'g')
xlabel('Percentage of Disruption');
ylabel('Total Cost');
legend('Continuous Cascade Prevention','Discrete Power Optimization', 'No Cascade Prevention');



