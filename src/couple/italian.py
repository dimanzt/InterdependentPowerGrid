#!/usr/bin/env python
# coding: utf-8
# created by hevlhayt@foxmail.com 
# Date: 2016/2/26 
# Time: 9:27
#
import os
import random
import networkx as nx
import matplotlib.pyplot as plt
#from src.couple.cascading_failures import cascading_failures, cascading_failures2
from cascading_failures import cascading_failures, cascading_failures2, cascading_failures_o
import matplotlib.pyplot as plt

def create_italian():

    #hpath = os.path.abspath('..\\..')+'\\data\\PIData\\\\hviet'
    #hcpath = os.path.abspath('..\\..')+'\\data\\PIData\\hviet_coordinates'
    #gpath = os.path.abspath('..\\..')+'\\data\\PIData\\garr'
    #gcpath = os.path.abspath('..\\..')+'\\data\\PIData\\garr_coordinates'
    hpath = os.path.abspath('../../')+'/data/PIData/hviet'
    hcpath = os.path.abspath('../../')+'/data/PIData/hviet_coordinates'
    gpath = os.path.abspath('../../')+'/data/PIData/garr'
    gcpath = os.path.abspath('../../')+'/data/PIData/garr_coordinates' 
    f_hviet = open(hpath, 'r')
    f_hvietc = open(hcpath, 'r')
    f_garr = open(gpath, 'r')
    f_garrc = open(gcpath, 'r')

    Ghviet = nx.Graph()
    Ggarr = nx.Graph()

    hc_dict = {}
    loc = ''
    node = ''
    for l in f_hvietc:
        tmp = l.rstrip('\n').split(',')
        if tmp[1]+tmp[2] != loc:
            node = tmp[0]
            loc = tmp[1]+tmp[2]
            hc_dict.setdefault(node, [node, float(tmp[1]), float(tmp[2])])
        else:
            hc_dict.setdefault(tmp[0], [node, float(tmp[1]), float(tmp[2])])

    # print hc_dict

    for l in f_hviet:
        nodes = l.rstrip('\n').split(',')
        Ghviet.add_edge(hc_dict.get(nodes[0])[0], hc_dict.get(nodes[1])[0])

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
    for net in Ggarr:
        mindist = 1000000.0
        inter = ''
        for node in Ghviet:
            x1 = hc_dict.get(node)[1]
            y1 = hc_dict.get(node)[2]
            x2 = gc_dict.get(net)[0]
            y2 = gc_dict.get(net)[1]
            dist = (x1-x2)*(x1-x2)+(y1-y2)*(y1-y2)
            if mindist > dist:
                mindist = dist
                inter = node

        # print 'garr node: %s  hviet node: %s  min dist: %s (%s, %s)-(%s, %s)' % \
        #       (net, inter, mindist, gc_dict.get(net)[0], gc_dict.get(net)[1],
        #           hc_dict.get(inter)[1], hc_dict.get(inter)[2])

        g_inter.setdefault(net, inter)
        if not h_inter.has_key(inter):
            h_inter.setdefault(inter, [net])
        else:
            tmp = h_inter.get(inter)
            h_inter.setdefault(inter, tmp.append(net))

    print 'hviet nodes: '+str(len(Ghviet.nodes()))
    print 'hviet edges: '+str(Ghviet.size())
    print 'garr nodes: '+str(len(Ggarr.nodes()))
    print 'garr edges: '+str(Ggarr.size())
    print h_inter
    print g_inter

    f_hviet.close()
    f_hvietc.close()
    f_garr.close()
    f_garrc.close()

    return [Ghviet, Ggarr, h_inter, g_inter]

if __name__ == '__main__':
    num_nodes = 1000
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

    x = []
    y = []
    for i in range(50):
        print i
        sum = 0
        it = 30
        for j in range(it):
            #er1 = create_graph('er', num_nodes, 4)
            g1 = hviet.copy()
            g2 = garr.copy()
            #er2 = create_graph('er', num_nodes, 4)
            remove_nodes = set([])
            k = 0
            while len(remove_nodes) < num_nodes * i / 50.0:
                r = random.randint(0, num_nodes)
                remove_nodes.add(r)
                k += 1
            cascading_failures_o(g1, g2, remove_nodes)
            sum += len(g1)
        y.append(sum / float(num_nodes) / it)
        x.append(1-i/50.0)
    print 'Printing x:'
    print x
    print 'Printing y:'
    print y

    """
    italian = create_italian()
    hviet = italian[0]
    garr = italian[1]
    h_inter = italian[2]
    g_inter = italian[3]
    num_nodes = len(garr.nodes())
    print num_nodes

    x = []
    y = []
    for i in range(50):
        print i
        sum = 0
        for j in range(50):
            g1 = hviet.copy()
            g2 = garr.copy()
            remove_nodes = set([])
            k = 0
            while len(remove_nodes) < num_nodes * i / 50.0:
                r = random.randint(0, num_nodes-1)
                # print r
                remove_nodes.add(garr.nodes()[r])
                k += 1
            cascading_failures2(g1, g2, remove_nodes, g_inter, h_inter)
            sum += len(g1)
            print 'Sum'
            print sum
        y.append(sum / float(num_nodes) / 50)
        x.append(1-i/50.0)
    #plt.plot(x, y)
    print 'Printing x'
    print x
    print 'Printing y'
    print y
    #plt.plot(x, y, 'o')
    #plt.show()
    """




