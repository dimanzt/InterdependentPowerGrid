__author__ = 'Diman'

from gurobipy import *
import numpy as np
from numpy.linalg import matrix_rank

# Model data
def optimal_Power_Control_discrete(H_Working, H, nodes, power, link1, link2, reactances, linkNum, Thr):
    flows = []
    flow_edges = []
    cost = []
    Total_power = []
    ILP_gen_power = []
    ILP_load_power = []
    #########################GREEEDY BASED APPROACH###############################
    flow_edges, flows, ILP_gen_power, ILP_load_power, cost, TotalPower, TotalGenPower = Power_Control_discrete_solution(H_Working, H, nodes, power, link1, link2, reactances, linkNum, Thr)

    return flow_edges, flows, ILP_gen_power, ILP_load_power, cost, TotalPower, TotalGenPower
###
# Solve ILP of max flow problem where the Sets are given and each set can identify a set of links,

def Power_Control_discrete_solution(H_Working, H, nodes, power, link1, link2, reactances, linkNum, Thr):
    #Power_gen_t = []
    #Power_load_t = []
    my_flows = []
    ILP_gen = []
    ILP_load = []
    ILP_jun = []
    cost = []
    w_g = 10
    w_l = 100
    Max_Thr = Thr#0.3#1.5
    Min_Thr = (-1)*Thr#-0.3#1.5
    P_g_max = 2
    P_g_min = -2
    P_l_max = -2
    P_l_min = 2
    Generator = []
    Load = []
    Junction = []
    #############################################################################
    ##Create the Br matrix
    NodeNum = len(H.nodes())
    EdgeNum = len(H.edges())
    b = np.zeros(shape=(NodeNum,NodeNum))
    X = np.zeros(shape=(NodeNum,NodeNum))
    P = np.zeros(shape=(NodeNum -1,1))
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
            elif (113 <= i < 210):
                Load.append(n)
                ILP_load.append(power[i])
                #TotalPower = TotalPower + power[i]
            elif (210 <= i < 310):
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

    #0: 113
    NumGen = len(ILP_gen)
    #113:210
    NumPow = len(ILP_load)
    NumJun = NodeNum - NumGen - NumPow

    """
    for i in range(1, NodeNum):
        P[i-1, 0] = power[i]
    TheTeta = np.linalg.solve(a, b)

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
    """
    NumberofNodes = NodeNum
    for e in H.edges():
        i = H.nodes().index(e[0])#e[0]
        j = H.nodes().index(e[1])#e[1]
        #print 'i,j:'
        #print i, j, X[i-1, j-1]
        e1 = e[0]
        e2 = e[1]
        this_react = H[e1][e2]['weight']
        if (X[i,j] != 0):
            X[i,j] =  float("%0.10f"%(((this_react*X[i,j])/(X[i,j] + this_react))))
            X[j,i] =  float("%0.10f"%(((this_react*X[j,i])/(X[j,i] + this_react))))
        else:
            X[i,j] =  float("%0.10f"%(((this_react))))
            X[j,i] =  float("%0.10f"%(((this_react))))
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
    ####################################################
    if (matrix_rank(Br)== NumberofNodes -1):
        TheTeta = np.linalg.solve(-Br, P)
    else:
        print 'ERROR:'
        TheTeta = np.zeros(shape = (NumberofNodes-1, 1))
    ##############################################################################
    ####################Find the power Flows at each link: #######################
    #i = 0
    ##print 'TheTeta:'
    #print TheTeta
    ##for i in range(0, len(TheTeta)):
    ##    print TheTeta[i], i
    #########################GREEEDY BASED APPROACH###############################
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
    for i in range(0, NodeNum):#(0, 310):
    #for i in range(0,3):
        my_objects.append(Node([], [],Node_index, Node_index, Node_index ))
        Node_index = Node_index + 1


    for m in range(0, len(link1)):
        for k in range(0, NodeNum):#(0, 310):
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
    """    
    for obj in my_objects:
        print obj.e
        #print obj.m
        #print obj.n
        #if obj.n not in Edges:
        #    Edges.append(obj.n)
    """
    ##########################################
    my_Model = Model('DCPowerflow')
    P_g_t = {}
    P_l_t = {}
    flows = {}
    flow_edges = {}
    P_j_t = {}
    Teta = {}
    delta = {}
    ILP_gen_power = []
    ILP_load_power = []
    #for p in range(0,2):
    for p in range(0, NumGen): #113):
        P_g_t[p] = my_Model.addVar(ub=2, lb=0, vtype=GRB.CONTINUOUS, name='GeneratorPower%s'% (p)) 
    #for e in range(2, 3):
    for e in range(NumGen, NumGen + NumPow):#(113, 210):
        P_l_t[e] = my_Model.addVar(ub=0, lb=-2, vtype=GRB.CONTINUOUS, name='LoadPower%s'% (e))
    for k in range(NumGen+NumPow, NodeNum):#(210, 310):
    #for k in range(0,0):
        P_j_t[k] = my_Model.addVar(ub=2, lb=-2, vtype=GRB.CONTINUOUS, name='JunctionPower%s'% (k))
    for h in range(0,NodeNum):#310):
        Teta[h] = my_Model.addVar(ub=100, lb=-100, vtype=GRB.CONTINUOUS, name='Theta%s'% (h))
    for e in range(0, NodeNum):
        delta[e] = my_Model.addVar(ub = 1, lb = 0, vtype=GRB.BINARY, name='OnOff%s'% (e))

    theEdges= []
    #for m in range(0, len(link1)):
    for e in H.edges():
        #i = link1[m]
        i = e[0]
        #j = link2[m]
        j = e[1]
        edge= (i,j)
        if edge not in theEdges:
            theEdges.append(edge)
            #print 'i,j:'
            #print i,j
            flows[i,j,1] = my_Model.addVar(ub=Max_Thr, lb=Min_Thr, vtype=GRB.CONTINUOUS, name='Flow_%s_%s_%s'% (i,j,1))
            flows[j,i,1] = my_Model.addVar(ub=Max_Thr, lb=Min_Thr, vtype=GRB.CONTINUOUS, name='Flow_%s_%s_%s'% (j,i,1)) 
        #else:#if edge in theEdges:
        #    flows[i,j,2] = my_Model.addVar(ub=Max_Thr, lb=Min_Thr, vtype=GRB.CONTINUOUS, name='Flow_%s_%s_%s'% (i,j,2))
        #    flows[j,i,2] = my_Model.addVar(ub=Max_Thr, lb=Min_Thr, vtype=GRB.CONTINUOUS, name='Flow_%s_%s_%s'% (j,i,2))
        #print 'theEdges'
        #print theEdges
    my_Model.update()
    for i in range(0, NumGen): #113):
    #for i in range(0,2):
        my_Model.addConstr(ILP_gen[i] -0.2 <= P_g_t[i], 'Non_Negative_Power_%s'% (i) ) #power[i] - 0.0001
        #my_Model.update()
    for j in range(0, NumGen):#113):
    #for j in range(0,2):
        #my_Model.addConstr(P_g_t[j] <= P_g_max, 'Max_Gen_Power_%s'% (j))
        my_Model.addConstr(P_g_t[j] <= ILP_gen[j], 'Max_Gen_Power_%s'% (j))
        #my_Model.update()
    #Load constraints
    for i in range(NumGen, NumGen + NumPow):#(113, 210):
    #for i in range(2, 3):
        #my_Model.addConstr(power[i] <= P_l_t[i] , 'Non_Negative_Power_%s'% (i))
        my_Model.addConstr(ILP_load[i - NumGen]  <= P_l_t[i] , 'Non_Negative_Power_%s'% (i))
        #my_Model.update()
    for j in range(NumGen, NumGen + NumPow): #(113, 210):
    #for j in range(2, 3):
        my_Model.addConstr(P_l_t[j] <= ILP_load[j-NumGen] +0.2 , 'Max_Load_Power_%s'% (j))
    #Diman commented two lines
    #for k in range(210, 310):
    #    my_Model.addConstr(P_j_t[k] == power[k], 'Junction_Power_%s'% (k))
    my_Model.update()
    my_Model.addConstr(Teta[0] == 0.0, 'ReferenceVoltage')
    #for k in range(1, NumGen):#(1, 113):
    #for x in H.nodes():
    #    if (x> 1):
    #        if x in Generator:
    #            k = Generator.index(x)
    #            my_Model.addConstr(P_g_t[k] == sum(Br[k-1, j-1]*Teta[j] for j in range(1, NodeNum)), 'GenFlow_%s'% (k))
    for k in range(1, NumGen):#(1, 113):
        #my_Model.addConstr(P_g_t[k] == sum(Br[k-1, j-1]*Teta[j] for j in range(1, 310)), 'GenFlow_%s'% (k))
        my_Model.addConstr(P_g_t[k]*delta[k] == sum(Br[k-1, j-1]*Teta[j] for j in range(1, NodeNum)), 'GenFlow_%s'% (k))
    my_Model.update()
    #for k in range(NumGen, NumGen + NumPow): #(113, 210):
    #for x in H.nodes():
    #    if (x > 1):
    #        if x in Load:
    #            k = Load.index(x)
                #my_Model.addConstr(P_l_t[k] == sum(Br[k-1, j-1]*Teta[j] for j in range(1, 310)), 'LoadFlow_%s'% (k))
    for k in range(NumGen, NumGen + NumPow): #(113, 210):
        my_Model.addConstr(P_l_t[k]*delta[k] == sum(Br[k-1, j-1]*Teta[j] for j in range(1, NodeNum)), 'LoadFlow_%s'% (k))
    my_Model.update()
    #for k in range(NumGen + NumPow, NodeNum):
    #    my_Model.addConstr(P_j_t[k] == ILP_jun[k- NumGen - NumPow], 'JunctionPow_%s'% (k))
    #for k in range(NumGen + NumPow, NodeNum): #(210, 310):
    #for x in H.nodes():
    #    if (x >1):
    #        if x in Junction:
    #            k = Junction.index(x)
    #            #my_Model.addConstr(P_j_t[k] == sum(Br[k-1, j-1]*Teta[j] for j in range(1,310)), 'JunctionFlow_%s'% (k))
    for k in range(NumGen + NumPow, NodeNum):
        my_Model.addConstr(P_j_t[k]*delta[k] == sum(Br[k-1, j-1]*Teta[j] for j in range(1,NodeNum)), 'JunctionFlow_%s'% (k))
    my_Model.update()
    #Load line capacities:
    theEdges= []
    #for m in range(0, len(link1)):
    for e in H.edges():
        #for j in range(0, 210):
        #i= link1[m]
        e1 = e[0]
        i = e1
        Tetai = H.nodes().index(e1)
        #i = e1 -1 
        #j = link2[m]
        e2 = e[1]
        j = e2
        #j = e2 -1
        Tetaj = H.nodes().index(e2)
        react = H[e1][e2]['weight']
        #print 'reactances:'
        #print react
        edge = (e1,e2)
        if edge not in theEdges:
            theEdges.append(edge)
            my_Model.addConstr(Min_Thr <= flows[i,j,1], 'Min_Flow_Thr1_%s_%s_%s'% (i,j,1))
            #my_Model.update()
            my_Model.addConstr(flows[i,j,1] <= Max_Thr, 'Max_Flow_Thr1_%s_%s_%s'% (i,j,1))
            #my_Model.update()
            my_Model.addConstr(flows[j,i,1] <= Max_Thr, 'Max_Flow_Thr2_%s_%s_%s'% (j,i,1))
            #my_Model.update()
            my_Model.addConstr(Min_Thr <= flows[j,i,1], 'Min_Flow_Thr2_%s_%s_%s'% (j,i,1))
            #my_Model.update()
            my_Model.addConstr(flows[i,j,1] + flows[j,i,1] == 0, 'Flows_dir_%s_%s_%s'% (i,j,1))
            #Reactance:
            my_Model.addConstr(flows[i,j,1]*react == (Teta[Tetai] - Teta[Tetaj]), 'FlowsCons_%s_%s_%s'% (i,j,1))
            my_Model.addConstr(flows[j,i,1]*react == (Teta[Tetaj] - Teta[Tetai]), 'FlowsRCons_%s_%s_%s'% (j,i,1))
            #my_Model.addConstr(flows[i,j,1]*reactances[m] == Teta[i-1] - Teta[j-1], 'FlowsCons_%s'% (m))
            #my_Model.addConstr(flows[j,i,1]*reactances[m] == Teta[j-1] - Teta[i-1], 'FlowsRCons_%s'% (m))
            #my_Model.update()
        """
        else:#if edge in theEdges:
            #my_Model.rem
            my_Model.addConstr(Min_Thr <= flows[i,j,2], 'Min_Flow_Thr1_%s_%s_%s'% (i,j,2))
            #my_Model.update()
            my_Model.addConstr(flows[i,j,2] <= Max_Thr, 'Max_Flow_Thr1_%s_%s_%s'% (i,j,2))
            #my_Model.update()
            my_Model.addConstr(flows[j,i,2] <= Max_Thr, 'Max_Flow_Thr2_%s_%s_%s'% (j,i,2))
            #my_Model.update()
            my_Model.addConstr(Min_Thr <= flows[j,i,2], 'Min_Flow_Thr2_%s_%s_%s'% (j,i,2))
            #my_Model.update()
            my_Model.addConstr(flows[i,j,2] + flows[j,i,2] == 0, 'Flows_dir_%s_%s_%s'% (i,j,2))
            my_Model.addConstr(flows[i,j,2]*react == Teta[i-1] - Teta[j-1], 'FlowCons2_%s_%s_%s'% (i,j,2))
            my_Model.addConstr(flows[j,i,2]*react == Teta[j-1] - Teta[i-1], 'FlowsRCons_%s_%s_%s'% (i,j,2))
            #my_Model.addConstr(flows[i,j,2]*reactances[m] == Teta[i-1] - Teta[j-1], 'FlowCons2_%s'% (m))
            #my_Model.addConstr(flows[j,i,2]*reactances[m] == Teta[j-1] - Teta[i-1], 'FlowsRCons_%s'% (m))
            #my_Model.update()
        """    
    ###Flow Conservation:
    #my_Model.addConstr((quicksum(P_g_t[l] for l in range(0,113)) + quicksum(P_l_t[j] for j in range(113, 210))) >= -0.1, 'ConsumedGeneratedPower')
    #my_Model.addConstr((quicksum(P_g_t[l] for l in range(0,113)) + quicksum(P_l_t[j] for j in range(113, 210))) <= 0.1, 'ConsumedGeneratedPower')
    my_Model.addConstr((quicksum(P_g_t[l]*delta[l] for l in range(0,NumGen)) + quicksum(P_l_t[j]*delta[j] for j in range(NumGen, NumGen + NumPow))) >= -0.2, 'ConsumedGeneratedPower')
    my_Model.addConstr((quicksum(P_g_t[l]*delta[l] for l in range(0,NumGen)) + quicksum(P_l_t[j]*delta[j] for j in range(NumGen, NumGen + NumPow))) <= 0.2, 'ConsumedGeneratedPower')

    ##my_Model.addConstr((quicksum(P_g_t[l] for l in range(0,2)) + quicksum(P_l_t[j] for j in range(2, 3))) == 0, 'ConsumedGeneratedPower')

    my_Model.update()
    #Flow Conservation constraint:
    #theEdges = []
    #for k in range(0, NumGen): #(0, 113):i
    #for k  in range(0, 2): 
    for x in H.nodes():
        #print 'Nodes in the disrupted graph:'
        #print x
        edges =[]
        theEdges =[]
        thisNode = x
        realIndex = H_Working.nodes().index(thisNode)
        #if (realIndex <= NumGen):
        if x in Generator:
            k = Generator.index(x)
            neighbors = H.neighbors(thisNode)
            if (len(neighbors) != 0):
                for node in H.neighbors(thisNode):
                    e = (thisNode, node)
                    if (thisNode,node,1) not in edges:
                        theEdges.append((thisNode, node, 1))
                        edges.append(e)
                if (theEdges !=[]):
                    #print 'theEdges:'
                    #print theEdges
                    #print 'K:'
                    #print k
                    #print 'Number of Generatores'
                    #print NumGen
                    #print Generator
                    #print (len(Generator))
                    #for p in range(0, NumGen):
                    #    print p
                    my_Model.addConstr(sum(flows[l,f,g] for (l,f,g) in theEdges) == P_g_t[k]*delta[k], 'Gen_FlowConservation_%s'% (k))
                    my_Model.update()
                else: #elif(theEdgs ==[]):
                #print 'ZERRROOOOOOOOOOOOOOO'
                #print theEdges
                    my_Model.addConstr(P_g_t[k]*delta[k] == 0, 'Gen_FlowConservation_%s'% (k))
                    my_Model.update()
            else:
                my_Model.addConstr(P_g_t[k]*delta[k] == 0, 'Gen_FlowConservation_%s'% (k))
        """
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
                    #else: #if e in edges:
                    #    edges.append(e)
                    #    theEdges.append((i,j,2))
                if (j == k+1):
                    e = (j,i)
                    if e not in edges:
                      edges.append(e)
                      theEdges.append((j,i,1))
                    #else: #if e in edges:
                    #  edges.append(e)
                    #  theEdges.append((j,i,2))
            #Diman Commented:
            #print 'INJAAAAAAAAAAA:'
            #print theEdges
            #for (e,f,g) in theEdges:
            #    print e,f,g
            #my_Model.addConstr(sum(flows[k,f,g] for (k,f,g) in theEdges) == P_g_t[k], 'Gen_FlowConservation_%s'% (k))
            
            if (theEdges !=[]):
                my_Model.addConstr(sum(flows[l,f,g] for (l,f,g) in theEdges) == P_g_t[k], 'Gen_FlowConservation_%s'% (k))
                my_Model.update()
            else: #elif(theEdgs ==[]):
                #print 'ZERRROOOOOOOOOOOOOOO'
                #print theEdges
                my_Model.addConstr(P_g_t[k] == 0, 'Gen_FlowConservation_%s'% (k))
                my_Model.update()
        else:
            my_Model.addConstr(P_g_t[k] == 0, 'Gen_FlowConservation_%s'% (k)) 
    """
    #Load flow conservation:
    #for k in range(NumGen, NumGen + NumPow): #(113, 210):
    #for k in range(2,3):
    for x in H.nodes():
        #print 'Nodes in the disrupted graph:'
        #print x
        edges =[]
        theEdges =[]
        thisNode = x
        realIndex = H_Working.nodes().index(thisNode)
        #if (realIndex <= NumGen):
        if x in Load:
            k = Load.index(x)
            neighbors = H.neighbors(thisNode)
            if (len(neighbors) != 0):
                for node in H.neighbors(thisNode):
                    e = (thisNode, node)
                    if (thisNode,node,1) not in edges:
                        theEdges.append((thisNode, node, 1))
                        edges.append(e)
                if (theEdges !=[]):
                    #print 'theEdges:'
                    #print theEdges
                    #print 'K:'
                    #print k
                    #print 'Number of Loads'
                    #print NumPow
                    #print Load
                    #print (len(Load))
                    my_Model.addConstr(sum(flows[l,f,g] for (l,f,g) in theEdges) == P_l_t[k+NumGen]*delta[k+NumGen] , 'Load_FlowConservation_%s'% (k))
                    #my_Model.addConstrs((flows.sum(e,f,g)  == P_l_t[k] for (e,f,g) in theEdges for k in range(113,210)), "node")
                    my_Model.update()
                else: #elif(theEdges == []):
                    my_Model.addConstr( P_l_t[k]*delta[k] == 0 , 'Load_FlowConservation_%s'% (k))
                    my_Model.update()
            else:
                my_Model.addConstr( P_l_t[k]*delta[k] == 0 , 'Load_FlowConservation_%s'% (k))
        """
        if (my_objects[k].e != ([], [])):
            for (i,j) in my_objects[k].e:
                if (i == k+1):
                    e = (i,j)
                    if e not in edges:
                        theEdges.append((i,j,1))
                        edges.append(e)
                    #else: #if e in edges:
                    #    edges.append(e)
                    #    theEdges.append((i,j,2))
                if (j == k+1):
                    e = (j,i)
                    if e not in edges:
                      edges.append(e)
                      theEdges.append((j,i,1))
                    #else: # e in edges:
                    #  edges.append(e)
                    #  theEdges.append((j,i,2))

            if (theEdges !=[]):
                my_Model.addConstr(sum(flows[k,f,g] for (k,f,g) in theEdges) == P_l_t[k] , 'Load_FlowConservation_%s'% (k))
                #my_Model.addConstrs((flows.sum(e,f,g)  == P_l_t[k] for (e,f,g) in theEdges for k in range(113,210)), "node")
                my_Model.update()
            else: #elif(theEdges == []):
                my_Model.addConstr( P_l_t[k] == 0 , 'Load_FlowConservation_%s'% (k))
                my_Model.update()
        else:
            my_Model.addConstr( P_l_t[k] == 0 , 'Load_FlowConservation_%s'% (k))
    """
    #m.addConstr( (quicksum(flow[h,k,i] for k,i in to_i) + inflow[h,i]) == (quicksum(flow[h,i,j] for i,j in from_i)),'node_%s_%s' % (h, i))
    #Junction flow conservation:
    #Diman commented
    for x in H.nodes():
        #print 'Nodes in the disrupted graph:'
        #print x
        edges =[]
        theEdges =[]
        thisNode = x
        realIndex = H_Working.nodes().index(thisNode)
        #if (realIndex <= NumGen):
        if x in Junction:
            k = Junction.index(x)
            neighbors = H.neighbors(thisNode)
            if (len(neighbors) != 0):
                for node in H.neighbors(thisNode):
                    e = (thisNode, node)
                    if (thisNode,node,1) not in edges:
                        theEdges.append((thisNode, node, 1))
                        edges.append(e)
                if (theEdges !=[]):
                    #print 'theEdges:'
                    #print theEdges
                    #print 'K:'
                    #print k
                    #print 'Number of Loads'
                    #print NumPow
                    #print Load
                    #print (len(Load))
                    my_Model.addConstr(sum(flows[l,f,g] for (l,f,g) in theEdges) == P_j_t[k+NumGen+NumPow]*delta[k+NumGen+NumPow] , 'Junction_FlowConservation_%s'% (k))
                    #my_Model.addConstrs((flows.sum(e,f,g)  == P_l_t[k] for (e,f,g) in theEdges for k in range(113,210)), "node")
                    my_Model.update()
                else: #elif(theEdges == []):
                    my_Model.addConstr( P_j_t[k]*delta[k] == 0 , 'Junction_FlowConservation_%s'% (k))
                    my_Model.update()
            else:
                my_Model.addConstr( P_j_t[k]*delta[k] == 0 , 'Junction_FlowConservation_%s'% (k))

    """ 
    for k in range(210, 310):
        edges =[]
        theEdges =[]
        if (my_objects[k].e != ([], [])):
            print 'my_objects[k].e'
            print my_objects[k].e
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
            #if power[k] >0:
            print 'Junction INJAAAAAAAAAAAAAA:'
            print theEdges
            my_Model.addConstr(quicksum(flows[e,f,g] for (e,f,g) in theEdges ) == P_j_t[k], 'Jun_FlowConservation_%s'% (k))
            #if power[k] <=0:
            #    my_Model.addConstr(quicksum(flows[i,j,k] for (i,j,k) in theEdges ) + power[k] == 0, 'Gen_FlowConservation')
    """
    #my_M del.update()
    #    for j in range(0, 210):
    #        for k in range(0, len(link1)):
    #            if (i == link1[k]) and (j == link2[k]):

    ##for obj in my_objects:
    ##    my_Model.addConstr(quicksum(flows[obj.e,j] for j in obj. )== power[m])
    

    my_Model.update()
    #print 'length ILP load:'
    #print len(ILP_load)
    #print 'length ILP gen:'
    #print len(ILP_gen)
    #for l in range(112, 113):
    #    print ILP_gen[l]
    #my_Model.optimize()
    #my_Model.setObjective(w_g*(sum((P_g_t[l] - power[l] ) for l in range(0,NumGen)))+w_l*(sum((P_l_t[l] - power[l]) for l in range(NumGen,NumGen + NumPow))), GRB.MINIMIZE)
    my_Model.setObjective(w_g*(sum(( ILP_gen[l] - P_g_t[l]*delta[l] ) for l in range(0,NumGen)))+w_l*(sum((P_l_t[l]*delta[l] - ILP_load[l- NumGen]) for  l in range(NumGen,NumGen + NumPow))), GRB.MINIMIZE)
    #my_Model.setObjective(w_g*(sum((P_g_t[l] - power[l] ) for l in range(0,113)))+w_l*(sum((P_l_t[l] - power[l]) for l in range(113,210))), GRB.MINIMIZE)
    ##my_Model.setObjective(w_g*(quicksum((P_g_t[l]-power[l] ) for l in range(0,2)))+w_l*(quicksum((P_l_t[l] - power[l]) for l in range(2,3))), GRB.MINIMIZE)

    my_Model.update()
    ILP_load_sol = []
    ILP_gen_sol = []
    my_Model.optimize()
    ###################################################################
    if my_Model.status == GRB.status.OPTIMAL:
        ILP_flows=[]
        ILP_gen_power=[]
        for p in range(0, NumGen):#(0, 113):
        #for p in range(0,2):
            var_reference = my_Model.getVarByName('GeneratorPower%s'% (p)) # ('GeneratorPower%s'%(i)) #Generator's power
            #Diman Commented
            ###print 'var_reference'
            ###print var_reference.x
            ILP_gen_power.append(var_reference.x)
            #if var_reference.x>0:
                #Diman Commented:
                ###print 'Generator Power:'
                ###print var_reference.x
                #ILP_gen_power.append(p)
                #print 'Generator Power:'
                #print ILP_gen_power
        ILP_load_power=[]
        for e in range(NumGen, NumGen + NumPow):#(113, 210):
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
        """
        for m in range(0, len(link1)):
            i = link1[m]
            j = link2[m]
            e = (i,j)
            if e not in theEdges:
                theEdges.append(e)
                #print 'i,j'
                #print i,j
                my_flow = my_Model.getVarByName('Flow_%s_%s_%s'%(i,j,1))
                my_flow_reverse = my_Model.getVarByName('Flow_%s_%s_%s'%(j,i,1))
            else:#if e in theEdges:
                my_flow = my_Model.getVarByName('Flow_%s_%s_%s'%(i,j,2))
                my_flow_reverse = my_Model.getVarByName('Flow_%s_%s_%s'%(j,i,2))
            print 'my_flow.x:'
            print my_flow.x
            #print 'my_flow_reverse.x:'
            #print my_flow_reverse.x
            print 'i,j:'
            print i,j
            if my_flow.x>0 or my_flow_reverse.x>0:
                #print 'MY_FLOW.X:'
                #print my_flow.x
                edge = (i,j)
                #print 'i,j:'
                #print edge
                ILP_flows.append(edge)
        """
        #Add the generator's power to the results:
        ILP_gen_sol = []
        ILP_gen_cont = []
        gen_sol = my_Model.getAttr('x', P_g_t)
        delta_sol = my_Model.getAttr('x', delta)
        #for h in range(0, NumGen):#(0, 113):
        #for h in range(0,2):
        for n in H_Working.nodes():
            if (len(H_Working.nodes()) > 10):
                if ( n <= 113):
                    if n in Generator:
                        k = Generator.index(n)
                        ILP_gen_sol.append(gen_sol[k]*delta_sol[k])
                        ILP_gen_cont.append(gen_sol[k]*delta_sol[k])
                    else:
                        ILP_gen_cont.append(power[n-1])
                        ILP_gen_sol.append(0)

            else:
                if ( n <= 1):
                    if n in Generator:
                        k = Generator.index(n)
                        ILP_gen_sol.append(gen_sol[k]*delta_sol[k])
                        ILP_gen_cont.append(gen_sol[k]*delta_sol[k])

                    else:
                        ILP_gen_sol.append(0)
                        ILP_gen_cont.append(power[n-1])
        #Add the load's power to the results:
        ILP_load_sol = []
        ILP_load_cont = []
        load_sol = my_Model.getAttr('x', P_l_t)
        #print 'Loaaaaaaaaaaaaaaaaad:'
        #print load_sol
        #for h in range(NumGen, NumGen + NumPow):#(113, 210):
        for n in H_Working.nodes():
            if (len(H_Working.nodes()) > 10):
                if (113 < n <= 210):
                    if n in Load:
                        k = Load.index(n)
                        ILP_load_sol.append(load_sol[k+NumGen]*delta_sol[k+NumGen])
                        ILP_load_cont.append(load_sol[k+NumGen]*delta_sol[k+NumGen])
                    else:
                        ILP_load_sol.append(0)#(power[n-1])
                        ILP_load_cont.append(power[n-1])
            else:
                if (1 < n <= 3):
                    if n in Load:
                        k = Load.index(n)
                        ILP_load_sol.append(load_sol[k+NumGen]*delta_sol[k+NumGen])
                        ILP_load_cont.append(load_sol[k+NumGen]*delta_sol[k+NumGen])
                    else:
                        ILP_load_sol.append(0)#(power[n-1])
                        ILP_load_cont.append(power[n-1])

        print 'ILP_load_sol:'
        print ILP_load_sol
        print 'length:'
        print len(ILP_load_sol)
        print 'ILP_gen_sol:'
        print ILP_gen_sol
        #for h in range(2, 3):
        #    ILP_load_sol.append(load_sol[h])
        #Add the flows of the lines to the results:
        solution = my_Model.getAttr('x', flows)
        theEdges = []
        flow_edges = []
        #for h in range(0, len(link1)):
        for edge in H.edges():
            #i = link1[h]
            i = edge[0]
            #j = link2[h]
            j = edge[1]
            e = (i,j)
            flow_edges.append(e)
            if e not in theEdges:
                theEdges.append(e)
                f = 1
            else:
                f =2
            #Diman Commented:
            ###print('\nOptimal flows for %s_%s:' % (i,j))
            #for i,j in arcs:
            #    if solution[h,i,j] > 0:
            #Diman Commented:
            ###print('%s -> %s, %s: %g' % (i, j, f, solution[i,j,f]))
            my_flows.append(solution[i,j,f])
        cost =[]
        cost = my_Model.objVal
        print 'Solution:'
        print('The optimal objective is %g' % my_Model.objVal)
        #Add The angle's solution:
        Theta_sol = []
        teta_sol = my_Model.getAttr('x', Teta)
        for k in range(0, NodeNum):#(0, 310):
            Theta_sol.append(teta_sol[k])
        #print 'Theta:'
        #print Theta_sol
    #Find the flows:
    ###Find the total power delivered:
    TotalPower = []
    TotalPower = 0
    TotalGenPower = []
    TotalGenPower = 0
    for i in range(0, len(ILP_load_sol)):
      TotalPower = TotalPower + ILP_load_sol[i]
    for i in range(0, len(ILP_gen_sol)):
      TotalGenPower = TotalGenPower + ILP_gen_sol[i]
    print 'Total Power HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH:'
    print TotalPower
    return flow_edges, my_flows, ILP_gen_cont, ILP_load_cont, cost, TotalPower, TotalGenPower #ILP_gen_power, ILP_load_power, cost #ILP_flows#flows

