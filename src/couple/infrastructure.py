#!/usr/bin/env python
# coding: utf-8
# created by hevlhayt@foxmail.com 
# Date: 2015/12/15 
# Time: 8:47
#
import os
import random
import networkx as nx


def power_grid_graph():
    G = nx.Graph()
    path = os.path.abspath('..\\..')+'\\data\\powergrid'
    f = open(path, 'r')
    for line in f:
        l = line.rstrip('\n').split(' ')
        # print l
        G.add_edge(int(l[0])-1, int(l[1])-1)
    f.close()
    return G


def power_grid_graph_random():
    path = os.path.abspath('..\\..')+'\\data\\powergrid'
    G = nx.Graph()
    connect = []
    f = open(path, 'r')
    i = 0
    for line in f:
        l = line.rstrip('\n').split(' ')
        # print l
        connect.append((int(l[0])-1, int(l[1])-1))
        i += 1
    index = [j+1 for j in range(i)]

    random.shuffle(index)
    # print index

    for c in connect:
        G.add_edge(index[c[0]], index[c[1]])
    f.close()
    return G


def airport_graph():
    G = nx.Graph()
    path = os.path.abspath('..\\..')+'\\data\\usairport'
    f = open(path, 'r')
    for line in f:
        l = line.rstrip('\n').split(' ')
        # print l
        G.add_edge(int(l[0])-1, int(l[1])-1)
    f.close()
    return G


if __name__ == '__main__':
    grid = airport_graph()
    print len(grid.nodes())


