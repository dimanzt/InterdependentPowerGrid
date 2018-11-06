#!/usr/bin/env python
# coding: utf-8
# created by hevlhayt@foxmail.com 
# Date: 2016/2/26 
# Time: 15:19
#
import os
import random
import networkx as nx
import matplotlib.pyplot as plt
from src.couple.cascading_failures import cascading_failures, cascading_failures2


def create_indian():

    path = os.path.abspath('..\\..')+'\\data\\ARData\\'
    airpath = os.path.abspath('..\\..')+'\\data\\ARData\\Airports_Edgelist.txt'
    railpath = os.path.abspath('..\\..')+'\\data\\ARData\\Railway_Edgelist.txt'

    airf = open(airpath, 'r')
    railf = open(railpath, 'r')

    GAir = nx.Graph()
    GRail = nx.Graph()

    for l in airf:
        tmp = l.rstrip('\n').split(' ')
        GAir.add_edge('A_'+tmp[2], 'A_'+tmp[5])

    air_inter = {}
    rail_inter = {}
    i = 0
    for f in os.listdir(path):
        # if i > 100:
        #     break
        # i += 1

        if f.startswith('S'):
            data = open(path+f, 'r')
            for l in data:
                rail = l.split('/')[1].split(' ')
                air = l.split('/')[2].split(':')
                # print rail+air

                rname = 'R_'+rail[0]
                aname = 'A_'+air[0]

                if rail[0] == '' or (not GAir.has_node(aname)):
                    continue

                rail_inter.setdefault(rname, aname)

                if not air_inter.has_key(aname):
                    air_inter.setdefault(aname, [rname])
                else:
                    tmp = air_inter.get(aname)
                    if not rname in tmp:
                        tmp.append(rname)
                        air_inter.setdefault(aname, tmp)
                    # print aname+'  '+str(tmp)
            data.close()

    for l in railf:
        tmp = l.rstrip('\n').split('\t')
        if rail_inter.has_key('R_'+tmp[0]) and rail_inter.has_key('R_'+tmp[1]):
            GRail.add_edge('R_'+tmp[0], 'R_'+tmp[1])

    print 'Air nodes: '+str(len(GAir.nodes()))
    print 'Air edges: '+str(GAir.size())
    print 'Rail nodes: '+str(len(GRail.nodes()))
    print 'Rail edges: '+str(GRail.size())
    print 'Air inter size: '+str(len(air_inter))
    print 'Rail inter size: '+str(len(rail_inter))

    print air_inter
    print rail_inter
    airf.close()
    railf.close()

    # nx.draw(GAir)
    # nx.draw(GRail)
    # plt.show()

    return [GAir, GRail, air_inter, rail_inter]


if __name__ == '__main__':
    italian = create_indian()
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
            g1 = garr.copy()
            g2 = hviet.copy()
            remove_nodes = set([])
            k = 0
            while len(remove_nodes) < num_nodes * i / 50.0:
                r = random.randint(0, num_nodes-1)
                # print r
                remove_nodes.add(garr.nodes()[r])
                k += 1
            cascading_failures2(g1, g2, remove_nodes, g_inter, h_inter)
            sum += len(g1)
        y.append(sum / float(num_nodes) / 50)
        x.append(1-i/50.0)

    plt.plot(x, y, 'o')
    plt.show()
