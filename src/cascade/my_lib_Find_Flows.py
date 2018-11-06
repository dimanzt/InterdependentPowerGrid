__author__ = 'Diman'

from gurobipy import *
import numpy as np
from my_lib_power import *
from my_lib_cascade import *
from my_lib_DC_Flow import *
#######Rank:
#from my_lib_Max_rank import *
from numpy.linalg import matrix_rank

# Model data
def optimal_Find_Flow(H_Working, H, nodes, power, link1, link2, reactances, linkNum, Thr):
    flows = []
    cost = []
    Total_power = []
    ILP_gen_power = []
    ILP_load_power = []
    #########################GREEEDY BASED APPROACH###############################
    flow_edges, flows, ILP_gen_power, ILP_load_power, cost, TotalPower, TotalGenPower = Find_Flow_solution(H_Working, H, nodes, power, link1, link2, reactances, linkNum, Thr)

    return flow_edges, flows, ILP_gen_power, ILP_load_power, cost, TotalPower, TotalGenPower
###
# Solve ILP of max flow problem where the Sets are given and each set can identify a set of links,

def Find_Flow_solution(H_Working, H, nodes, power, link1, link2, reactances, linkNum, Thr):
    #Power_gen_t = []
    #Power_load_t = []
    my_flows = []
    ILP_gen = []
    ILP_load = []
    ILP_jun = []
    cost = []
    w_g = 1
    w_l = 100
    Max_Thr = Thr#0.3#1.5
    Min_Thr = (-1)*Thr#-0.3#1.5
    P_g_max = 2
    P_g_min = -2
    P_l_max = -2
    P_l_min = 2
    #############################################################################
    ##Create the Br matrix
    NumberofEdges = len(H.edges())
    NumberofNodes = len(H.nodes())
    TotalPower = []
    TotalPower = 0
    TotalGenPower = []
    TotalGenPower = 0
    print 'Number of Edges'
    print NumberofEdges
    print 'Length of power'
    print len(power)
    Load = []
    Generator = []
    Junction = []
    b = np.zeros(shape=(NumberofNodes,NumberofNodes))
    X = np.zeros(shape=(NumberofNodes,NumberofNodes))
    P = np.zeros(shape=(NumberofNodes-1,1))
    for n in H.nodes():
        j = H.nodes().index(n)
        i = H_Working.nodes().index(n)
        if (i > 0):
            P[j-1, 0] = power[i]

        if (len(H_Working.nodes()) > 10):
            if (i < 113):
                Generator.append(n)
                ILP_gen.append(power[i])
                #TotalGenPower = TotalGenPower + power[i]
            elif (113 <= i < 310):#210):
                Load.append(n)
                if (power[i] > 0):
                    power[i] = (-1)*power[i]
                ILP_load.append(power[i])
                #TotalPower = TotalPower + power[i]
            elif (i > 311):#(210 <= i < 310):
                ILP_jun.append(power[i])
                Junction.append(n)
        else:
            if (i < 1):
                Generator.append(n)
                ILP_gen.append(power[i])
                #TotalGenPower = TotalGenPower + power[i]
            elif (1 <= i < 3):
                Load.append(n)
                ILP_load.append(power[i])
                #TotalPower = TotalPower + power[i]
            elif (3 <= i < 4):
                ILP_jun.append(power[i])
                Junction.append(n)
    ########################################
    SUM_Load = 0
    for i in range(0, len(ILP_load)):
        SUM_Load = SUM_Load + ILP_load[i]

    SUM_Gen = 0
    for i in range(0, len(ILP_gen)):
        SUM_Gen = SUM_Gen + ILP_gen[i]
    if (abs(SUM_Gen) < abs(SUM_Load)):
        if (SUM_Gen != 0):
            Diff = (abs(SUM_Load) - abs(SUM_Gen)) / abs(SUM_Gen)
        else:
            Diff = 1
        for k in range(0, len(ILP_gen)):
            ILP_gen[k] = (1 - Diff)*ILP_gen[k]
    if (abs(SUM_Gen) > abs(SUM_Load)):
        if (SUM_Load != 0):
            Diff = (abs(SUM_Gen) - abs(SUM_Load)) / abs(SUM_Load)
        else:
            Diff = 1
        for k in range(0, len(ILP_load)):
            ILP_load[k] = (1- Diff)*ILP_load[k]
    ########################################
    for n in H.nodes():
        j = H.nodes().index(n)
        i = H_Working.nodes().index(n)
        #if (i > 0):
        #    P[j-1, 0] = power[i]
        if (len(H_Working.nodes()) > 10):
            if (0 < i < 113):
                #Generator.append(n)
                h= Generator.index(n)
                P[j-1, 0] = ILP_gen[h]
                #power[i] = ILP_gen[h]
                #TotalGenPower = TotalGenPower + power[i]
            elif (113 <= i < 310):#210):
                #Load.append(n)
                h= Load.index(n)
                P[j-1, 0] =ILP_load[h]
                #power[i] = ILP_load[h]
                #TotalPower = TotalPower + power[i]
        else:
            if (0 < i < 1):
                #Generator.append(n)
                h= Generator.index(n)
                P[j-1, 0] =ILP_gen[h]
                #power[i] = ILP_gen[h]
                #TotalGenPower = TotalGenPower + power[i]
            elif (1 <= i < 3):
                #Load.append(n)
                h= Load.index(n)
                P[j-1, 0]=ILP_load[h]
                #power[i] = ILP_load[h]
                #TotalPower = TotalPower + power[i]
        """
        if (i < 113):
            ILP_gen.append(power[i])
            TotalGenPower = TotalGenPower + power[i]
            Generator.append(n)
        elif (113 <= i < 210):
            ILP_load.append(power[i])
            TotalPower = TotalPower + power[i]
            Load.append(n)
        """
    #for i in range(1, NumberofNodes):
    #    P[i-1, 0] = power[i]
    #TheTeta = np.linalg.solve(a, b)
    #for j in range(0, NumberofNodes):
    #    if (j < 113):
    #        TotalGenPower = TotalGenPower + power[j]
    #        ILP_gen.append(power[j])
    #    elif (113 <= j < 210):
    #        ILP_load.append(power[j])
    #        TotalPower = TotalPower + power[j]
    #for m in range(0, len(link1)):
    for e in H.edges():
        i = H.nodes().index(e[0])#e[0]
        j = H.nodes().index(e[1])#e[1]
        #print 'i,j:'
        #print i, j, X[i-1, j-1]
        e1 = e[0]
        e2 = e[1]
        this_react = H[e1][e2]['weight']
        X[i,j] = this_react
        X[j,i] = this_react
        #if (X[i,j] != 0):
        #    X[i,j] =  float("%0.10f"%(((this_react*X[i,j])/(X[i,j] + this_react))))
        #    X[j,i] =  float("%0.10f"%(((this_react*X[j,i])/(X[j,i] + this_react))))
        #else:
        #    X[i,j] =  float("%0.10f"%(((this_react))))
        #    X[j,i] =  float("%0.10f"%(((this_react))))
        #if G.has_edge(subject_id, object_id):
        #            # we added this one before, just increase the weight by one
        #            G[subject_id][object_id]['weight'] += 1
        #i = link1[m]
        #j = link2[m]
        ##if (X[i-1,j-1] != 0):
        ##    X[i-1,j-1] =  float("%0.10f"%(((reactances[m]*X[i-1,j-1])/(X[i-1,j-1] + reactances[m]))))
        ##    X[j-1,i-1] =  float("%0.10f"%(((reactances[m]*X[j-1,i-1])/(X[j-1,i-1] + reactances[m]))))
        ##else:
        ##    X[i-1,j-1] =  float("%0.10f"%(((reactances[m]))))
        ##    X[j-1,i-1] =  float("%0.10f"%(((reactances[m]))))
    for i in range(0, NumberofNodes):
        for j in range(0, NumberofNodes):
            if (i == j):
                for k in range(0,NumberofNodes):
                    if (X[i,k] !=0):
                        b[i,j] =  float("%0.10f"%(((b[i,j] + 1/X[i,k]))))
            else:
                if X[i,j] !=0:
                    b[i,j] =  float("%0.10f"%(((-1/X[i,j]))))
    print 'b[0, 0]'
    print b[0,0]
    Br = np.zeros(shape= (NumberofNodes -1 ,NumberofNodes-1))
    for i in range(0,NumberofNodes -1):
      for j in range(0, NumberofNodes -1):
          Br[i,j] = b[i+1,j+1]
    ####################################################
    if (matrix_rank(Br)== NumberofNodes -1):
        TheTeta = np.linalg.solve(-Br, P)
    else:
        print 'ERROR:'
        print 'Matrix rank:'
        print matrix_rank(Br)
        print 'Number of Nodes:'
        print NumberofNodes
        print 'Number of Edges:'
        print len(H.edges())
        TheTeta = np.zeros(shape = (NumberofNodes-1, 1))
    #TheTeta = np.linalg.solve(-Br, P)
    ##############################################################################
    ####################Find the power Flows at each link: #######################
    #i = 0
    print 'TheTeta:'
    #print TheTeta
    ##for i in range(0, len(TheTeta)):
    ##    print TheTeta[i], i
    Teta = np.zeros(shape = (NumberofNodes, 1))
    Teta[0] = 0
    for i in range(0, NumberofNodes -1):
        Teta[i+1,0] = TheTeta[i]
    flow = np.zeros(shape = (len(H.nodes()), len(H.nodes())))
    flow_edges = []
    for e in H.edges():
        i = H.nodes().index(e[0])#e[0]
        j= H.nodes().index(e[1])#e[1]
        e1 = e[0]
        e2 = e[1]
        #print 'e1, e2'
        #print e1, e2
        #print 'He1e2:'
        #print H[e1][e2]['weight']
        flow[i][j] = (Teta[i] - Teta[j])/H[e1][e2]['weight']
        flow[j][i] = (Teta[j] - Teta[i])/H[e1][e2]['weight']
        flow_edges.append(e)
        #i = i + 1
        ##print 'Thissssssssssssssssssssss Floooooooooooooooooooow:'
        print flow[i][j],Teta[i], Teta[j], i, j, e1, e2, H[e1][e2]['weight']
        my_flows.append(flow[i][j])
        #my_Model.addConstr(flows[j,i,1]*reactances[m] == Teta[j-1] - Teta[i-1], 'FlowsRCons_%s'% (m))
    print 'Flows:HHHHHHHHHHHHHHHHHHHHHaaaaaaaaaaaaaaaHHHHHHHHHHHaaaaaa'
    print flow
    #################################################################################
    #ILP Power and load
    """
    for p in range(0,len(ILP_load)):
        ILP_load[p] = 0
    for g in range(0, len(ILP_gen)):
        ILP_gen[g] = 0
    TotalPower = 0
    for n in H.nodes():
        neighbors = H.neighbors(n)
        for n2 in neighbors:
            f1 = H.nodes().index(n)
            f2 = H.nodes().index(n2)
            #j = Load.index(n) #H.nodes().index(n)
            i = H_Working.nodes().index(n)
            if (i < 113):
                j = Generator.index(n)
                ILP_gen[j] = ILP_gen[j] + flow[f1][f2]
                #ILP_gen.append(power[i])
                #TotalGenPower = TotalGenPower + power[i]
            elif (113 <= i < 210):
                j = Load.index(n)
                ILP_load[j] = ILP_load[j] + flow[f1][f2]
                #ILP_load.append(power[i])
                #TotalPower = TotalPower + power[i]
    """
    for p in range(0, len(ILP_load)):
        TotalPower = TotalPower + ILP_load[p]
    for p in range(0, len(ILP_gen)):
        TotalGenPower = TotalGenPower + ILP_gen[p] 
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
    ######################################################
    #Comment all the gurobi optimization:
    #TotalPower = []
    #TotalPower = 0
    #for i in range(0, len(ILP_load)):
    #  TotalPower = TotalPower + ILP_load[i]
    print 'Total Power HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH:'
    print TotalPower
    print 'Loads Power:'
    print ILP_load
    print 'Generator Power:'
    print ILP_gen
    return flow_edges, my_flows, ILP_gen, ILP_load, cost, TotalPower, TotalGenPower #ILP_gen_power, ILP_load_power, cost #ILP_flows#flows

