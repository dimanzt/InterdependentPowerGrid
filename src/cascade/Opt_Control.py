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
from my_lib_DC_Flow import *
###from my_lib_Power_Control import *
###from my_lib_Power_Control_discrete import *
#from my_lib import *
#https://www.diffchecker.com/efddo0xv
work_dir=os.getcwd()
#######################################################
#removed_g1, removed_g2= Let_it_Cascade(hviet, garr, init_removed_g1, init_removed_g2, h_inter, g_inter)
def Let_it_Cascade(hviet, garr, init_removed_g1_edges, init_removed_g1, init_removed_g2, h_inter, g_inter, Index, N_Index, j_Index):
    Thr = 0.5#1.3#float(sys.argv[1])
    seed_passed = j_Index
    seed_random=int(seed_passed)
    random.seed(seed_random)
    ##############################
    print 'Threshold:'
    print Thr
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
    #for e in hviet.edges():
        #print 'HVIET Edges:'
        #print e
    ################################################################################################################################
    nodes = []
    power = []
    linkNum = []
    link1 = []
    link2 = []
    power, nodes, linkNum, link1, link2, reactances = read_hviet()
    #if (len(link1) > 10):
    #    for i in range(210, 310):
    #        power[i] = 0
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
    #for n in init_removed_g2:
    #    if n not in Curr_Gray_Nodes:
    [non_cont_h_nodes, non_cont_h_edges, des_garr_nodes, des_garr_edges] = Destroy_Monitors_from_init(hviet, garr, h_inter, g_inter, init_removed_g1, init_removed_g2)    
    #[non_cont_h_nodes, non_cont_h_edges, des_garr_nodes, des_garr_edges] = Destroy_Monitors(hviet, garr, h_inter, g_inter, Dest_perc)
    NumberofCycles = 0
    [NumberofCycles, Curr_Gray_Edges, Curr_Gray_Nodes] = Count_Cycles(non_cont_h_nodes, non_cont_h_edges, hviet)
    print 'Number of Cycles :::::::::::::::::::::'
    print NumberofCycles
    Original_Gray_Edges = []
    for i in non_cont_h_edges:
        Original_Gray_Edges.append(i)
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
    Original_link1 = deepcopy(link1) #[]
    Original_link2 = deepcopy(link2) #[]
    Original_linkNum = deepcopy(linkNum) #[]
    Original_reactances = deepcopy(reactances)#[]
    Cascade_Thr = 5
    destroyed_edges = []
    unknown_graph = nx.MultiGraph()
    #########################################################################################################################################
    #Here try to solve DC power flow equations for each connected component of the graph
    k = 0
    num_edges =  len(hviet.edges())
    while (len(destroyed_edges) <  min((len(hviet.edges()) * (Index*1.8) / N_Index), len(hviet.edges()))):#((num_edges * (Index+len(init_removed_g2)) /N_Index))):
        rem = random.randint(0, len(link1)-1)
        #print 'removed index:'
        print 'edge index'
        print rem
        print 'size of link1:'
        print len(link1)
        e1 = link1[rem]
        e2 = link2[rem]
        e = (e1, e2)
        print 'Removed Edges:'
        print e, 'length destroyed edges:', len(destroyed_edges), 'length link1:', len(link1), 'TotalPower:', TotalPower
        print 'How many should be removes:',min((num_nodes * (Index*1.8) / N_Index), len(hviet.edges())), 'Index', Index 
        if e not in destroyed_edges:
            destroyed_edges.append(e)
            k += 1
            del link1[rem]
            del link2[rem]
            del linkNum[rem]
            del reactances[rem]
    """
    for edge in init_removed_g1_edges:
        rem = random.randint(0, len(link1)-1)
        #print 'removed index:'
        print 'edge index'
        print edge
        print 'size of link1:'
        print len(link1)
        e1 = link1[edge]
        e2 = link2[edge]
        e = (e1, e2)
        print 'Removed Edges:'
        print e
        if e not in destroyed_edges:
            destroyed_edges.append(e)
            k += 1
            del link1[edge]
            del link2[edge]
            del linkNum[edge]
            del reactances[edge]
    """
    #Hviet_Destroyed= get_graph_from_destroyed_graph(hviet, destroyed_edges)
    #graphs = list(nx.connected_component_subgraphs(Hviet_Destroyed))
    ##graphs_no_mon = list(nx.connected_component_subgraphs(Hviet_Destroyed_no_mon))
    #print graphs
    ################################################
    #######################################################################################################################################
    TotalPowerAllGraphs= []
    TotalPowerAllGraphs = 0
    TotalGenPowerAllGraphs = []
    TotalGenPowerAllGraphs = 0
    Max_nodes = []
    nodes_to_remove = []
    edges_to_remove = []
    cascade =1 
    test = 0
    for n in init_removed_g1:
        if n not in nodes_to_remove:
            nodes_to_remove.append(n)
    [flows, ILP_gen_power, ILP_load_power, cost, TotalPower] = optimal_DC_Flow(nodes, power, link1, link2,reactances, linkNum, Thr)
    print 'TotalPower:', TotalPower
    for n in hviet.nodes():#graph_des.nodes():
        #j = graph_des.nodes().index(n)
        i = hviet.nodes().index(n)
        j = i
        #print 'i'
        #print i
        #print 'j'
        #print j
        #print 'Number of loads'
        #print len(ILP_load_power)
        #print 'Number of Generators'
        #print len(ILP_gen_power)
        if (j <len(ILP_gen_power)):
            if (abs(ILP_gen_power[j]) < 0.1*abs(power[i])):
                if n not in nodes_to_remove:
                    nodes_to_remove.append(n)
        if (len(ILP_gen_power)<= j <(len(ILP_gen_power)+len(ILP_load_power))):
            generators = len(ILP_gen_power)
            if (abs(ILP_load_power[j-generators]) < 0.1*abs(power[i])):
                if n not in nodes_to_remove:
                   nodes_to_remove.append(n)
                    ####Add failed nodes to the initial failures if the power is zero:
                    #
    print 'Total Power of each connected component:'
    print TotalPower
    if (TotalPower >= 0.0):
        print 'TotalGenPower:'
        print TotalGenPower
        print 'TotalPower in Real Cascade:'
        print TotalPower
        print 'Size of this connected Max_nodes:'
        print len(Max_nodes)
        if (abs(TotalPower) <= abs(TotalGenPower)):
            TotalPowerAllGraphs = TotalPower #+ TotalPowerAllGraphs #+ TotalPower
            TotalGenPowerAllGraphs = TotalGenPower #+ TotalGenPowerAllGraphs #+ TotalGenPower
        elif(abs(TotalPower) > abs(TotalGenPower)):
            print 'WHAAAAAAAT THE FUCKKKKKK!'
            TotalPowerAllGraphs = TotalGenPower #+ TotalPowerAllGraphs
            TotalGenPowerAllGraphs = TotalGenPower #+TotalGenPowerAllGraphs
        #else:
    removed_g1_edges = []
    for e in destroyed_edges:
        removed_g1_edges.append(e)
    removed_g1 = nodes_to_remove
    removed_g2=init_removed_g2
    print 'k, removed_g1_edges, removed_g1, removed_g2, TotalPowerAllGraphs:'
    print k, removed_g1_edges, removed_g1, removed_g2, TotalPower
    return k, removed_g1_edges, removed_g1, removed_g2, TotalPower
    ########################################################################################################################################
    """
    while(cascade ==1):
        Max_nodes = []
        Hviet_Destroyed, nodes_to_remove, edges_to_remove= get_graph_from_destroyed_graph(hviet, destroyed_edges)
        print 'Hviet destroyed:'
        print len(Hviet_Destroyed.nodes())
        print len(hviet.nodes())
        graphs = list(nx.connected_component_subgraphs(Hviet_Destroyed))
        print 'Length of graphs:'
        print len(graphs)
        for g in graphs:
            graph_des = nx.Graph()
            graph_des = Create_Weighted(g, link1, link2, reactances)
            print 'connected component nodes'
            print len(graph_des.nodes())
            Maximum = len(Max_nodes) +1
            print 'Maximum'
            print Maximum
            test=test+1
            print test
            if (len(graph_des.nodes()) > 0) and (len(graph_des.nodes()) > Maximum ):#Maximum):
                Max_nodes = graph_des.nodes()
                flows = []
                flow_edges = []
                #[flow_edges, flows, ILP_gen_power, ILP_load_power, cost, TotalPower, TotalGenPower] = optimal_Power_Control_discrete(hviet, graph_des, nodes, power, link1, link2, reactances, linkNum, Thr) #optimal_DC_
                [flow_edges, flows, ILP_gen_power, ILP_load_power, cost, TotalPower, TotalGenPower]= optimal_Find_Flow(hviet, graph_des, nodes, power, link1, link2, reactances, linkNum, Thr)
                print 'ILP Gen:'
                print ILP_gen_power
                print 'ILP Gen:'
                print ILP_load_power
                for n in graph_des.nodes():
                    j = graph_des.nodes().index(n)
                    i = hviet.nodes().index(n)
                    print 'i'
                    print i
                    print 'j'
                    print j
                    print 'Number of loads'
                    print len(ILP_load_power)
                    print 'Number of Generators'
                    print len(ILP_gen_power)
                    if (j <len(ILP_gen_power)):
                        if (abs(ILP_gen_power[j]) < 0.1*abs(power[i])):
                            if n not in nodes_to_remove:
                                nodes_to_remove.append(n)
                    if (len(ILP_gen_power)<= j <(len(ILP_gen_power)+len(ILP_load_power))):
                        generators = len(ILP_gen_power)
                        if (abs(ILP_load_power[j-generators]) < 0.1*abs(power[i])):
                            if n not in nodes_to_remove:
                                nodes_to_remove.append(n)
                ####Add failed nodes to the initial failures if the power is zero:
                #
                print 'Total Power of each connected component:'
                print TotalPower
                if (TotalPower >= 0.0):
                    print 'TotalGenPower:'
                    print TotalGenPower
                    print 'TotalPower in Real Cascade:'
                    print TotalPower
                    print 'Size of this connected Max_nodes:'
                    print len(Max_nodes)
                    if (abs(TotalPower) <= abs(TotalGenPower)):
                        TotalPowerAllGraphs = TotalPower #+ TotalPowerAllGraphs #+ TotalPower 
                        TotalGenPowerAllGraphs = TotalGenPower #+ TotalGenPowerAllGraphs #+ TotalGenPower
                    elif(abs(TotalPower) > abs(TotalGenPower)):
                        print 'WHAAAAAAAT THE FUCKKKKKK!'
                        TotalPowerAllGraphs = TotalGenPower #+ TotalPowerAllGraphs
                        TotalGenPowerAllGraphs = TotalGenPower #+TotalGenPowerAllGraphs
                    #else:
                    #    TotalPowerAllGraphs = TotalPower_no_mon #+ TotalPowerAllGraphs
                    #    TotalGenPowerAllGraphs = TotalGenPower_no_mon #+ TotalGenPowerAllGraphs
        Max_flow = 0
        AbsFlows = []
        for i in range(0, len(flows)):
            AbsFlows.append(abs(flows[i]))
        if (len(AbsFlows) != 0):
            Max_flow = max(AbsFlows)
        print 'Max Flow is:'
        print Max_flow
        if  (Max_flow <= 1.02*(Thr)):
          cascade = 0
        else:
          cascade = 1
          Flow_Index = AbsFlows.index(Max_flow)
          thisEdge = flow_edges[Flow_Index]
          e1 = thisEdge[0]
          e2 = thisEdge[1]
          print 'Im removing this edge'
          print (e1, e2)
          edge = (e1, e2)
          if edge not in destroyed_edges:
              destroyed_edges.append(edge) 
          for m in range(0, len(link1)):
              if ((e1 == link1[m]) and (e2 == link2[m])) or ((e1 == link2[m]) and (e2 == link1[m])):
                  Index = m
          if edge not in destroyed_edges:
              destroyed_edges.append(edge)
              del link1[Index]
              del link2[Index]
              del linkNum[Index]
              del reactances[Index]
              times = times + 1
    ################################################################
    print 'Total Power of all connected components of the graphs:'
    print TotalPowerAllGraphs
    print 'FLOOOOOOOOOOOOOOOOOOOOOOOOWS:'
    print flows
    if (len(flows) != 0):
            print 'Maximum flow:'
            print max(flows)
    print 'Length Flows:'
    print len(flows)
    print 'Length link1:'
    print len(link1)
    print 'Number of nodes in graph_des'
    print len(Max_nodes)
    removed_g1_edges = destroyed_edges
    removed_g1 = nodes_to_remove
    removed_g2=init_removed_g2 
    return k, removed_g1_edges, removed_g1, removed_g2, TotalPowerAllGraphs
    #########################################################################################################################################
"""
"""
for j in range(0, repeat):
    for x in range(0,1):
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
                #if e not in Curr_Gray_Edges:
                del link1[rem]
                del link2[rem]
                del linkNum[rem]
                del reactances[rem]
                
                if (rem < len(link1_no_mon)):
                    if e not in Curr_Gray_Edges:
                        del link1_no_mon[rem]
                        del link2_no_mon[rem]
                        del reactances_no_mon[rem]
                        #if rem not in destroyed_edges_no_mon:
                        #    destroyed_edges_no_mon.append(rem)
                
                if rem not in removed_edges:
                    removed_edges.append(rem)
                        
        #########################################################################################################################################
        Hviet_Destroyed = nx.MultiGraph()
        Hviet_Destroyed= get_graph_from_destroyed_graph(hviet, destroyed_edges) #(graph_built, destroyed_edges)
        destroyed_edges_no_mon = []
        for e in destroyed_edges:
            if e not in destroyed_edges_no_mon:
                destroyed_edges_no_mon.append(e)
        
        for e in destroyed_edges:
            e1 = e[0]
            e2= e[1]
            for r in range(0, len(link1_no_mon)-1):
                if ((link1_no_mon[r] == e1) and (link2_no_mon[r] == e2)):
                    del link1_no_mon[r]
                    del link2_no_mon[r]
                    del reactances_no_mon[r]
        Hviet_Destroyed_no_mon = nx.MultiGraph()
        Hviet_Destroyed_no_mon = get_graph_from_destroyed_graph(hviet, destroyed_edges_no_mon)
        print 'Hviet Destroyed Nodes:'
        print len(Hviet_Destroyed.nodes())
        print 'Hviet Number of edges:'
        print len(Hviet_Destroyed.edges())
        #########################################################################################################################################
        #Here try to solve DC power flow equations for each connected component of the graph
        graphs = list(nx.connected_component_subgraphs(Hviet_Destroyed))
        graphs_no_mon = list(nx.connected_component_subgraphs(Hviet_Destroyed_no_mon))
        #print graphs
        ################################################
        Max_nodes = []
        flows = []
        flow_edges = []
        for g in graphs:#graphs_no_mon:
            graph_des = nx.MultiGraph()
            graph_des = Create_Weighted(g, link1, link2, reactances)
            Maximum = len(Max_nodes)+1
            #if (len(graph_des.nodes()) > Maximum):
            if (len(graph_des.nodes()) > 0) and (len(graph_des.nodes()) > Maximum ):#Maximum):
                Max_nodes = graph_des.nodes()
                [flows_no_mon, ILP_gen_power_no_mon, ILP_load_power_no_mon, cost_no_mon, TotalPower_no_mon] = optimal_Power_Control(hviet, graph_des, nodes, power, link1_no_mon, link2_no_mon, reactances_no_mon, linkNum, Thr) #optimal_DC_Flow_Cascade
                #Add the controller's solution to the powers
                if (Dest_perc < 1.0) and (len(ILP_gen_power_no_mon) != 0):
                    for i in range(0, len(power)):
                        if (len(hviet.nodes()) > 10): 
                            if (i < 113) and (i not in Curr_Gray_Nodes):
                                power[i] = ILP_gen_power_no_mon[i]
                            if (113 <= i < 210) and (i not in Curr_Gray_Nodes):
                                power[i] = ILP_load_power_no_mon[i-113]
                        else:
                            if (i < 1) and (i not in Curr_Gray_Nodes):
                                power[i] = ILP_gen_power_no_mon[i]
                            if (1 <= i < 3) and (i not in Curr_Gray_Nodes):
                                power[i] = ILP_load_power_no_mon[i-1]
                    
        ########################################################################################################################################
        #######SOLVE DC POWER FLOW MODEL:
        Max_nodes = []
        flows = []
        flows_edges = []
        for g in graphs:
            graph_des = nx.MultiGraph()
            graph_des = Create_Weighted(g, link1, link2, reactances)
            Maximum = len(Max_nodes) + 1
            #if (len(graph_des.nodes()) > Maximum):
            if (len(graph_des.nodes()) > 0) and (len(graph_des.nodes()) > Maximum ):#Maximum):
                Max_nodes = graph_des.nodes()
                #Now solve the DC flow to see any cascade can happen!
                #[flow_edges, flows, ILP_gen_power, ILP_load_power, cost, TotalPower, TotalGenPower] = optimal_Power_Control_discrete(hviet, graph_des, nodes, power, link1, link2, reactances, linkNum, Thr) #optimal_DC_
                [flow_edges, flows, ILP_gen_power, ILP_load_power, cost, TotalPower, TotalGenPower]= optimal_Find_Flow(hviet, graph_des, nodes, power, link1, link2, reactances, linkNum, Thr)            
        #[flows_no_mon, ILP_gen_power_no_mon, ILP_load_power_no_mon, cost_no_mon, TotalPower_no_mon] = optimal_DC_Flow_Cascade(nodes, power, link1_no_mon, link2_no_mon, reactances_no_mon, linkNum, Thr)
        #########################################################################################################################################
        #############Remove edges which are overloaded:        
        loop =1
        print ' Length Flows:'
        print len(flows)
        print 'Length link1:'
        print len(link1)
        print 'FLOOOOOOOOOOOOOOOOOOOOOOOOWS:'
        print flows
        print 'Length Flows:'
        print len(flows)
        print 'Length link1:'
        print len(link1)
        print 'Number of nodes in graph_des'
        print Max_nodes
        times = 1
        ##########################################################################################################################################
        while (loop ==1):
            f =0
            Max_Flow = 0
            if (len(flows) != 0):
                print 'Flooooooooooooooooooooooooooows:'
                print flows
                print 'Maximum Flowwwww:'
                AbsFlows = []
                for i in range(0, len(flows)):
                    AbsFlows.append(abs(flows[i]))
                print 'AbsFlows:'
                print AbsFlows
                Max_Flow = max(AbsFlows)
                print Max_Flow
                if (Max_Flow <= 1.02*(Thr)):
                    loop = 0
                else:
                    loop = 2
                    Flow_Index = AbsFlows.index(Max_Flow)
                    thisEdge = flow_edges[f]
                    e1 = thisEdge[0]
                    e2 = thisEdge[1]
                    print 'Im removing this edge'
                    print (e1, e2)
                    edge = (e1, e2)
                    for m in range(0, len(link1)):
                        if ((e1 == link1[m]) and(e2 == link2[m])) or ((e1 == link2[m]) and (e2 == link1[m])):
                            Index = m
            else:
                loop = 0
            print 'LOOOOOOOOOOOOOPPPP:'
            print loop
            #del reactances[f]
            if (loop == 2):
                if edge not in destroyed_edges_no_mon:
                    destroyed_edges_no_mon.append(edge)
                if edge not in destroyed_edges:
                    destroyed_edges.append(edge)
                #########################################################################################################################################
                Hviet_Destroyed = nx.MultiGraph()
                Hviet_Destroyed= get_graph_from_destroyed_graph(hviet, destroyed_edges) #(graph_built, destroyed_edges
                Hviet_Destroyed_no_mon = nx.MultiGraph()
                Hviet_Destroyed_no_mon = get_graph_from_destroyed_graph(hviet, destroyed_edges_no_mon) #(graph_built, destroyed_edges

                del link1[Index]
                del link2[Index]
                del linkNum[Index]
                del flows[Flow_Index]
                del flow_edges[Flow_Index]
                #del Original_flows[f]
                del reactances[Index]
                times = times +1
                if (Index < len(link1_no_mon)):
                    if edge not in Curr_Gray_Edges:
                        del link1_no_mon[Index]
                        del link2_no_mon[Index]
                        del reactances_no_mon[Index]

            print 'REPEAAAAAAAAAAAAAAAAAAAAAAATTT'
            graphs = list(nx.connected_component_subgraphs(Hviet_Destroyed))
            print 'Connected Components of the Destroyed Graph:'
            print graphs
            #######################################################################################################################################
            ################################################
            if (Dest_perc ==0):
                graphs_no_mon = list(nx.connected_component_subgraphs(Hviet_Destroyed_no_mon))            
                Max_nodes = []
                flows = []
                flow_edges = []
                TotalPower_no_mon2 = 0
                #power, nodes_here, linkNum_here, link1_here, link2_here, reactances_here = read_hviet()
                for g in graphs:#graphs_no_mon:
                    graph_des = nx.MultiGraph()
                    graph_des = Create_Weighted(g, link1, link2, reactances)
                    Maximum = len(Max_nodes)+1
                    #if (len(graph_des.nodes()) > Maximum):
                    if (len(graph_des.nodes()) > 0) and (len(graph_des.nodes()) > Maximum ):#Maximum):
                        Max_nodes = graph_des.nodes()
                        [flows_no_mon, ILP_gen_power_no_mon, ILP_load_power_no_mon, cost_no_mon, TotalPower_no_mon2] = optimal_Power_Control(hviet, graph_des, nodes, Original_power, link1_no_mon, link2_no_mon, reactances_no_mon, linkNum, Thr) #optimal_DC_Flow_Cascade
                        #Add the controller's solution to the powers
                        if (Dest_perc < 1.0) and (len(ILP_gen_power_no_mon) != 0):
                            for i in range(0, len(power)):

                                if (len(hviet.nodes()) > 10):
                                    if (i < 113) and (i not in Curr_Gray_Nodes):
                                        power[i] = ILP_gen_power_no_mon[i]
                                    if (113 <= i < 210) and (i not in Curr_Gray_Nodes):
                                        power[i] = ILP_load_power_no_mon[i-113]
                                else:
                                    if (i < 1) and (i not in Curr_Gray_Nodes):
                                        power[i] = ILP_gen_power_no_mon[i]
                                    if (1 <= i < 3) and (i not in Curr_Gray_Nodes):
                                        power[i] = ILP_load_power_no_mon[i-1]

                            #if (i < 113) and (i not in Curr_Gray_Nodes):
                            #    power[i] = ILP_gen_power_no_mon[i]
                            #if (113 <= i < 210) and (i not in Curr_Gray_Nodes):
                            #    power[i] = ILP_load_power_no_mon[i-113]
            
            ########################################################################################################################################
            #######################################################################################################################################
            TotalPowerAllGraphs= []
            TotalPowerAllGraphs = 0
            TotalGenPowerAllGraphs = []
            TotalGenPowerAllGraphs = 0
            Max_nodes = []
            for g in graphs:
                #Function to find the optimal flow
                #print 'Number of Edges of Subgraph g:'
                #print len(g.edges())
                #print 'Number of Nodes in Subgraph g:'
                #print len(g.nodes())
                #print 'Weight of subgraph g:'
                graph_des = nx.Graph()
                graph_des = Create_Weighted(g, link1, link2, reactances)
                #for e in g.edges():#raph_des.edges():
                #    e1 = e[0]
                #    e2 = e[1]
                #    w = g[e1][e2]['weight'] #graph_des[e1][e2]['weight']
                #    print w
                #Max_nodes = []
                Maximum = len(Max_nodes) +1
                if (len(graph_des.nodes()) > 0) and (len(graph_des.nodes()) > Maximum ):#Maximum):
                    Max_nodes = graph_des.nodes()
                    flows = []
                    flow_edges = []
                    #[flow_edges, flows, ILP_gen_power, ILP_load_power, cost, TotalPower, TotalGenPower] = optimal_Power_Control_discrete(hviet, graph_des, nodes, power, link1, link2, reactances, linkNum, Thr) #optimal_DC_
                    [flow_edges, flows, ILP_gen_power, ILP_load_power, cost, TotalPower, TotalGenPower]= optimal_Find_Flow(hviet, graph_des, nodes, power, link1, link2, reactances, linkNum, Thr)
                    print 'Total Power of each connected component:'
                    print TotalPower
                    if (Dest_perc >= 0.0):
                        print 'TotalGenPower:'
                        print TotalGenPower
                        print 'TotalPower in Real Cascade:'
                        print TotalPower
                        print 'Size of this connected Max_nodes:'
                        print len(Max_nodes)
                        if (abs(TotalPower) <= abs(TotalGenPower)):
                            TotalPowerAllGraphs = TotalPower #+ TotalPowerAllGraphs + TotalPower 
                            TotalGenPowerAllGraphs = TotalGenPower #+ TotalGenPowerAllGraphs + TotalGenPower
                        elif(abs(TotalPower) > abs(TotalGenPower)):
                            print 'WHAAAAAAAT THE FUCKKKKKK!'
                            TotalPowerAllGraphs = TotalGenPower #+ TotalPowerAllGraphs
                            TotalGenPowerAllGraphs = TotalGenPower #+TotalGenPowerAllGraphs
                    else:
                        TotalPowerAllGraphs = TotalPower_no_mon #+ TotalPowerAllGraphs
                        TotalGenPowerAllGraphs = TotalGenPower_no_mon #+ TotalGenPowerAllGraphs
            print 'Total Power of all connected components of the graphs:'
            print TotalPowerAllGraphs
            print 'FLOOOOOOOOOOOOOOOOOOOOOOOOWS:'
            print flows
            if (len(flows) != 0):
                print 'Maximum flow:'
                print max(flows)
            print 'Length Flows:'
            print len(flows)
            print 'Length link1:'
            print len(link1)
            print 'Number of nodes in graph_des'
            print len(Max_nodes)
            ##if (len(Max_nodes) == 0):
            ##    TotalPowerAllGraphs = 0
            ##    TotalGenPowerAllGraphs = 0
            #########################################################################################################################################
            #Original_flows = flows
            #[flows, ILP_gen_power, ILP_load_power, cost, TotalPower] = optimal_Find_Flow(graph_des, nodes, power, link1, link2, reactances, linkNum, Thr)# optimal_DC_Flow_Cascade()
            #Original_flows = flows
            if (len(flows) != 0):
                if (abs(max(flows)) <= 1.02*(Thr)):
                    loop = 0
            if (loop ==2):
                loop =1
                #loop =0
            #if (Dest_perc == 0):
            #    loop = 0
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
print Thr

print 'Number Curr_Gray_Edges:'
print len(Curr_Gray_Edges)
print 'Original Gray Edges:'
print len(Original_Gray_Edges)
print 'Number Curr Gray Nodes:'
print len(Curr_Gray_Nodes)
print 'Cycles:'
print NumberofCycles
"""
