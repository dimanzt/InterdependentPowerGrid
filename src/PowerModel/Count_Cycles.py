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
from my_lib_Power_Control_discrete import *
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
seed_passed=sys.argv[5]
#############################
seed_random=int(seed_passed)
random.seed(seed_random)
##############################
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
if (len(link1) > 10):
    for i in range(210, 310):
        power[i] = 0
Original_power = []
for i in range(0, len(power)):
    Original_power.append(power[i])
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
lengthCurr_Gray_Edges = []
NumCycles = []
lengthCurr_Gray_Nodes = []
for i in range(0, N):
    [non_cont_h_nodes, non_cont_h_edges, des_garr_nodes, des_garr_edges] = Destroy_Monitors(hviet, garr, h_inter, g_inter, Dest_perc)
    NumberofCycles = 0
    [NumberofCycles, Curr_Gray_Edges, Curr_Gray_Nodes] = Count_Cycles(non_cont_h_nodes, non_cont_h_edges, hviet)
    print 'Number of Cycles :::::::::::::::::::::'
    print NumberofCycles
    Original_Gray_Edges = []
    for i in non_cont_h_edges:
        Original_Gray_Edges.append(i)
    lengthCurr_Gray_Edges.append(len(non_cont_h_edges))
    NumCycles.append(NumberofCycles)
    lengthCurr_Gray_Nodes.append(len(non_cont_h_nodes))
################################################################################################################################
###################################################################################
#################Started Max-Rank Alg 1: This algorithm gauranteed (1-1/e)/2 approximation######################################
#Power_2 = Greedy_Max_Rank_Alg1(Cost_routing, R, ProbeCost, green_edges)
#MaxRank_Identi_link, MaxRank,MaxRankMonitors, RMaxRank, CostMaxRank = Greedy_Max_Rank_Alg2(Cost_routing, R, ProbeCost, green_edges)
#####################NO CASCADE PREVENTION SCENARIO:###########################################################################
####What happens if we dont stop the cascade and let it propagate? How much power do we lose? How much load is not satisfied?
print '#######################NO CASCADE PREVENTION:#########################################'
print 'Number Curr_Gray_Edges:'
print lengthCurr_Gray_Edges#len(Curr_Gray_Edges)
AvgGrayEdges = 0
for i in lengthCurr_Gray_Edges:
    AvgGrayEdges = AvgGrayEdges + i
print float(float(AvgGrayEdges) / 100)
print 'Number Curr Gray Nodes:'
print lengthCurr_Gray_Nodes#len(Curr_Gray_Nodes)
AvgGrayNodes = 0
for i in lengthCurr_Gray_Nodes:
    AvgGrayNodes = AvgGrayNodes + i
print float(float(AvgGrayNodes) /100)
print 'Cycles:'
print NumCycles
AvgCycles = 0
for i in NumCycles:
    AvgCycles = AvgCycles + i
print float(float(AvgCycles)/ 100)

print 'Garr Nodes:'
print len(garr.nodes())
print 'Garr Edges:'
print len(garr.edges())
print 'Hviet Nodes:'
print len(hviet.nodes())
print 'Hviet Edges:'
print len(hviet.edges())
