# Author: Diman Zad Tootaghaj
import pydot # import pydot or you're not going to get anywhere my friend :D
import networkx as nx
#import my_lib as my_lib_var
import sys
#import winsound
import time
import itertools
from scipy import stats
import numpy as np
import copy
from numpy.linalg import svd
from my_lib_optimal_power import *
from numpy.linalg import matrix_rank
from my_lib_power import *
from my_lib_cascade import *
from my_lib_DC_Flow_Cascade import *
#https://www.diffchecker.com/efddo0xv

work_dir=os.getcwd()

#[Ghviet, Ggarr, h_inter, g_inter] = create_italian() 
italian = create_italian()
hviet = italian[0]
garr = italian[1]
h_inter = italian[2]
g_inter = italian[3]
num_nodes = len(garr.nodes())
print 'Number of nodes:'
print num_nodes
print 'HVIET:'
print hviet
print 'GARR:'
print garr
print 'h_inter:'
print h_inter
print 'g_inter:'
print g_inter
################################################################################################################################
nodes = []
power = []
linkNum = []
link1 = []
link2 = []
power, nodes, linkNum, link1, link2, reactances = read_hviet()

print 'Nodes:'
print nodes
print 'Power:'
print power
print 'Links1:'
print link1
print 'Links2:'
print link2
#################################################################################################################################
##############Start Greedy-Max-Rank Algorithm####################################################################################
All_Costs = []
All_power = []
flows = []
ILP_gen_power = []
ILP_load_power = []
cost = []
TotalPower = []
Thr= 0.7
Original_flows = []
print '################################# Start Solving the Power Flow Model ###################################################'
[Original_flows, ILP_gen_power, ILP_load_power, cost, TotalPower] = optimal_DC_Flow_Cascade(nodes, power, link1, link2, reactances, linkNum, Thr)
print 'Flows:'
print flows
print 'ILP_gen_power:'
print ILP_gen_power
print 'ILP_load_power:'
print ILP_load_power
#All_Costs.append(cost)
#All_power.append(TotalPower)
########################################Start the attack model:#################################################################
removed_edges = []
flows = []
Costs = []
Power = []
TotalPower = []
#ILP_gen_power = []
#ILP_load_power = []
N= 360 #360
repeat = 10 #10
Original_link1 = deepcopy(link1) #[]
Original_link2 = deepcopy(link2) #[]
Original_linkNum = deepcopy(linkNum) #[]
Original_reactances = deepcopy(reactances)#[]
"""
for i in link1:
    Original_link1.append(i)
for i in link2:
    Original_link2.append(i)
for i in linkNum:
    Original_linkNum.append(i)
for i in reactances:
    Original_reactances.append(i)
#Original_link1 = link1
#Original_link2 = link2
#Original_linkNum = linkNum
#Original_reactances = reactances
"""
Thr = 1
for j in range(0, repeat):
    for i in range(0, N):
        ILP_gen_power = []
        IP_load_power = []
        print 'I:'
        print i
        print 'J:'
        print j
        print 'Length link1'
        print len(link1)
        print 'Length Original link1:'
        print len(Original_link1)
        if (len(link1) != 0):
            rem = random.randint(0, len(link1)-1)
            print 'removed index:'
            print rem
            """
            del link1[0]
            del link2[0]
            del linkNum[0]
            del reactances[0]
            """
            del link1[rem]
            del link2[rem]
            del linkNum[rem]
            del reactances[rem]
        if rem not in removed_edges:
            removed_edges.append(rem)
            #del link1[i]
            #del link2[i]
            #del linkNum[i]
            #del reactances[i]
            #link1.remove(link1[i])
            #link2.remove(link2[i])
            #linkNum.remove(linkNum[i])
            #reactances.remove(reactances[i])
        if i <20:
            [flows, ILP_gen_power, ILP_load_power, cost, TotalPower] = optimal_DC_Flow_Cascade(nodes, power, link1, link2,reactances, linkNum, 0.7)
        else:
            [flows, ILP_gen_power, ILP_load_power, cost, TotalPower] = optimal_DC_Flow_Cascade(nodes, power, link1, link2,reactances, linkNum, Thr)
        #############Remove edges which are overloaded:
        
        loop =1
        print ' Length Flows:'
        print len(flows)
        print 'Length link1:'
        print len(link1)
        print 'FLOOOOOOOOOOOOOOOOOOOOOOOOWS:'
        print flows
        times = 1
        while (loop ==1):
            f =0
            while (f < len(flows)) and (f < len(Original_flows)):
                #print 'Flooooooooooooooooooooooooooows:'
                #print flows
                #for f in range(0, len(flows)):
                if (abs(flows[f]- Original_flows[f]) >= 0.2) and (times < i) and (i>20):# or (flows[f] != -0.31):
                    if (abs(flows[f]) > 0.7) and (abs(flows[f]) < 0.9):
                        print 'HHHHHHHHHHHHHHHHHHHHHHHH:'
                        print flows[f]
                        loop = 2
                        #print 'f:'
                        #print f
                        #print link1
                        print 'link1'
                        print link1[f]
                        print 'link2'
                        print link2[f]
                        e1 = link1[f]
                        e2 = link2[f]
                        edge = (e1, e2)
                        del link1[f]
                        del link2[f]
                        del linkNum[f]
                        del flows[f]
                        del Original_flows[f]
                        del reactances[f]
                        times = times +1
                f = f +1
                    #del reactances[f]
            print 'REPEAAAAAAAAAAAAAAAAAAAAAAATTT'
            Original_flows = flows
            [flows, ILP_gen_power, ILP_load_power, cost, TotalPower] = optimal_DC_Flow_Cascade(nodes, power, link1, link2, reactances, linkNum, Thr)
            #Original_flows = flows
            if (loop ==2):
                loop =1
            else:
                loop = 0
        
        #############Remove Edges which are overloaded
        All_Costs.append(cost)
        thispower = 0
        #for i in range(0, len(ILP_load_power)):
        #    thispower = thispower + ILP_load_power[i]
        print 'TotalPower'
        print TotalPower
        All_power.append(TotalPower)
        #print 'Removed Index:'
        #print i
        print 'SSSSSSSSSSSSSSSSSSSSIIIIIIIIIIIIIIIIZEEEEEEEEE:'
        print len(link1)
        print 'Link1:'
        print link1
        print 'Link2:'
        print link2
        print 'Flows:'
        print flows
        print 'ILP Gen power:'
        print ILP_gen_power
        print 'ILP load power:'
        print ILP_load_power
    print '################################# Finished Power Flow Optimization algorithm ###########################################'
    print 'All Costs:'
    print All_Costs
    print 'All_power:'
    print All_power
    Costs.append(All_Costs)
    Power.append(All_power)
    All_Costs =[]
    All_power = []
    #link1 = []
    #link2 = []
    #reactances = []
    #linkNum = []
    link1 = deepcopy(Original_link1)
    link2 = deepcopy(Original_link2)
    linkNum = deepcopy(Original_linkNum)
    reactances = deepcopy(Original_reactances)
    link1 = deepcopy(Original_link1)
    link2 = deepcopy(Original_link2)
    linkNum = deepcopy(Original_linkNum)
    reactances = deepcopy(Original_reactances)

print 'Costs:'
print Costs
print 'Power:'
print Power
#################################################
Disruption_Cost = []#np.zeros(shape=(1,N))
for i in range(0, N):
    Disruption_Cost.append(0)
print 'Disruption Cost'
print Disruption_Cost
for i in range(0, N):
    for c in Costs:
        Disruption_Cost[i] = Disruption_Cost[i] + c[i]
for i in range(0, N):
    Disruption_Cost[i] = Disruption_Cost[i] / repeat
##################################################
Load_P = []
for i in range(0, N):
    Load_P.append(0)
print 'Load Power:'
print Load_P
for i in range(0, N):
    for p in Power:
        print 'Load_P[i]:'
        print Load_P[i]
        print p[i]
        Load_P[i] = Load_P[i] + p[i]
for i in range(0, N):
    Load_P[i] = Load_P[i] /repeat
#################################################
print 'Disruption Cost:'
print Disruption_Cost
print 'Load Power:'
print Load_P
f = open("Result_Costs_Cascade10.txt", "w")
for i in range(0, len(Disruption_Cost)):
    f.write(str(Disruption_Cost[i])+ "\n" )
f.close()
f = open("Result_Power_Cascade10.txt", "w")
for i in range(0, len(Load_P)):
    f.write(str(Load_P[i])+ "\n" )
f.close()
#R= np.zeros(shape=(len(green_edges),H2.number_of_edges()))    
###################################################################################
#################Started Max-Rank Alg 1: This algorithm gauranteed (1-1/e)/2 approximation######################################
#Power_2 = Greedy_Max_Rank_Alg1(Cost_routing, R, ProbeCost, green_edges)
#MaxRank_Identi_link, MaxRank,MaxRankMonitors, RMaxRank, CostMaxRank = Greedy_Max_Rank_Alg2(Cost_routing, R, ProbeCost, green_edges)
#####################NO CASCADE PREVENTION SCENARIO:###########################################################################
####What happens if we dont stop the cascade and let it propagate? How much power do we lose? How much load is not satisfied?
print '#######################NO CASCADE PREVENTION:#########################################'



