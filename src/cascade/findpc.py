#!/usr/bin/env python
# coding: utf-8
# created by hevlhayt@foxmail.com 
# Date: 2016/1/15 
# Time: 9:47
#
import random
import networkx as nx
#from src.cascade.cascading_failures import cascading_failures
from cascading_failures import cascading_failures

def findpc(G1, G2, attack='random'):
    epsilon = 0.001
    tol = 0.001
    a, b = 0.0, 1.0

    while (b - a) > epsilon:

        mid = (a + b) / 2
        pm = cal_pi(G1, G2, mid, attack)

        if pm > tol:
            a = mid
        else:
            b = mid

    return 1 - (a + b) / 2


def cal_pi(G1, G2, p, attack):
    size = len(G1)
    it = 100
    sl = 0

    for j in range(it):
        g1 = G1.copy()
        g2 = G2.copy()

        remove_nodes = set([])

        if attack == 'random':
            while len(remove_nodes) < size * p:
                r = random.randint(0, size)
                remove_nodes.add(r)
        elif attack == 'high':
            l = sorted(nx.degree_centrality(g1).items(),
                       lambda x, y: cmp(x[1], y[1]), reverse=True)
            k = 0
            while len(remove_nodes) < size * p:
                remove_nodes.add(l[k][0])
                k += 1
        elif attack == 'low':
            l = sorted(nx.degree_centrality(g1).items(),
                       lambda x, y: cmp(x[1], y[1]))
            k = 0
            while len(remove_nodes) < size * p:
                remove_nodes.add(l[k][0])
                k += 1

        cascading_failures(g1, g2, remove_nodes)
        sl += len(g1)

    pi = float(sl) / it / size

    return pi


if __name__ == '__main__':
    print 1
