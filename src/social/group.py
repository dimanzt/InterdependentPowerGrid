#!/usr/bin/env python
# coding: utf-8
# created by hevlhayt@foxmail.com 
# Date: 2016/11/6
# Time: 15:42
import random
from collections import Counter

import networkx as nx
import matplotlib.pyplot as plt


x, y = [], []
# f = open('weight', 'w')
num_of_groups = 100
# for i in xrange(100, num_of_groups+1):
for i in [10, 20, 50, 100]:

    print i
    x.append(i)
    num_of_members = i
    it = 100

    sl = 0.0
    cnt = Counter()
    for j in xrange(it):
        # G = nx.barabasi_albert_graph(num_of_groups * num_of_members, num_of_members)
        G = nx.watts_strogatz_graph(num_of_groups * num_of_members, num_of_members, 0.3)
        # nx.draw(G)
        # plt.show()

        nodes = G.nodes()
        random.shuffle(nodes)

        group_index = {n: nodes.index(n) / num_of_members for n in G.nodes()}
        # print group_index

        G_group = nx.Graph()
        for s, t in G.edges():
            s, t = group_index[s], group_index[t]
            if G_group.has_edge(s, t):
                G_group[s][t]['weight'] += 1
            else:
                G_group.add_edge(s, t, weight=1)

        # print G_group.edges(), G.edges()

        for s, t, d in G_group.edges(data=True):
            # print s, t, d['weight']
            cnt[d['weight']] += 1
            # if d['weight'] < len(groups[s]) * len(groups[t]) / 2.0:
            #     G_group.remove_edge(s, t)

        average_weight = G.number_of_edges() / float(G_group.number_of_edges())
        sl += average_weight
        # print average_weight
        # # print G.number_of_edges() / float(G_group.number_of_edges()) / num_of_members
        # print '==='

    y.append(sl / it)
    print sl / it

    weight = [[k, cnt[k] / float(it)] for k in sorted(cnt, key=cnt.get, reverse=True)]
    # f.write(str(i)+'\n')
    # f.write(str(weight)+'\n')
    # f.flush()
    print weight
    print '======'

# f.close()
plt.plot(x, y)
plt.plot([i for i in xrange(num_of_groups)], [i for i in xrange(num_of_groups)])
plt.show()