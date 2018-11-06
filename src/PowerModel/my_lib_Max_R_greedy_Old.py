__author__ = 'Diman'

from gurobipy import *
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
from numpy.linalg import matrix_rank
from my_lib_DC_Flow import *
from copy import deepcopy
############################
# Model data
def optimal_Max_R(nodes, power, link1, link2, reactances, linkNum, Resources, Stage_Resource, Thr, removed_edges, removed_power, removed_index, Original_link1, Original_link2, Original_reactances):
    flows = []
    cost = []
    Total_power = []
    ILP_gen_power = []
    ILP_load_power = []
    TotalPower = 0
    diff =0
    Added_Flows = []
    repairs = []
    Flow_inTime = []
    times = []
    Original_Flow = []
    New_Flow = []
    #########################GREEEDY BASED APPROACH###############################
    [flows, ILP_gen_power, ILP_load_power, cost, TotalPower] = optimal_DC_Flow(nodes, power, link1, link2,reactances, linkNum, Thr)
    ##flows, ILP_gen_power, ILP_load_power, cost, TotalPower = Max_R_solution(nodes, power, link1, link2, reactances, linkNum, Thr)
    returned_power = []
    New_link1 = []
    New_link2 = []
    New_reactances = []
    New_link1 = deepcopy(Original_link1)
    New_link2 = deepcopy(Original_link2)
    New_reactances = deepcopy(Original_reactances)
    """
    for i in removed_index:
        #id_source = edge[0]
        #id_target = edge[1]
        #print 'Added Link:'
        #print Original_link1[i]
        #print Original_link2[i]
        #link1.append(Original_link1[i])
        #link2.append(Original_link2[i])
        #reactances.append(Original_reactances[i])
        for m in removed_index:
            if m!=i:
                del New_link1[m]
                del New_link2[m]
                del New_reactances[m]
        [flows, ILP_gen_power, ILP_load_power, cost, ThisTotalPower] = optimal_DC_Flow(nodes, power, New_link1, New_link2, New_reactances, linkNum, Thr)
        diff = float(TotalPower) - float(ThisTotalPower)
        Added_Flows.append(diff)
        Original_Flow.append(TotalPower)
        New_Flow.append(ThisTotalPower)
        diff =0
        New_link1 = []
        New_link2 = []
        New_reactances = []
        New_link1 = deepcopy(Original_link1)
        New_link2 = deepcopy(Original_link2)
        New_reactances = deepcopy(Original_reactances)
        #link1.remove(Original_link1[i])
        #link2.remove(Original_link2[i])
        #reactances.remove(Original_reactances[i])
    print 'Indexes:'
    print removed_index
    print 'Added_Flows:'
    print Added_Flows
    print 'Original Flows:'
    print Original_Flow
    print 'New Flows:'
    print New_Flow
    """
    # 1 repair at a time:
    NumRepairs = 1
    #[Flow_inTime, repairs, time] = Max_R_solution(nodes, power, link1, link2, reactances, linkNum, Thr, removed_edges, removed_power, removed_index, Original_link1, Original_link2, Original_reactances, Added_Flows, NumRepairs)
    [Flow_inTime, repairs, time] = Max_R_solution_greedy(nodes, power, link1, link2, reactances, linkNum, Resources, Stage_Resource, Thr, removed_edges, removed_power, removed_index, Original_link1, Original_link2, Original_reactances, Added_Flows, NumRepairs)
    return Flow_inTime, repairs, time
###
# Solve ILP of max flow problem where the Sets are given and each set can identify a set of links,
# Recover 10 nodes at a time: 100 nodes have been disrupted, in 10 stages all nodes will be recovered: 
def Max_R_solution(nodes, power, link1, link2, reactances, linkNum, Resources, Stage_Resource, Thr, removed_edges, removed_power, removed_index, Original_link1, Original_link2, Original_reactances, Added_Flows, NumRepairs):
    repairs = []
    time = []
    ################################################################################################################
    New_link1 = []
    New_link1 = deepcopy(Original_link1)
    New_link2 = []
    New_link2 = deepcopy(Original_link2)
    New_reactances = []
    New_reactances = deepcopy(Original_reactances)
    flows = []
    Thisflows = []
    ILP_gen_power = []
    ThisILP_gen_power = []
    ILP_load_power = []
    ThisILP_load_power = []
    cost = []
    Thiscost = []
    TotalPower = []
    ThisTotalPower = []
    Flow_inTime = []
    ##############First Look at the flows to see how much flow could be routed in each link if they were all working:
    [flows, ILP_gen_power, ILP_load_power, cost, TotalPower] = optimal_DC_Flow(nodes, power, New_link1, New_link2, New_reactances, linkNum, Thr)
    #Flow_inTime.append(TotalPower)
    [Thisflows, ThisILP_gen_power, ThisILP_load_power, Thiscost, ThisTotalPower] = optimal_DC_Flow(nodes, power, link1, link2, reactances, linkNum, Thr)
    Flow_inTime.append(ThisTotalPower)
    #############################################################################
    Max_flow = 0
    repair_index = []
    time_index = 0
    #New_removed_index = deepcopy(removed_index)
    N = len(removed_index)
    for i in range(0, N):
        for m in removed_index:
            if abs(flows[m]) > Max_flow:
                Max_flow = flows[m]
                repair_index = m
        repairs.append(repair_index)
        time.append(time_index)
        link1 = deepcopy(Original_link1)
        link2 = deepcopy(Original_link2)
        reactances = deepcopy(Original_reactances)
        Max_flow = 0
        This_link1 = deepcopy(Original_link1)
        This_link2 = deepcopy(Original_link2)
        This_reactances = deepcopy(Original_reactances)
        for v in removed_index:
            if v!=repair_index:
                del This_link1[v]
                del This_link2[v]
                del This_reactances[v]
            else:
                removed_index.remove(v)
        print 'REMOVED INDEX:'
        print removed_index
        [Newflows, ILP_gen_power, ILP_load_power, cost, TotalPower] = optimal_DC_Flow(nodes, power, This_link1, This_link2, This_reactances, linkNum, Thr)
        Flow_inTime.append(TotalPower)
        time_index = time_index + 1
    print 'Repairs:'
    print repairs
    print 'time:'
    print time
    print 'Flow during time:'
    print Flow_inTime
    return Flow_inTime, repairs, time #ILP_gen_power, ILP_load_power, cost #ILP_flows#flows    

def Max_R_solution_greedy(nodes, power, link1, link2, reactances, linkNum, Resources, Stage_Resource, Thr, removed_edges, removed_power, removed_index, Original_link1, Original_link2, Original_reactances, Added_Flows, NumRepairs):
    repairs = []
    time = []
    ################################################################################################################
    New_link1 = []
    New_link1 = deepcopy(Original_link1)
    New_link2 = []
    New_link2 = deepcopy(Original_link2)
    New_reactances = []
    New_reactances = deepcopy(Original_reactances)
    flows = []
    Thisflows = []
    ILP_gen_power = []
    ThisILP_gen_power = []
    ILP_load_power = []
    ThisILP_load_power = []
    cost = []
    Thiscost = []
    TotalPower = []
    ThisTotalPower = []
    Flow_inTime = []
    ##############First Look at the flows to see how much flow could be routed in each link if they were all working:
    [flows, ILP_gen_power, ILP_load_power, cost, TotalPower] = optimal_DC_Flow(nodes, power, New_link1, New_link2, New_reactances, linkNum, Thr)
    #Flow_inTime.append(TotalPower)
    [Thisflows, ThisILP_gen_power, ThisILP_load_power, Thiscost, ThisTotalPower] = optimal_DC_Flow(nodes, power, link1, link2, reactances, linkNum, Thr)
    Flow_inTime.append(ThisTotalPower)
    #############################################################################
    repair_index = []
    time_index = 0
    #Added = []
    #New_removed_index = deepcopy(removed_index)
    N = len(removed_index)
    Left_Resources = 0
    for i in range(0, N):
        loop = 0
        Iter = 0
        Left_Resources = Left_Resources + Stage_Resource
        for m in removed_index:
            if (Left_Resources >= Resources[m]):
                loop = 1
        while (loop == 1): 
            Max_flow = 0
            Added_Index = []
            Iter = Iter + 1
            for m in removed_index:
                New_link1 = []
                New_link2 = []
                New_reactances = []
                New_link1 = deepcopy(Original_link1)
                New_link2 = deepcopy(Original_link2)
                New_reactances = deepcopy(Original_reactances)
                for c in removed_index:
                    if m!=c:
                        del New_link1[c]
                        del New_link2[c]
                        del New_reactances[c]
                [Newflows, ILP_gen_power, ILP_load_power, cost, TotalPower] = optimal_DC_Flow(nodes, power, New_link1, New_link2, New_reactances, linkNum, Thr)
                if (abs(TotalPower)>= Max_flow) and (Resources[m] <= Stage_Resource):
                    Max_flow = TotalPower
                    Added_Index = m
            repairs.append(Added_Index)
            Left_Resources = Stage_Resource - Resources[Added_Index]
            loop = 0
            for m in removed_index:
                if (Left_Resources >= Resources[m]):
                    loop = 1
            #if (Iter > 2):
            #    loop = 0
        ##############################
        time.append(time_index)
        Flow_inTime.append(Max_flow)
        removed_index.remove(Added_Index)
        time_index = time_index + 1
    print 'Repairs:'
    print repairs
    print 'time:'
    print 'Flow during time:'
    print Flow_inTime
    return Flow_inTime, repairs, time #ILP_gen_power, ILP_load_power, cost #ILP_flows#flows
    """
    returned_power = []
    New_link1 = []
    New_link2 = []
    New_reactances = []
    New_link1 = deepcopy(Original_link1)
    New_link2 = deepcopy(Original_link2)
    New_reactances = deepcopy(Original_reactances)
    for i in removed_index:
        for m in removed_index:
            if m!=i:
                del New_link1[m]
                del New_link2[m]
                del New_reactances[m]
        [flows, ILP_gen_power, ILP_load_power, cost, ThisTotalPower] = optimal_DC_Flow(nodes, power, New_link1, New_link2, New_reactances, linkNum, Thr)
        diff = float(TotalPower) - float(ThisTotalPower)
        Added_Flows.append(diff)
        Original_Flow.append(TotalPower)
        New_Flow.append(ThisTotalPower)
        diff =0
        New_link1 = []
        New_link2 = []
        New_reactances = []
        New_link1 = deepcopy(Original_link1)
        New_link2 = deepcopy(Original_link2)
        New_reactances = deepcopy(Original_reactances)
    print 'Indexes:'
    print re_greedymoved_index
    print 'Added_Flows:'

    ##Create the Br matrix
    b = np.zeros(shape=(310,310))
    X = np.zeros(shape=(310,310))
    P = np.zeros(shape=(309,1))
    for i in range(1, 310):
        P[i-1, 0] = power[i]
    #TheTeta = np.linalg.solve(a, b)
    for m in range(0, len(link1)):
        i = link1[m]
        j = link2[m]
        if (X[i-1,j-1] != 0):
            X[i-1,j-1] =  float("%0.10f"%(((reactances[m]*X[i-1,j-1])/(X[i-1,j-1] + reactances[m]))))
            X[j-1,i-1] =  float("%0.10f"%(((reactances[m]*X[j-1,i-1])/(X[j-1,i-1] + reactances[m]))))
        else:
            X[i-1,j-1] =  float("%0.10f"%(((reactances[m]))))
            X[j-1,i-1] =  float("%0.10f"%(((reactances[m]))))
    for i in range(0, 310):
        for j in range(0, 310):
            if (i == j):
                for k in range(0,310):
                    if (X[i,k] !=0):
                        b[i,j] =  float("%0.10f"%(((b[i,j] + 1/X[i,k]))))
            else:
                if X[i,j] !=0:
                    b[i,j] =  float("%0.10f"%(((-1/X[i,j]))))
    Br = np.zeros(shape= (309,309))
    for i in range(0,309):
      for j in range(0, 309):
          Br[i,j] = b[i+1,j+1]
    #########################GREEEDY BASED APPROACH###############################
    #Best_greedy=0
    #Best_greedy_monitors=[]
    #Identified_links=[]
    #Edges=[]
    class Node():#(s,d,m):
        def __init__(self, s, d, m, number, node_number):
            edge=(s, d)
            self.e = edge # .append(edge)
            self.m = m
            self.n = number
            self.node_num = node_number
        def AddComb(self, edge):
            edges = []
            for e in self.e:
                if (e != ([], [])):
                    if (e != []):
                        edges.append(e)
            #if edges[0] ==([],[]):
            #    edges.remove(edges[0])
            edges.append(edge)
            self.e = edges
        def RemComb(self, edge):
            edges = []
            for e in self.e:
                edges.append(e)
            if (self.e != ([], [])):
                edges.remove(([], []))
            self.e = edges
    ########################################    
    class Monitors_Perm():
        def __init__(self,edges,m,number):
            self.ident= edges
            self.num=number
            self.monitors= m


    my_objects = []
    Edge_index=0
    Node_index = 0
    for i in range(0, 310):
    #for i in range(0,3):
        my_objects.append(Node([], [],Node_index, Node_index, Node_index ))
        Node_index = Node_index + 1


    for m in range(0, len(link1)):
        for k in range(0, 310):
        #for k in range(0, 3):
            #print 'KKKKKKKKKKKKKK'
            #print k
            if ((k+1)== link1[m]):# or (k == link2[m])):
                edge = (k+1, link2[m])
                my_objects[k].AddComb(edge)
                #Diman Commented:
                ###print 'my_objects[k].e'
                ###print my_objects[k].e
                ###print 'K:'
                ###print k
                #my_objects[k].AddComb(edge)
                ##my_objects[k].e.append(edge)
            if ((k+1)== link2[m]):
                edge = (link1[m], k+1)
                my_objects[k].AddComb(edge)
                #Diman Commented:
                ###print 'my_objects[k].e'
                ###print my_objects[k].e
                ###print 'K 2:'
                ###print k
                #my_objects[k].AddComb(edge)
    my_Model = Model('DCPowerflow')
    P_g_t = {}
    P_l_t = {}
    flows = {}
    P_j_t = {}
    Teta = {}
    ILP_gen_power = []
    ILP_load_power = []
    #for p in range(0,2):
    for p in range(0, 113):
        P_g_t[p] = my_Model.addVar(ub=2, lb=0, vtype=GRB.CONTINUOUS, name='GeneratorPower%s'% (p)) 
    #for e in range(2, 3):
    for e in range(113, 210):
        P_l_t[e] = my_Model.addVar(ub=0, lb=-2, vtype=GRB.CONTINUOUS, name='LoadPower%s'% (e))
    for k in range(210, 310):
    #for k in range(0,0):
        P_j_t[k] = my_Model.addVar(ub=2, lb=-2, vtype=GRB.CONTINUOUS, name='JunctionPower%s'% (k))
    for h in range(0,310):
        Teta[h] = my_Model.addVar(ub=10, lb=-10, vtype=GRB.CONTINUOUS, name='Theta%s'% (h))
    theEdges= []
    for m in range(0, len(link1)):
        i = link1[m]
        j = link2[m]
        edge= (i,j)
        if edge not in theEdges:
            theEdges.append(edge)
            #print 'i,j:'
            #print i,j
            flows[i,j,1] = my_Model.addVar(ub=Max_Thr, lb=Min_Thr, vtype=GRB.CONTINUOUS, name='Flow_%s_%s_%s'% (i,j,1))
            flows[j,i,1] = my_Model.addVar(ub=Max_Thr, lb=Min_Thr, vtype=GRB.CONTINUOUS, name='Flow_%s_%s_%s'% (j,i,1)) 
        else:#if edge in theEdges:
            flows[i,j,2] = my_Model.addVar(ub=Max_Thr, lb=Min_Thr, vtype=GRB.CONTINUOUS, name='Flow_%s_%s_%s'% (i,j,2))
            flows[j,i,2] = my_Model.addVar(ub=Max_Thr, lb=Min_Thr, vtype=GRB.CONTINUOUS, name='Flow_%s_%s_%s'% (j,i,2))
        #print 'theEdges'
        #print theEdges
    my_Model.update()
    for i in range(0, 113):
    #for i in range(0,2):
        my_Model.addConstr(0.0 <= P_g_t[i], 'Non_Negative_Power_%s'% (i) ) #power[i] - 0.0001
        #my_Model.update()
    for j in range(0, 113):
    #for j in range(0,2):
        my_Model.addConstr(P_g_t[j] <= P_g_max, 'Max_Gen_Power_%s'% (j))
        #my_Model.update()
    #Load constraints
    for i in range(113, 210):
    #for i in range(2, 3):
        my_Model.addConstr(power[i] <= P_l_t[i] , 'Non_Negative_Power_%s'% (i))
        #my_Model.update()
    for j in range(113, 210):
    #for j in range(2, 3):
        my_Model.addConstr(P_l_t[j] <= 0.0 , 'Max_Load_Power_%s'% (j))
    #Diman commented two lines
    #for k in range(210, 310):
    #    my_Model.addConstr(P_j_t[k] == power[k], 'Junction_Power_%s'% (k))
    my_Model.update()
    my_Model.addConstr(Teta[0] == 0.0, 'ReferenceVoltage')
    for k in range(1, 113):
        my_Model.addConstr(P_g_t[k] == sum(Br[k-1, j-1]*Teta[j] for j in range(1, 310)), 'GenFlow_%s'% (k))
    my_Model.update()
    for k in range(113, 210):
        my_Model.addConstr(P_l_t[k] == sum(Br[k-1, j-1]*Teta[j] for j in range(1, 310)), 'LoadFlow_%s'% (k))
    my_Model.update()
    for k in range(210, 310):
        my_Model.addConstr(P_j_t[k] == sum(Br[k-1, j-1]*Teta[j] for j in range(1,310)), 'JunctionFlow_%s'% (k))
    my_Model.update()
    #Load line capacities:
    theEdges= []
    for m in range(0, len(link1)):
        #for j in range(0, 210):
        i= link1[m]
        j = link2[m]
        edge = (i,j)
        if edge not in theEdges:
            theEdges.append(edge)
            my_Model.addConstr(Min_Thr <= flows[i,j,1], 'Min_Flow_Thr1_%s'% (m))
            #my_Model.update()
            my_Model.addConstr(flows[i,j,1] <= Max_Thr, 'Max_Flow_Thr1_%s'% (m))
            #my_Model.update()
            my_Model.addConstr(flows[j,i,1] <= Max_Thr, 'Max_Flow_Thr2_%s'% (m))
            #my_Model.update()
            my_Model.addConstr(Min_Thr <= flows[j,i,1], 'Min_Flow_Thr2_%s'% (m))
            #my_Model.update()
            my_Model.addConstr(flows[i,j,1] + flows[j,i,1] == 0, 'Flows_dir_%s'% (m))
            #Reactance:
            my_Model.addConstr(flows[i,j,1]*reactances[m] == Teta[i-1] - Teta[j-1], 'FlowsCons_%s'% (m))
            my_Model.addConstr(flows[j,i,1]*reactances[m] == Teta[j-1] - Teta[i-1], 'FlowsRCons_%s'% (m))
            #my_Model.update()
        else:#if edge in theEdges:
            #my_Model.rem
            my_Model.addConstr(Min_Thr <= flows[i,j,2], 'Min_Flow_Thr1_%s'% (m))
            #my_Model.update()
            my_Model.addConstr(flows[i,j,2] <= Max_Thr, 'Max_Flow_Thr1_%s'% (m))
            #my_Model.update()
            my_Model.addConstr(flows[j,i,2] <= Max_Thr, 'Max_Flow_Thr2_%s'% (m))
            #my_Model.update()
            my_Model.addConstr(Min_Thr <= flows[j,i,2], 'Min_Flow_Thr2_%s'% (m))
            #my_Model.update()
            my_Model.addConstr(flows[i,j,2] + flows[j,i,2] == 0, 'Flows_dir_%s'% (m))
            my_Model.addConstr(flows[i,j,2]*reactances[m] == Teta[i-1] - Teta[j-1], 'FlowCons2_%s'% (m))
            my_Model.addConstr(flows[j,i,2]*reactances[m] == Teta[j-1] - Teta[i-1], 'FlowsRCons_%s'% (m))
            #my_Model.update()
            
    ###Flow Conservation:
    my_Model.addConstr((quicksum(P_g_t[l] for l in range(0,113)) + quicksum(P_l_t[j] for j in range(113, 210))) >= -0.1, 'ConsumedGeneratedPower')
    my_Model.addConstr((quicksum(P_g_t[l] for l in range(0,113)) + quicksum(P_l_t[j] for j in range(113, 210))) <= 0.1, 'ConsumedGeneratedPower')
    ##my_Model.addConstr((quicksum(P_g_t[l] for l in range(0,2)) + quicksum(P_l_t[j] for j in range(2, 3))) == 0, 'ConsumedGeneratedPower')

    my_Model.update()
    #Flow Conservation constraint:
    #theEdges = []
    for k in range(0, 113):
    #for k in range(0,2):
        edges =[]
        theEdges =[]
        if (my_objects[k].e != ([], [])):
            #Diman Commented:
            ###print 'my_objects[k].e'
            ###print my_objects[k].e
            for (i,j) in my_objects[k].e:
                if (i == k+1):
                    e = (i,j)
                    if e not in edges:
                        theEdges.append((i,j,1))
                        edges.append(e)
                    else: #if e in edges:
                        edges.append(e)
                        theEdges.append((i,j,2))
                if (j == k+1):
                    e = (j,i)
                    if e not in edges:
                      edges.append(e)
                      theEdges.append((j,i,1))
                    else: #if e in edges:
                      edges.append(e)
                      theEdges.append((j,i,2))
            #Diman Commented:
            print 'INJAAAAAAAAAAA:'
            print theEdges
            #for (e,f,g) in theEdges:
            #    print e,f,g
            #my_Model.addConstr(sum(flows[k,f,g] for (k,f,g) in theEdges) == P_g_t[k], 'Gen_FlowConservation_%s'% (k))
            if (theEdges !=[]):
                my_Model.addConstr(sum(flows[k,f,g] for (k,f,g) in theEdges) == P_g_t[k], 'Gen_FlowConservation_%s'% (k))
                my_Model.update()
            else: #elif(theEdgs ==[]):
                print 'ZERRROOOOOOOOOOOOOOO'
                print theEdges
                my_Model.addConstr(P_g_t[k] == 0, 'Gen_FlowConservation_%s'% (k))
                my_Model.update()
        else:
            my_Model.addConstr(P_g_t[k] == 0, 'Gen_FlowConservation_%s'% (k)) 
    #Load flow conservation:
    for k in range(113, 210):
    #for k in range(2,3):
        edges =[]
        theEdges =[]
        if (my_objects[k].e != ([], [])):
            #Diman Commented:
            ###print 'my_objects[k].e'
            ###print my_objects[k].e
            for (i,j) in my_objects[k].e:
                if (i == k+1):
                    e = (i,j)
                    if e not in edges:
                        theEdges.append((i,j,1))
                        edges.append(e)
                    else: #if e in edges:
                        edges.append(e)
                        theEdges.append((i,j,2))
                if (j == k+1):
                    e = (j,i)
                    if e not in edges:
                      edges.append(e)
                      theEdges.append((j,i,1))
                    else: # e in edges:
                      edges.append(e)
                      theEdges.append((j,i,2))
            #Diman Commented:
            print 'Power INJAAAAAAAAAAAA:'
            print theEdges
            #my_Model.addConstr(quicksum(flows[e,f,g] for (e,f,g) in theEdges) == power[k] , 'Load_FlowConservation_%s'% (k) )
            if (theEdges !=[]):
                print 'INJAAAAAAAAAAAAAAAAAAAAAAAAAAAA:'
                print theEdges
                my_Model.addConstr(sum(flows[k,f,g] for (k,f,g) in theEdges) == P_l_t[k] , 'Load_FlowConservation_%s'% (k))
                #my_Model.addConstrs((flows.sum(e,f,g)  == P_l_t[k] for (e,f,g) in theEdges for k in range(113,210)), "node")
                my_Model.update()
            else: #elif(theEdges == []):
                print 'Zeroooooooooooooooo'
                print theEdges
                my_Model.addConstr( P_l_t[k] == 0 , 'Load_FlowConservation_%s'% (k))
                my_Model.update()
        else:
            my_Model.addConstr( P_l_t[k] == 0 , 'Load_FlowConservation_%s'% (k))

    my_Model.update()
    #my_Model.optimize()

    my_Model.setObjective(w_g*(sum((P_g_t[l] - power[l] ) for l in range(0,113)))+w_l*(sum((P_l_t[l] - power[l]) for l in range(113,210))), GRB.MINIMIZE)
    ##my_Model.setObjective(w_g*(quicksum((P_g_t[l]-power[l] ) for l in range(0,2)))+w_l*(quicksum((P_l_t[l] - power[l]) for l in range(2,3))), GRB.MINIMIZE)

    my_Model.update()
    my_Model.optimize()
    ###################################################################
    if my_Model.status == GRB.status.OPTIMAL:
        ILP_flows=[]
        ILP_gen_power=[]
        for p in range(0, 113):
        #for p in range(0,2):
            var_reference = my_Model.getVarByName('GeneratorPower%s'% (p)) # ('GeneratorPower%s'%(i)) #Generator's power
            #Diman Commented
            ###print 'var_reference'
            ###print var_reference.x
            ILP_gen_power.append(var_reference.x)
            #if var_reference.x>0:
        ILP_load_power=[]
        for e in range(113, 210):
        #for e in range(2,3):
            var_reference = my_Model.getVarByName('LoadPower%s'% (e)) #('LoadPower%s'% (e)) #Load's Power
            #Diman Commented:
            ###print 'var_reference_power:'
            ###print var_reference.x
            ILP_load_power.append(var_reference.x)
            if var_reference.x>0:
                #Diman Commented:
                ###print var_reference.x
                ILP_load_power.append(e)
                #Diman Commented:
                ###print 'Load Power:'
                ###print ILP_load_power

    #Find the flows:
        theEdges =[]
        #Add the generator's power to the results:
        ILP_gen = []
        gen_sol = my_Model.getAttr('x', P_g_t)
        for h in range(0, 113):
        #for h in range(0,2):
            ILP_gen.append(gen_sol[h])
        #Add the load's power to the results:
        ILP_load = []
        load_sol = my_Model.getAttr('x', P_l_t)
        for h in range(113, 210):
        #for h in range(2, 3):
            ILP_load.append(load_sol[h])
        #Add the flows of the lines to the results:
        solution = my_Model.getAttr('x', flows)
        theEdges = []
        for h in range(0, len(link1)):
            i = link1[h]
            j = link2[h]
            e = (i,j)
            if e not in theEdges:
                theEdges.append(e)
                f = 1
            else:
                f =2
            my_flows.append(solution[i,j,f])
        cost =[]
        cost = my_Model.objVal
        print 'Solution:'
        print('The optimal objective is %g' % my_Model.objVal)
        #Add The angle's solution:
        Theta_sol = []
        teta_sol = my_Model.getAttr('x', Teta)
        for k in range(0, 310):
            Theta_sol.append(teta_sol[k])
        print 'Theta:'
        print Theta_sol
    #Find the flows:
    ###Find the total power delivered:
    TotalPower = []
    TotalPower = 0
    for i in range(0, len(ILP_load)):
      TotalPower = TotalPower + ILP_load[i]
    print 'Total Power HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH:'
    print TotalPower
    
    return repairs, time #ILP_gen_power, ILP_load_power, cost #ILP_flows#flows
    """
