#!/usr/bin/env python
# coding: utf-8
# created by hevlhayt@foxmail.com 
# Date: 2016/1/15 
# Time: 16:16
#
import random
import networkx as nx
#import src.cascade.infrastructure as inf
import infrastructure as inf

def create_graph(g, size, degree):

    if g == 'ba':
        G = nx.barabasi_albert_graph(size, degree / 2)
    elif g == 'bas':
        ba = nx.barabasi_albert_graph(size, degree / 2)
        G = ba_random(ba)
    elif g == 'er':
        G = nx.fast_gnp_random_graph(size, float(degree) / size)
    elif g == 'ws':
        G = nx.connected_watts_strogatz_graph(size, degree, 0.3)
    elif g == 'power':
        G = inf.power_grid_graph()
        add_edges(G, degree)
    elif g == 'powers':
        G = inf.power_grid_graph_random()
    elif g == 'air':
        G = inf.airport_graph()
        add_edges(G, degree)
    else:
        G = nx.gnm_random_graph(size, degree*size)

    return G


def add_edges(G, degree):
    l = len(G)
    for node in range(l):
        i = 0
        while i < degree/2:
            r = random.randint(0, l-1)
            if not G.has_edge(node, r):
                G.add_edge(node, r)
                i += 1


def ba_random(ba):
    G = nx.Graph()
    index = [j for j in range(len(ba))]
    random.shuffle(index)

    for node in ba.nodes():
        for nei in ba.neighbors(node):
            G.add_edge(index[node], index[nei])

    return G
