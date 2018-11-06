#!/usr/bin/env python
# coding: utf-8
# created by hevlhayt@foxmail.com
# Date: 2016/3/1
# Time: 19:08
#
import os
import random
import matplotlib.pyplot as plt
from multiprocessing import Process
import networkx as nx
from networkx.algorithms.operators.binary import disjoint_union
from networkx.algorithms.shortest_paths.generic import average_shortest_path_length
from src.cascade.graph import create_graph
from src.couple.findpc import findpc
from src.couple.inter_couple import create_couplings_121


def exp(arg0, arg1, arg2):
    title = arg0
    print title

    path = os.path.abspath('..\\..')+'\\exp2\\'
    f = open(path+title+'.txt', 'a+')

    num_nodes = 5000
    degree = 4

    g1 = create_graph('ba', num_nodes, degree)
    g2 = create_graph('ba', num_nodes, degree)

    # g1sort = sorted(nx.degree_centrality(g1).items(), lambda x, y: cmp(x[1], y[1]))
    # g2sort = sorted(nx.degree_centrality(g2).items(), lambda x, y: cmp(x[1], y[1]))

    inter = create_couplings_121(g1, g2)
    myInter = {}

    if arg1 == 0:
        for k, v in inter.items():
            myInter.setdefault(k, g1.degree(k) + g2.degree(v[0]))
    elif arg1 == 1:
        for k, v in inter.items():
            myInter.setdefault(k, g1.degree(k) * g2.degree(v[0]))
    elif arg1 == 2:
        for k, v in inter.items():
            myInter.setdefault(k, abs(g1.degree(k) - g2.degree(v[0])))
    if arg2 == 0:
        myInter = sorted(myInter.items(), lambda x, y: cmp(x[1], y[1]))
    if arg2 == 1:
        myInter = sorted(myInter.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
    # print myInter

    p = int(1 / 100.0 * len(inter))

    for i in range(60):

        for item in myInter[i*p:(i+1)*p]:
            inter.pop(item[0])

        pc = findpc(g1, g2, inter)

        g3 = disjoint_union(g1, g2)
        # print g3.nodes()

        for i1, i22 in inter.items():
            for i2 in i22:
                g3.add_edge(i1, i2+num_nodes)

        singleNodes = []
        for node in g3:
            if g3.degree(node) == 0:
                singleNodes.append(node)
        # print singleNodes
        g3.remove_nodes_from(singleNodes)
        # print nx.is_connected(g1)
        # print nx.is_connected(g2)
        # print nx.is_connected(g3), "===="
        try:
            pathLen = average_shortest_path_length(g3)
        except Exception:
            continue

        result = str(pc)+" "+str(pathLen)
        print title, result, i

        f.write(result+'\n')

    f.close()


if __name__ == '__main__':
    time = '412'
    type = 'ba'
    target = [(type+'_'+'add'+'_'+time, 0, 0), (type+'_'+'add_r'+'_'+time, 0, 1),
              (type+'_'+'mul'+'_'+time, 1, 0), (type+'_'+'mul_r'+'_'+time, 1, 1),
              (type+'_'+'min'+'_'+time, 2, 0), (type+'_'+'min_r'+'_'+time, 2, 1)]

    for arg in target:
        proc2 = Process(target=exp, args=arg)
        proc2.start()


