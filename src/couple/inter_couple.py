#!/usr/bin/env python
# coding: utf-8
# created by hevlhayt@foxmail.com 
# Date: 2016/3/1 
# Time: 11:07
#
import random
#from src.cascade.graph import create_graph
from graph import create_graph

def create_couplings(g1, g2, max_dep, p):
    g1_inter = {}

    g1_size = len(g1.nodes())
    g2_size = len(g2.nodes())
    g2_nodes = g2.nodes()

    i = 0
    for node in g1.nodes():

        dep = random.randint(0, max_dep)
        link = []
        for m in range(dep):
            r = random.randint(0, g2_size-1)
            link.append(g2_nodes[r])

        g1_inter.setdefault(node, link)

        i += 1
        if i > g1_size*p:
            break

    return g1_inter


def create_couplings_121(g1, g2, p=1):

    if len(g1.nodes()) != len(g2.nodes()):
        raise TypeError
    l = len(g1.nodes())

    g1n = g1.nodes()
    g2n = g2.nodes()

    index = [i for i in range(l)]
    random.shuffle(index)
    g1_inter = {}
    for i in range(l):
        if i > l*p:
            break
        g1_inter.setdefault(g1n[i], [g2n[index[i]]])

    return g1_inter


def oppo_inter(a_inter):
    b_inter = {}
    for k, v in a_inter.items():
        for node in v:
            if not b_inter.has_key(node):
                b_inter.setdefault(node, [k])
            else:
                tmp = b_inter.get(node)
                if k not in tmp:
                    tmp.append(k)
                    b_inter.setdefault(node, tmp)

    return b_inter


if __name__ == '__main__':
    num_nodes = 1000
    g1 = create_graph('ba', num_nodes, 4)
    g2 = create_graph('ba', num_nodes, 4)

    g1c = create_couplings(g1, g2, 5, 0.5)
    # g2c = generate_inter_oppo(g1c)

    # print g1c
    # print "============================="
    # print g2c

    create_couplings_121(g1, g2)
