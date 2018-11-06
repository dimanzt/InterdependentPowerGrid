__author__ = 'Diman'

from gurobipy import *
import numpy as np

# Model data
def optimal_Solve_DC_Flow(nodes, power, link1, link2, reactances, linkNum, Thr):
    flows = []
    cost = []
    Total_power = []
    ILP_gen_power = []
    ILP_load_power = []
    #########################GREEEDY BASED APPROACH###############################
    flows = Solve_DC_Flow_solution(nodes, power, link1, link2, reactances, linkNum, Thr)

    return flows #, ILP_gen_power, ILP_load_power, cost, TotalPower
###
# Solve ILP of max flow problem where the Sets are given and each set can identify a set of links,

def Solve_DC_Flow_solution(nodes, power, link1, link2, reactances, linkNum, Thr):
    #Power_gen_t = []
    #Power_load_t = []
    my_flows = []
    ILP_gen = []
    ILP_load = []
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
    b = np.zeros(shape=(310,310))
    X = np.zeros(shape=(310,310))
    P = np.zeros(shape=(309,1))
    for i in range(1, 310):
        neighbors = 0
        for m in range(0, len(link1)):
            if (i == link1[m]) or (i == link2[m]):
                neighbors = neighbors + 1
        if (neighbors > 0):
            P[i-1, 0] = power[i]
        else:
            P[i-1, 0] = 0
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
    TheTeta = np.linalg.solve(-Br, P)
    #TheTeta = np.linalg.solve.lstsq(-Br, P)
    #print 'GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG'
    #print TheTeta
    #print 'Size TheTeta'
    #print len(TheTeta)
    Current_Flows = np.zeros(shape=(len(link1), 1))
    CurrentTeta = np.zeros(shape=(310, 1))
    #CurrentTeta.append(0)
    for i in range(0, 309):
        CurrentTeta[i+1,0] = TheTeta[i]
    for m in range(0, len(link1)):
        #print 'link1[m]'
        #print link1[m]
        #print 'link2[m]'
        #print link2[m]
        #print 'TheTeta[link1]'
        #print CurrentTeta[link1[m]-1, 0]
        Current_Flows[m, 0] = float("%0.10f"%((CurrentTeta[link1[m]-1, 0] - CurrentTeta[link2[m]-1, 0])/reactances[m]))  # (TheTeta[link1[m]-1] - TheTeta[link2[m]-1])/ reactances[m]
    #print 'FLOOOOOOOOOOOOOOOOOOOOSSSS:'
    #print Current_Flows
    for m in range(0, len(link1)):
        my_flows.append(Current_Flows[m, 0])
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


    return my_flows#, ILP_gen, ILP_load, cost, TotalPower #ILP_gen_power, ILP_load_power, cost #ILP_flows#flows

