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
#from my_lib_DC_Flow_Cascade import *
from my_lib_Find_Flows import *
from my_lib_Power_Control import *
#from my_lib import *
#https://www.diffchecker.com/efddo0xv
work_dir=os.getcwd()

#path_to_dot_dir='../../../image_graph_dot/DotFile/'
#path_to_image_dir='../../../image_graph_dot/immagini_generate/'
#path_to_image_store='../../../image_graph_dot/store_images/'
#path_to_stats='../../../image_graph_dot/stats/statistiche/'
#path_to_file_simulation='../../../image_graph_dot/current_simulation.txt'
#path_to_stat_prog='../../../image_graph_dot/stats/progress_iteration/'
#path_to_stat_times='../../../image_graph_dot/stats/times/'
#print "Number of runs: "+sys.argv[5]+ "/"+sys.argv[4]
#print "Simulation Parameters: "
#print "Seed: "+sys.argv[1]
#print "Alpha demand: "+sys.argv[2]
#print "Prob edge green: "+sys.argv[3]
#print "Distance metric: "+sys.argv[6]
#print "Type of betweeness: "+sys.argv[7]

#seed_passed=sys.argv[1]
#alpha_passed=sys.argv[2]
#prob_edge_passed=sys.argv[3]
#distance_metric_passed=sys.argv[6]
#type_of_bet_passed=sys.argv[7]
#flow_c_fixed=sys.argv[8]
#flow_c_value=int(sys.argv[9])
#number_of_couple=int(sys.argv[10])
#Percentage = float(sys.argv[18])
#Monitors = int(sys.argv[17])
#fixed_distruption=str(sys.argv[11])
#var_distruption=float(sys.argv[12])
#K_HOPS=int(sys.argv[14])
#always_split=int(sys.argv[15])
#random_disruption=int(sys.argv[16])
#disruption_value=int(sys.argv[17])
#error=float(sys.argv[18])
#Gap=float(sys.argv[19])
#ProbeCost = int(sys.argv[19])
Thr = float(sys.argv[1])
Dest_perc = float(sys.argv[2])
N = int(sys.argv[3])
repeat = int(sys.argv[4])
print 'Threshold:'
print Thr
print 'Dest perc:'
print Dest_perc
print 'N:'
print N
print 'repeat:'
print repeat
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
for e in hviet.edges():
    print 'HVIET Edges:'
    print e
################################################################################################################################
nodes = []
power = []
linkNum = []
link1 = []
link2 = []
power, nodes, linkNum, link1, link2, reactances = read_hviet()
################################################################################################################################
# Percentage of monitors destroyed: 
##Dest_perc = 0.0
# Non controllable nodes in the hviet
non_cont_h_nodes = []
# Non controllable edges in hviet
non_cont_h_edges = []
# Destroyed nodes in garr:
des_garr_nodes = []
# Destroyed edges in garr:
des_garr_edges = []
Curr_Gray_Edges = []
Curr_Gray_Nodes = []
[non_cont_h_nodes, non_cont_h_edges, des_garr_nodes, des_garr_edges] = Destroy_Monitors(hviet, garr, h_inter, g_inter, Dest_perc)
NumberofCycles = 0
[NumberofCycles, Curr_Gray_Edges, Curr_Gray_Nodes] = Count_Cycles(non_cont_h_nodes, non_cont_h_edges, hviet)
print 'Number of Cycles :::::::::::::::::::::'
print NumberofCycles
################################################################################################################################
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
cost_no_mon = []
TotalPower = []
#Thr= 0.5
Original_flows = []
print '################################# Start Solving the Power Flow Model ###################################################'
#[Original_flows, ILP_gen_power, ILP_load_power, cost, TotalPower] = optimal_DC_Flow_Cascade(nodes, power, link1, link2, reactances, linkNum, Thr)
#print 'Flows:'
#print flows
#print 'ILP_gen_power:'
#print ILP_gen_power
#print 'ILP_load_power:'
#print ILP_load_power
#All_Costs.append(cost)
#All_power.append(TotalPower)
########################################Start the attack model:#################################################################
removed_edges = []
flows = []
flows_no_mon = []
Costs = []
Power = []
TotalPower = []
TotalGenPower = []
TotalPower_no_mon = []
TotalGenPower_no_mon = []
link1_no_mon = []#deepcopy(link1)
link2_no_mon = []#deepcopy(link2)
reactances_no_mon = []#deepcopy(reactances)
for e in link1:
    link1_no_mon.append(e)
for e in link2:
    link2_no_mon.append(e)
for e in reactances:
    reactances_no_mon.append(e)
graph_built = nx.MultiGraph(hviet)
#graph_built = Create_Weighted(hviet, link1, link2, reactances)
#ILP_gen_power = []
#ILP_load_power = []
##N= 360 #360
##repeat = 2 #10
Original_link1 = deepcopy(link1) #[]
Original_link2 = deepcopy(link2) #[]
Original_linkNum = deepcopy(linkNum) #[]
Original_reactances = deepcopy(reactances)#[]
##Thr = 0.8
destroyed_edges = []
unknown_graph = nx.MultiGraph()
for j in range(0, repeat):
    for i in range(0, N):
        ILP_gen_power = []
        ILP_load_power = []
        ILP_gen_power_no_mon = []
        ILP_load_power_no_mon = []
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
            e1 = link1[rem]
            e2 = link2[rem]
            e = (e1, e2)
            print 'Removed Edges:'
            print e
        
            if e not in destroyed_edges:
                destroyed_edges.append(e)
            del link1[rem]
            del link2[rem]
            del linkNum[rem]
            del reactances[rem]
            if (rem < len(link1_no_mon)):
                del link1_no_mon[rem]
                del link2_no_mon[rem]
                del reactances_no_mon[rem]
        if rem not in removed_edges:
            removed_edges.append(rem)
        
        #########################################################################################################################################
        Hviet_Destroyed = nx.MultiGraph()
        Hviet_Destroyed= get_graph_from_destroyed_graph(hviet, destroyed_edges) #(graph_built, destroyed_edges)
        destroyed_edges_no_mon = []
        for e in destroyed_edges:
            if e not in destroyed_edges_no_mon:
                destroyed_edges_no_mon.append(e)
        for e in Curr_Gray_Edges:
            if e not in destroyed_edges_no_mon:
                destroyed_edges_no_mon.append(e) 
        for e in Curr_Gray_Edges:
            e1 = e[0]
            e2= e[1]
            for i in range(0, len(link1_no_mon)):
                if ((link1_no_mon[i] == e1) and (link2_no_mon[i] == e2)):
                    del link1_no_mon[i]
                    del link2_no_mon[i]
                    del reactances_no_mon[i]
                if ((link1_no_mon[i] == e2) and (link2_no_mon[i] == e1)):
                    del link1_no_mon[i]
                    del link2_no_mon[i]
                    del reactances_no_mon[i]
        Hviet_Destroyed_no_mon = nx.MultiGraph()
        Hviet_Destroyed_no_mon = get_graph_from_destroyed_graph(hviet, destroyed_edges_no_mon)
        print 'Hviet Destroyed Nodes:'
        print len(Hviet_Destroyed.nodes())
        print 'Hviet Number of edges:'
        print len(Hviet_Destroyed.edges())
        #link1
        #graph_destroyed = nx.Graph()
        #graph_destroyed = Create_Weighted(Hviet_Destroyed, link1, link2, reactances) 
        #########################################################################################################################################
        #Here try to solve DC power flow equations for each connected component of the graph
        graphs = list(nx.connected_component_subgraphs(Hviet_Destroyed))
        print 'Connected Components of the Destroyed Graph:'
        print graphs
        """
        [flows_no_mon, ILP_gen_power_no_mon, ILP_load_power_no_mon, cost_no_mon, TotalPower_no_mon] = optimal_Power_Control(hviet, hviet, nodes, power, link1_no_mon, link2_no_mon, reactances_no_mon, linkNum, Thr) #optimal_DC_Flow_Cascade
        
        for i in range(0, len(power)):
            if (i < 113) and (i not in Curr_Gray_Nodes):
                #print 'i:'
                #print i
                #print 'Gray Nodes:'
                #print Curr_Gray_Nodes
                power[i] = ILP_gen_power_no_mon[i]
            if (113 <= i < 210) and (i not in Curr_Gray_Nodes):
                power[i] = ILP_load_power_no_mon[i-113]
        """
        for g in graphs:
            #Function to find the optimal flow
            print 'Number of Edges of Subgraph g:'
            print len(g.edges())
            print 'Number of Nodes in Subgraph g:'
            print len(g.nodes())
            #print 'Weight of subgraph g:'
            graph_des = nx.MultiGraph()
            graph_des = Create_Weighted(g, link1, link2, reactances)
            #for e in graph_des.edges(): #g.edges():#raph_des.edges():
            #    e1 = e[0]
            #    e2 = e[1]
            #    w = graph_des[e1][e2]['weight'] #graph_des[e1][e2]['weight']
            #    print w
            if (len(graph_des.edges()) > 10):
                [flows, ILP_gen_power, ILP_load_power, cost, TotalPower, TotalGenPower]= optimal_Find_Flow(hviet, graph_des, nodes, power, link1, link2, reactances, linkNum, Thr)            
        #[flows_no_mon, ILP_gen_power_no_mon, ILP_load_power_no_mon, cost_no_mon, TotalPower_no_mon] = optimal_DC_Flow_Cascade(nodes, power, link1_no_mon, link2_no_mon, reactances_no_mon, linkNum, Thr)
        #########################################################################################################################################
        #if i <20:
        #    [flows, ILP_gen_power, ILP_load_power, cost, TotalPower] = optimal_DC_Flow_Cascade(nodes, power, link1, link2,reactances, linkNum, 0.5)
        #else:
        #    [flows, ILP_gen_power, ILP_load_power, cost, TotalPower] = optimal_DC_Flow_Cascade(nodes, power, link1, link2,reactances, linkNum, Thr)
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
                if (abs(flows[f]) >= Thr):# and (times < i):# and (i>20):# or (flows[f] != -0.31):
                    #if (abs(flows[f]) > 0.5) and (abs(flows[f]) < 0.7):
                    print 'DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDHHHHHHHHHHHHHHHHHHHHHHHH:'
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
                    if e not in destroyed_edges:
                        destroyed_edges.append(edge)
                    #########################################################################################################################################
                    Hviet_Destroyed = nx.MultiGraph()
                    Hviet_Destroyed= get_graph_from_destroyed_graph(hviet, destroyed_edges) #(graph_built, destroyed_edges
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
            graphs = list(nx.connected_component_subgraphs(Hviet_Destroyed))
            print 'Connected Components of the Destroyed Graph:'
            print graphs
            TotalPowerAllGraphs= []
            TotalPowerAllGraphs = 0
            TotalGenPowerAllGraphs = []
            TotalGenPowerAllGraphs = 0
            for g in graphs:
                #Function to find the optimal flow
                print 'Number of Edges of Subgraph g:'
                print len(g.edges())
                print 'Number of Nodes in Subgraph g:'
                print len(g.nodes())
                #print 'Weight of subgraph g:'
                graph_des = nx.Graph()
                graph_des = Create_Weighted(g, link1, link2, reactances)
                #for e in g.edges():#raph_des.edges():
                #    e1 = e[0]
                #    e2 = e[1]
                #    w = g[e1][e2]['weight'] #graph_des[e1][e2]['weight']
                #    print w
                if (len(graph_des.nodes()) > 10):
                    [flows, ILP_gen_power, ILP_load_power, cost, TotalPower, TotalGenPower]= optimal_Find_Flow(hviet, graph_des, nodes, power, link1, link2, reactances, linkNum, Thr)
                    TotalPowerAllGraphs = TotalPowerAllGraphs + TotalPower 
                    TotalGenPowerAllGraphs = TotalGenPowerAllGraphs + TotalGenPower
            print 'Total Power of all connected components of the graphs:'
            print TotalPowerAllGraphs
            #########################################################################################################################################
            #Original_flows = flows
            #[flows, ILP_gen_power, ILP_load_power, cost, TotalPower] = optimal_Find_Flow(graph_des, nodes, power, link1, link2, reactances, linkNum, Thr)# optimal_DC_Flow_Cascade()
            #Original_flows = flows
            if (loop ==2):
                loop =1
            else:
                loop = 0
        
        #############Remove Edges which are overloaded
        cost = 100*abs(abs(TotalPowerAllGraphs)- 31.817217299999992559378) #- (TotalGenPowerAllGraphs)
        All_Costs.append(cost)
        thispower = 0
        #for i in range(0, len(ILP_load_power)):
        #    thispower = thispower + ILP_load_power[i]
        print 'TotalPower'
        print TotalPower
        #if (TotalPowerAllGraphs < 0):
        All_power.append(TotalPowerAllGraphs)#TotalPower)
        #else:
        #    All_power.append(0)
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
    link1 = []
    link2 = []
    reactances = []
    linkNum = []
    #link1 = deepcopy(Original_link1)
    #link2 = deepcopy(Original_link2)
    #linkNum = deepcopy(Original_linkNum)
    #reactances = deepcopy(Original_reactances)
    #link1 = deepcopy(Original_link1)
    #link2 = deepcopy(Original_link2)
    #linkNum = deepcopy(Original_linkNum)
    #reactances = deepcopy(Original_reactances)
    power, nodes, linkNum, link1, link2, reactances = read_hviet()
    link1_no_mon = []#deepcopy(link1)
    link2_no_mon = []#deepcopy(link2)
    reactances_no_mon = []#deepcopy(reactances)
    for e in link1:
        link1_no_mon.append(e)
    for e in link2:
        link2_no_mon.append(e)
    for e in reactances:
        reactances_no_mon.append(e)


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
        #print 'Load_P[i]:'
        #print Load_P[i]
        #print p[i]
        Load_P[i] = Load_P[i] + p[i]
for i in range(0, N):
    Load_P[i] = Load_P[i] /repeat
#################################################
print 'Disruption Cost:'
print Disruption_Cost
print 'Load Power:'
print Load_P
f = open("Result_Costs_No_control_Cascade_"+str(Thr)+"_Thr_"+str(Dest_perc)+"_DesMon_"+str(N)+"_N_"+str(repeat)+"_repeat_"+".txt", "w")
for i in range(0, len(Disruption_Cost)):
    f.write(str(Disruption_Cost[i])+ "\n" )
f.close()
f = open("Result_Power_No_Control_Cascade_"+str(Thr)+"_Thr_"+str(Dest_perc)+"_DesMon_"+str(N)+"_N_"+str(repeat)+"_repeat_"+".txt", "w")
#f = open("Result_Power_Cascade_08Thr_0mon.txt", "w")
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
print 'Total_Cost:'
print Costs
print 'Total_power:'
print Power
