#!/usr/bin/env python
# coding: utf-8
# created by hevlhayt@foxmail.com 
# Date: 2016/1/15 
# Time: 9:28
#
import random
#Diman Added 
import os
from my_lib_power import *
#Diman Added
import networkx as nx
#from src.cascade.graph import create_graph
from graph import create_graph
from False_Control import *
import matplotlib.pyplot as plt


def cascading_failures(G1, G2, init_nodes):
    G1.remove_nodes_from(init_nodes)
    na = len(init_nodes)
    noi = 0
    while na > 0:

        largests_a = sorted(nx.connected_components(G1), key=len, reverse=True)
        if len(largests_a) == 0:
            break
        largest_a = largests_a[0]

        remove_nodes_a = set([])
        remove_nodes_b = set([])
        for g1node in G1.nodes_iter():
            if g1node not in largest_a:
                remove_nodes_a.add(g1node)
        G1.remove_nodes_from(remove_nodes_a)

        for g2node in G2.nodes_iter():
            if g2node not in largest_a:
                remove_nodes_b.add(g2node)

        G2.remove_nodes_from(remove_nodes_b)

        remove_nodes_a.clear()
        remove_nodes_b.clear()

        # print "remove a %s----remove b %s" % (na ,nb)
        # print "ba1 len: %s" % (len(ba1))
        # print "---"

        largests_b = sorted(nx.connected_components(G2), key=len, reverse=True)
        if len(largests_b) == 0:
            break
        largest_b = largests_b[0]

        for g2node in G2.nodes_iter():
            if g2node not in largest_b:
                remove_nodes_b.add(g2node)

        G2.remove_nodes_from(remove_nodes_b)

        for g1node in G1.nodes_iter():
            if g1node not in largest_b:
                remove_nodes_a.add(g1node)

        G1.remove_nodes_from(remove_nodes_a)
        na = len(remove_nodes_a)
        remove_nodes_a.clear()
        remove_nodes_b.clear()
        if na == 0:
            break
        noi += 1
    return noi

def cascading_failures_ping_pong(G1, G2, init_nodes,  h_inter, g_inter ):
    G1.remove_nodes_from(init_nodes)
    na = len(init_nodes)
    noi = 0
    g1_dest = 0
    g2_dest = 0
    removed_g1 = []
    removed_g2 = []
    des_g1_nodes = []
    des_g2_nodes = []
    remove_nodes_a = set([])
    remove_nodes_b = set([])
    #while na > 0:
    for g1node in init_nodes:
        #g1node = random.randint(0, len(G1.nodes())-1)
        na = na - 1
        print 'Selected Node in g1:'
        print g1node
        remove_nodes_a.add(g1node)
        if g1node not in des_g1_nodes:
          des_g1_nodes.append(g1node)
        #g1_dest = g1_dest + 1
        while (len(removed_g1) != len(des_g1_nodes)):
          #print 'removed_g1:'
          #print removed_g1
          #print des_g1_nodes
          for n_g1 in des_g1_nodes:
            if n_g1 not in removed_g1:
              removed_g1.append(n_g1)
              if h_inter.has_key(n_g1):
                tmp = h_inter.get(n_g1)
                print 'garr inter'
                print tmp
                g1_dest = g1_dest + 1
                for n in tmp:
                  if n not in des_g2_nodes:
                    des_g2_nodes.append(n)
                    g2_dest = g2_dest + 1
                    if g_inter.has_key(n):
                      g1_n = g_inter.get(n)
                      for g1 in g1_n:
                        if g1 not in des_g1_nodes:
                          des_g1_nodes.append(g1)
    return len(removed_g1), len(des_g2_nodes)
##########################################	
def add_more_edges_random(G, num_edge, size):
    k = 0
    while k < num_edge:
        a, b = random.randint(0, size), random.randint(0, size)
        if not G.has_edge(a, b):
            G.add_edge(a, b)
            k += 1

if __name__ == '__main__':
    num_nodes = 1000

    x = []
    y = []
    y2 = []
    y3 = []
    y4 = []
    g1_failed = []
    g2_failed = []

    ####Diman added for hviet and garr:
    """
    hpath = os.path.abspath('../../')+'/data/PIData/hviet'
    ##hpath = os.path.abspath('../../')+'/data/PIData/hviet_test'
    hcpath = os.path.abspath('../../')+'/data/PIData/hviet_coordinates'
    Linkpath = os.path.abspath('../../')+'/data/HVIET/reactances.txt'
    ##Linkpath = os.path.abspath('../../')+'/data/HVIET/test2_reactances.txt'
    gpath = os.path.abspath('../../')+'/data/PIData/garr'
    ##gpath = os.path.abspath('../../')+'/data/PIData/garr_test'
    gcpath = os.path.abspath('../../')+'/data/PIData/garr_coordinates'
    f_hviet = open(hpath, 'r')
    f_hvietc = open(hcpath, 'r')
    f_garr = open(gpath, 'r')
    f_garrc = open(gcpath, 'r')
    Ghviet = nx.Graph() #MultiGraph() #nx.Graph()
    Ggarr = nx.Graph() #MultiGraph() #nx.Graph()
    num_nodes = len(Ghviet.nodes())
    print 'Number of Nodes:'
    print num_nodes
    """
    italian = create_italian()
    #power, nodes, linkNum, link1, link2, reactances = read_hviet()
    hviet = italian[0]
    garr = italian[1]
    h_inter = italian[2]
    g_inter = italian[3]
    num_nodes = len(hviet.nodes())
    num_edges = len(hviet.edges())
    print 'Number of Nodes:'
    print num_nodes
    ####Diman added for hviet and garr
    N= 50.0 # 50 bood
    i = 0
    for g in range(1):#51
        i = 1
        print i
        sum = 0
        sum2 = 0
        PowerDelivered = 0
        sum_edges = 0
        it = 1 #30
        for j in range(it):
            ####Diman added for hviet and garr:
            italian = create_italian()
            #italian = create_italian_random()
            #italian = create_er_random()
            #italian  = create_ba_random()
            hviet = italian[0]
            garr = italian[1]
            h_inter = italian[2]
            print 'H_INTER:'
            print h_inter
            print 'G_INTER:'
            print g_inter
            g_inter = italian[3]
            num_nodes = len(hviet.nodes())
            num_edges = len(hviet.edges())
            num_nodes2 = len(garr.nodes())
            #print 'Number of Nodes:'
            #print num_nodes
            
            ####Diman added for hviet and garr
            ##er1 = create_graph('er', num_nodes, 4)
            ##er2 = create_graph('er', num_nodes, 4)
            remove_nodes = set([])
            remove_edges = set([])
            k = 0
            """
            while len(remove_edges) < num_edges * i /N:
                r = random.randint(0, num_edges-1)
                #r = random.randint(0, len(link1)-1)
                if r not in remove_edges:
                    remove_edges.add(r)
                    k += 1
            ########################################
            while len(remove_nodes) < num_nodes * i / N:
                r = random.randint(0, num_nodes)
                if r not in remove_nodes:
                    remove_nodes.add(r)
                    k += 1
            """
            ##cascading_failures(er1, er2, remove_nodes)
            #cascading_failures(hviet, garr, remove_nodes)
            ###init_removed_g1, init_removed_g2= cascading_failures_ping_pong(hviet, garr, remove_nodes, h_inter, g_inter)
            init_removed_g1_edges = remove_edges
            removed_g1= []
            removed_g2= []
            init_removed_g1 = []
            init_removed_g2 = []
            TotalPowerAllGraphs = 0
            k, removed_g1_edges, removed_g1_nodes, removed_g2, TotalPowerAllGraphs= Let_it_Cascade(hviet, garr, init_removed_g1_edges, init_removed_g1, init_removed_g2, h_inter, g_inter, i, N, j)
            num_removed_g1_edges = len(removed_g1_edges)
            #while (len(init_removed_g1_nodes) != len(init_removed_g1)):
            #    removed_g1_edges, removed_g1_nodes, removed_g2= Let_it_Cascade(hviet, garr,init_removed_g1_edges, init_removed_g1, init_removed_g2, h_inter, g_inter)
            init_removed_g1, init_removed_g2= cascading_failures_ping_pong(hviet, garr, removed_g1_nodes, h_inter, g_inter)
            print 'Leng of initial nodes:'
            print len(remove_nodes)
            ##sum += len(er1)
            ##sum2 += len(er2)
            print 'removed g1:'
            print removed_g1
            print 'removed_g2:'
            print removed_g2
            sum_edges += (num_removed_g1_edges)
            sum += (init_removed_g1)#(removed_g1) #len(hviet)
            sum2 += (init_removed_g2)#(removed_g2) #len(garr)
            PowerDelivered += (TotalPowerAllGraphs)
            #Diman
            print 'Sum:'
            print sum
            print 'Hviet and Garr nodes, remove nodes:'
            print len(hviet.nodes()), len(garr.nodes()), remove_nodes
            #Diman
        g1_failed.append(init_removed_g1 / float(num_nodes))
        g2_failed.append(init_removed_g2 / float(num_nodes2))
        y.append(sum / float(num_nodes) / it)
        y2.append(sum2 / float(num_nodes2) / it)
        y3.append(sum_edges /float(num_edges) /it)
        y4.append((PowerDelivered) /float(31.8172) /it)
        x.append(1-i/50.0)
    print 'Printing x:'
    print x
    print 'Printing y: Percentage of hviet uncontrollable nodes'
    print y
    print 'Printing y2 percentage of garr lost power nodes:'
    print y2
    print 'Printing y3: Number of failed edges:'
    print y3
    print 'Printing y4: Delivered Power in power grid:'
    print y4
    print 'Printing G1 percentage of failed :'
    print g1_failed
    print 'Printing G2 Percentage of failed:'
    print g2_failed

    #plt.plot(x, y, 'o')
    #plt.show()



