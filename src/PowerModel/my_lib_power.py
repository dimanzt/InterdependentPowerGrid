user_name='Diman'

import networkx as nx
import pydot
import numpy as np
from numpy.linalg import svd
import matplotlib.pyplot as plt
import math
import scipy
from scipy import linalg, matrix
from scipy.integrate import dblquad
from scipy.stats import multivariate_normal
from matplotlib.mlab import bivariate_normal
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FixedLocator, FormatStrFormatter
from copy import deepcopy
import random
from heapq import heappush, heappop
from itertools import count

from operator import itemgetter
#from find_max_value_of_split import *

import os
import shutil
import re
import math
import collections
import time

###########################################################################
def create_italian():

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

    """
    link1 = []
    link2 =[]
    linkNum = []
    reactances = []
    with open(Linkpath, 'r') as links:

        for line in links:
            #list_line = re.findall(r"[\d.\d+']+", line)
            #.\d+[Ee][+\-]
            list_line = re.findall(r"[\d.\d+']+", line)
            linkNum.append(float(list_line[0])) #appends first column
            link1.append(float(list_line[1])) #append second column
            link2.append(float(list_line[2])) # append the third column
            reactances.append(float(list_line[3])) #append the fourth column

    
    f = open(hpath, "w")
    for i in range(0, len(link1)):
        f.write(str(int(link1[i]))+","+str(int(link2[i]))+ "\n" )
    f.close()
    #f = open(gpath, "w")
    #for i in range(0, len(Load_P)):
    #    f.write(str(Load_P[i])+ "\n" )
    #f.close()
    """
    hc_dict = {}
    loc = ''
    node = ''
    for l in f_hvietc:
        tmp = l.rstrip('\n').split(',')
        #Diman added this line and commented the next 6 lines:
        hc_dict.setdefault(int(tmp[0]), [float(tmp[1]), float(tmp[2])])
        #if tmp[1]+tmp[2] != loc:
        #    node = tmp[0]
        #    loc = tmp[1]+tmp[2]
        #    hc_dict.setdefault(node, [node, float(tmp[1]), float(tmp[2])])
        #else:
        #    hc_dict.setdefault(tmp[0], [node, float(tmp[1]), float(tmp[2])])

    # print hc_dict
    #Diman ADDED to make a weighted graph:
    link1 = []
    link2 = []
    linkNum = []
    reactances = []
    # .4g
    with open(Linkpath, 'r') as links:

        for line in links:
            #list_line = re.findall(r"[\d.\d+']+", line)
            #.\d+[Ee][+\-]
            list_line = re.findall(r"[\d.\d+']+", line)
            linkNum.append(float(list_line[0])) #appends first column
            link1.append(float(list_line[1])) #append second column
            link2.append(float(list_line[2])) # append the third column
            reactances.append(float(list_line[3])) #append the fourth column      
    ##CREATE a Weighted Graph
    m = 0
    ListofEdges = []
    for l in f_hviet:
        nodes = l.rstrip('\n').split(',')
        #Ghviet.add_edge(hc_dict.get(nodes[0])[0], hc_dict.get(nodes[1])[0])
        e1= link1[m]
        e2= link2[m]
        e = (e1, e2)
        if e not in ListofEdges:
            ListofEdges.append(e)
        if e in ListofEdges:
            w = reactances[m]/2
        #else:
        w = reactances[m]
        Ghviet.add_edge(int(nodes[0]), int(nodes[1]),weight=w) #add_weighted_edges_from() #add_edge
        #print Ghviet[e1][e2]['weight']
        m = m + 1
    gc_dict = {}
    for l in f_garrc:
        tmp = l.rstrip('\n').split(',')
        gc_dict.setdefault(int(tmp[0]), [float(tmp[1]), float(tmp[2])])

    for l in f_garr:
        nodes = l.rstrip('\n').split(',')
        Ggarr.add_edge(int(nodes[0]), int(nodes[1]))

    # nx.draw(Ghviet)
    # nx.draw(Ggarr)
    # plt.show()

    h_inter = {}
    g_inter = {}
    i = 0
    for net in Ghviet: #Ggarr:
        mindist = 1000000.0
        #print net
        inter = ''
        for node in Ggarr: #Ghviet:
            #x1 = hc_dict.get(node)[1]
            #x1 = hc_dict.get(node)[0]
            x1 = gc_dict.get(node)[0]
            #y1 = hc_dict.get(node)[2]
            #y1 = hc_dict.get(node)[1]
            y1 = gc_dict.get(node)[1]
            #x2 = gc_dict.get(net)[0]
            x2 = hc_dict.get(net)[0]
            #y2 = gc_dict.get(net)[1]
            y2 = hc_dict.get(net)[1]
            dist = (x1-x2)*(x1-x2)+(y1-y2)*(y1-y2)
            if mindist > dist:
                mindist = dist
                inter = node

        # print 'garr node: %s  hviet node: %s  min dist: %s (%s, %s)-(%s, %s)' % \
        #       (net, inter, mindist, gc_dict.get(net)[0], gc_dict.get(net)[1],
        #           hc_dict.get(inter)[1], hc_dict.get(inter)[2])

        #g_inter.setdefault(net, [inter])
        h_inter.setdefault(net, [inter])
        #if not h_inter.has_key(inter):
        if not g_inter.has_key(inter):
            #h_inter.setdefault(inter, [net])
            g_inter.setdefault(inter, [net])
        else:
            tmp = g_inter.get(inter) #h_inter.get(inter)
            #h_inter.setdefault(inter, tmp.append(net))
            g_inter.setdefault(inter, tmp.append(net))

    print 'hviet nodes: '+str(len(Ghviet.nodes()))
    print Ghviet.nodes()
    print 'hviet edges: '+str(len(Ghviet.edges()))
    print Ghviet.edges()
    #for e in Ghviet.edges():
    #    e1 = e[0]
    #    e2 = e[1]
    #    w = Ghviet[e1][e2]['weight']
    #    print 'weight of edge:'
    #    print Ghviet[e1][e2]['weight']
    #print 'hviet edges: '+str(Ghviet.size())
    print 'garr nodes: '+str(len(Ggarr.nodes()))
    print Ggarr.nodes()
    print 'garr edges: '+str(len(Ggarr.edges()))
    print Ggarr.edges()
    #print 'garr edges: '+str(Ggarr.size())
    #print 'HVIET:'
    #print Ghviet.edge
    #print 'GARR:'
    #print Ggarr.edge
    print 'H_INTER:'
    print 'HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHaaaaaaaaaaaaa'
    print h_inter
    print 'G_INTER:'
    print g_inter
    ###############################
    for i in Ghviet.nodes():
        if 'Longitude' not in Ghviet.node[i]:
            Ghviet.node[i]['Longitude']= hc_dict.get(i)[1]#random.randint(0,300)
        if 'Latitude' not in Ghviet.node[i]:
            Ghviet.node[i]['Latitude']= hc_dict.get(i)[0]#random.randint(0,300)
    ### Ggarr:
    for i in Ggarr.nodes():
        if 'Longitude' not in Ggarr.node[i]:
            Ggarr.node[i]['Longitude']= gc_dict.get(i)[1]#random.randint(0,300)
        if 'Latitude' not in Ggarr.node[i]:
            Ggarr.node[i]['Latitude']= gc_dict.get(i)[0]#random.randint(0,300)
    ################################
    nx.write_gml(Ghviet,"hviet.gml")
    nx.write_gml(Ggarr,"garr.gml")
    f_hviet.close()
    f_hvietc.close()
    f_garr.close()
    f_garrc.close()
    return [Ghviet, Ggarr, h_inter, g_inter]

def read_hviet():

    Powpath = os.path.abspath('../../')+'/data/HVIET/ne.txt'
    ##Powpath = os.path.abspath('../../')+'/data/HVIET/power_test2.txt'
    Linkpath = os.path.abspath('../../')+'/data/HVIET/reactances.txt'
    ##Linkpath = os.path.abspath('../../')+'/data/HVIET/test2_reactances.txt'
    #hcpath = os.path.abspath('../../')+'/data/PIData/hviet_coordinates'
    hcpath = os.path.abspath('../../')+'/data/PIData/hviet_coordinates'

    #gpath = os.path.abspath('../../')+'/data/P/garr'
    #gcpath = os.path.abspath('../../')+'/data/PIData/garr_coordinates'
    p_hviet = open(Powpath, 'r')
    L_hviet = open(Linkpath, 'r')
    f_hvietc = open(hcpath, 'r')
    #f_garr = open(gpath, 'r')
    #f_garrc = open(gcpath, 'r')
    Ghviet = nx.Graph()
    #Ggarr = nx.Graph()
    #f=open("input.txt",'r')
    x=p_hviet.readlines()
    nodes=[]
    power=[]
    import re
    
    with open(Powpath, 'r') as f:
        for line in f:
            #list_line = re.findall(r"[\d.\e+']+", line)
            list_line = re.findall(r"[-\d.\d+']+", line)
            #list_line = re.findall(r"-?\d\.?\d*[Ee][+\-]?\d+", line)
            nodes.append(float(list_line[0])) #appends first column
            power.append(float(list_line[1])) #appends second column
    print 'Nodes:'
    print nodes
    print 'Power:'
    print power
    link1 = []
    link2 = []
    linkNum = []
    reactances = []
    # .4g
    
    with open(Linkpath, 'r') as links:
        
        for line in links:
            #list_line = re.findall(r"[\d.\d+']+", line)
            #.\d+[Ee][+\-]
            list_line = re.findall(r"[\d.\d+']+", line)
            linkNum.append(float(list_line[0])) #appends first column
            link1.append(float(list_line[1])) #append second column
            link2.append(float(list_line[2])) # append the third column
            reactances.append(float(list_line[3])) #append the fourth column

    '''
    #Open the file

    verts = []
    #verts=[float(e) for e in verts if e]
    #values = []

    f = open(Linkpath,'r')
    #first, extract all of the sim values
    val = []
    for line in f:
        lineval = line.split()
        print 'Dimaaan:'
        print lineval
        val.append(lineval)
    print val
    #val = map(float,val)
    maxv = max(val)
    minv = min(val)
    setrange = float(maxv) - float(minv)
        
        
    for line in f:
        lines = f.readline() 
        #values = ([c for c in lines if c in '-1234567890.'])
        if line.startswith("v "): #Go through file line by line
            read = lines.strip(' v\n').split(',') #remove the v,split@, 
            #read = values.split(',')
            #loop over all stuff in read, remove non-numerics
            print 'read:'
            print read
            for d in read:
                d= d.strip('-').split(' ')
                #print("d:", (d))
                print 'd:'
                print d
                for n in d:
                    n = n.strip('-')
                    verts = verts.append(float(n[0]))
                    #verts = verts.append(float(n[2]))
                    #verts = verts.append(float(n[3]))
                    #print("vertsloops", d[0])
                    print 'vertsloops'
                    print d[0]
                print 'read1'
                print read[0]
                print read
                print 'oo1verts'
                print verts
                #print("read1", read[0])
                #print(read)
                #print("oo1verts", verts)
    '''
    #print 'LinkNumber:'
    #print linkNum
    #print 'Links:'
    #print link1
    #print link2
    #print 'Reactances:'
    #print reactances
    return power, nodes, linkNum, link1, link2, reactances
##########################################################
#[non_cont_g_nodes, non_cont_g_edges, des_garr_nodes, des_garr_edges] = Destroy_Monitors(hviet, garr, h_inter, g_inter, Dest_perc)
def Destroy_Monitors(hviet, garr, h_inter, g_inter, Dest_perc):
    #Outputs 
    non_cont_h_nodes = []
    non_cont_h_edges = []
    des_garr_nodes = []
    des_garr_edges = []
    Destroyed = 0 
    percentage = float(float(Destroyed) / float(len(garr.nodes())))
    while (percentage < Dest_perc):
        destroy_node = random.randint(0, len(garr.nodes())-1)
        if destroy_node not in des_garr_nodes:
            des_garr_nodes.append(destroy_node)
            Destroyed = Destroyed + 1
            percentage = float(float(Destroyed) / float(len(garr.nodes())))
            print 'Percentage:'
            print percentage

    for n in des_garr_nodes:
        print 'Destroyed garr node:'
        print n
        if g_inter.has_key(n):
            #h_inter.setdefault(inter, [net])
            tmp = g_inter.get(n)
            print 'garr inter'
            print tmp
            for h_nodes in tmp:
                if h_nodes not in non_cont_h_nodes:
                    non_cont_h_nodes.append(h_nodes)
            #g_inter.setdefault(inter, tmp.append(net))
        #for g in h_inter

    for e in hviet.edges():
        e1 = e[0]
        e2 = e[1]
        if (e1 in non_cont_h_nodes) and (e2 in non_cont_h_nodes):
            non_cont_h_edges.append(e) 
        
    print 'non controllable nodes in hviet:'
    print non_cont_h_nodes
    print 'non controllable edges in hviet:'
    print non_cont_h_edges
    print 'Destroyed garr nodes:'
    print des_garr_nodes
    return non_cont_h_nodes, non_cont_h_edges, des_garr_nodes, des_garr_edges
##########################################################################
def No_Power_Monitors(hviet, garr, h_inter, g_inter, Zero_Pow_nodes):
    #Outputs
    non_cont_h_nodes = []
    non_cont_h_edges = []
    des_garr_nodes = []
    des_garr_edges = []
    Destroyed = 0
    for n in Zero_Pow_nodes:
        if h_inter.has_key(n):
            tmp = h_inter.get(n)
            for g_nodes in tmp:
                if g_nodes not in des_garr_nodes:
                    des_garr_nodes.append(g_nodes)
    #######################################################################
    for n in des_garr_nodes:
        print 'Destroyed garr node:'
        print n
        if g_inter.has_key(n):
            #h_inter.setdefault(inter, [net])
            tmp = g_inter.get(n)
            print 'garr inter'
            print tmp
            for h_nodes in tmp:
                if h_nodes not in non_cont_h_nodes:
                    non_cont_h_nodes.append(h_nodes)
            #g_inter.setdefault(inter, tmp.append(net))
        #for g in h_inter

    for e in hviet.edges():
        e1 = e[0]
        e2 = e[1]
        if (e1 in non_cont_h_nodes) and (e2 in non_cont_h_nodes):
            non_cont_h_edges.append(e)

    print 'non controllable nodes in hviet:'
    print non_cont_h_nodes
    print 'non controllable edges in hviet:'
    print non_cont_h_edges
    print 'Destroyed garr nodes:'
    print des_garr_nodes
    return non_cont_h_nodes, non_cont_h_edges, des_garr_nodes, des_garr_edges
######################################################################### 
#NumberofCycles = Count_Cycles(non_cont_h_nodes, non_cont_h_edges, hviet)
def Count_Cycles(non_cont_h_nodes, non_cont_h_edges, hviet):
    Cycles = 0
    Curr_Gray_Edges = []
    GrayEdges = []
    Curr_Gray_Nodes = []
    gray = []
    SingleEdgeIndex = []
    for e in non_cont_h_edges:
        Curr_Gray_Edges.append(e)
        #GrayEdges.append(0)
        gray.append(1)
    for n in non_cont_h_nodes:
        Curr_Gray_Nodes.append(n)
    ##########################
    while (len(Curr_Gray_Edges) != 0):
        GrayEdges = []
        i = -1
        for m in Curr_Gray_Nodes:
            i = i + 1
            GrayEdges.append(0)
            #gray.append(1)
            for k in range(0, len(Curr_Gray_Edges)):
                e1 = Curr_Gray_Edges[k][0]
                e2 = Curr_Gray_Edges[k][1]
                if (e1 == m) or (e2 == m):
                    GrayEdges[i] = GrayEdges[i] + 1
                    #print 'm'
                    #print m 
                    SingleEdgeIndex = k
            if (GrayEdges[i] == 1):
                Curr_Gray_Nodes.remove(m)
                gray[SingleEdgeIndex] = 0
                Curr_Gray_Edges.remove(Curr_Gray_Edges[SingleEdgeIndex])
        if(len(Curr_Gray_Edges) != 0):
            Cycles = Cycles + 1
            Curr_Gray_Edges.remove(Curr_Gray_Edges[0])
    ##########################
    return Cycles, Curr_Gray_Edges, Curr_Gray_Nodes
#############################################################################
#Function to destroy the graph:
def get_graph_from_destroyed_graph(H, destroyed_edges):
    new_graph=nx.Graph(H)#MultiGraph(H)
    edges_to_remove=[]
    nodes_to_remove=[]
    print 'Number of edges to be removed:'
    print len(destroyed_edges)
    for edge in new_graph.edges():
        source=edge[0]
        target=edge[1]
        #weight =edge[2]
        if new_graph.has_edge(source,target):
            #keydict=H[source][target]
            arc = (source, target)
            arc_reverse = (target, source)
            if arc in destroyed_edges or arc_reverse in destroyed_edges:
                edges_to_remove.append(arc)
            """
            #for k in keydict:
                #if H[source][target][k]['type']!='green' and H[source][target][k]['status']=='destroyed':
                arc=(source,target)
                my_arc = (source, target, k)
                arc_reverse=(target,source)
                if arc in destroyed_edges or arc_reverse in destroyed_edges:
                    edges_to_remove.append(my_arc)
            """
    #for node in H.nodes():
    #    values = H.neighbors(node) # neighbors_iter(node)
    #    #print 'Values:'
    #    #print values
    #    if (len(values)== 0): #H.node[node]['status']=='destroyed':
    #        nodes_to_remove.append(node)
    for arc in edges_to_remove:
        new_graph.remove_edge(u=arc[0],v=arc[1])#,key=arc[2])

    for node in new_graph.nodes():
        values = new_graph.neighbors(node) # neighbors_iter(node)
        #print 'Values:'
        #print values
        if (len(values)== 0): #H.node[node]['status']=='destroyed':
            nodes_to_remove.append(node)

    for id_nodo in nodes_to_remove:
        new_graph.remove_node(id_nodo)
    print 'Num Edges to be removed:'
    print len(edges_to_remove)
    print 'Num Nodes to be removed:'
    print len(nodes_to_remove)
    print 'Number of Edges in the destroyed graph:'
    print len(new_graph.edges())
    print 'Number of Nodes in the destroyed graph:'
    print len(new_graph.nodes())
    return new_graph
###############################################################################
# Create a weighted graph by adding the reactances in the weight of each edge:
def Create_Weighted(H, link1, link2, reactances):
    new_graph = nx.Graph() #nx.Graph() #nx.MultiGraph(H) #nx.Graph() #nx.MultiGraph(H)
    #print 'Number of Edges HEEEEEEEEEERE:'
    #print len(H.edges())
    for n in H.nodes():
        if n not in new_graph.nodes():
            new_graph.add_node(n)      
    Added_Edges = []
    Double_Edges = []
    for e in H.edges():
        e1 = e[0]
        e2 = e[1]
        #print 'e1'
        #print e1
        #print 'e2'
        #print e2
        ##if e1 not in new_graph.nodes():
        ##    new_graph.add_node(e1)
        ##if e2 not in new_graph.nodes():
        ##    new_graph.add_node(e2)
        for m in range(0, len(link1)):
            if ((link1[m] == e1) and (link2[m] == e2)) or ((link2[m] == e1) and (link1[m] == e2)):
                if e in Double_Edges:
                    w = reactances[m]/2
                else:
                    w = reactances[m]
                if e not in Added_Edges:
                    Added_Edges.append(e)
                    #if (not new_graph.has_edge(e1,e2)) or (not new_graph.has_edge(e2, e1)):
                    #new_graph[e1][e2]['weight'] = w
                    new_graph.add_edge(e1, e2, weight= w)
                    #new_graph[e1][e2]['weight'] = w
                    #print 'New Graph Weight:'
                    #print new_graph[e1][e2]['weight']
                
                if e not in Double_Edges:
                    Double_Edges.append(e)
                else:
                    new_graph.remove_edge(u=e1, v=e2)
                    new_graph.add_edge(e1, e2, weight= w)
                
        Added_Edges = []
            #if (link1[m] == e2) and (link2[m] == e1):
            #    weight = reactances[m]
            #    if new_graph.has_edge(e2, e1) or new_graph.has_edge(e1, e2):
            #        new_graph[e1][e2]['weight'] = weight
                #new_graph.add_edge(e2, e1, weight)
    #if G.has_edge(subject_id, object_id):
                # we added this one before, just increase the weight by one
                #G[subject_id][object_id]['weight'] += 1
    #print 'NEW GRAPH:'
    #print new_graph
    #print 'Number of Edges in new_graph:'
    #print len(new_graph.edges())
    #for e in new_graph.edges():
    #    e1 = e[0]
    #    e2 = e[1]
    #    print 'Edges:'
    #    print e
    #    print 'Weight:'
    #    print new_graph[e1][e2]['weight']
    return new_graph
