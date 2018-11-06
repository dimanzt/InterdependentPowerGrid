#!/usr/bin/env python
# coding: utf-8
# created by hevlhayt@foxmail.com 
# Date: 2016/1/15 
# Time: 9:47
#
import random
import networkx as nx
from src.couple.cascading_failures import cascading_failures, cascading_failures2
from src.couple.inter_couple import oppo_inter


def findpc(G1, G2, inter):
    epsilon = 0.001
    tol = 0.001
    a, b = 0.0, 1.0

    while (b - a) > epsilon:

        mid = (a + b) / 2
        # print mid
        pm = cal_pi(G1, G2, mid, inter)

        if pm > tol:
            a = mid
        else:
            b = mid
        # print "===================="
    return 1 - (a + b) / 2


def cal_pi(G1, G2, p, inter):
    size = len(G1)
    it = 100
    sl = 0
    inter2 = oppo_inter(inter)
    for j in range(it):
        g1 = G1.copy()
        g2 = G2.copy()
        # print j
        remove_nodes = set([])
        while len(remove_nodes) < size * p:
            r = random.randint(0, size)
            remove_nodes.add(r)

        cascading_failures2(g1, g2, remove_nodes, inter, inter2)
        sl += len(g1)
    pi = float(sl) / it / size

    return pi


if __name__ == '__main__':
    print 1