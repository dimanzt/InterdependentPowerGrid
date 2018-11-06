#!/usr/bin/env python
# coding: utf-8
# created by hevlhayt@foxmail.com 
# Date: 2016/1/15 
# Time: 9:28
#
import random
import networkx as nx
#from src.cascade.graph import create_graph
from graph import create_graph

import matplotlib.pyplot as plt
#from src.couple.inter_couple import oppo_inter, create_couplings, create_couplings_121
from inter_couple import  oppo_inter, create_couplings, create_couplings_121

def cascading_failures_o(G1, G2, init_nodes):
    G1.remove_nodes_from(init_nodes)
    na = len(init_nodes)
    noi = 0
    while na > 0:

        largests_a = sorted(nx.connected_components(G1), key=len, reverse=True)
        if len(largests_a) == 0:
            break
        largest_a = largests_a[0]

        remove_nodes_a = set([])
        remove_nodes_b = set([])
        for g1node in G1.nodes_iter():
            if g1node not in largest_a:
                remove_nodes_a.add(g1node)
        G1.remove_nodes_from(remove_nodes_a)

        for g2node in G2.nodes_iter():
            if g2node not in largest_a:
                remove_nodes_b.add(g2node)

        G2.remove_nodes_from(remove_nodes_b)

        remove_nodes_a.clear()
        remove_nodes_b.clear()

        # print "remove a %s----remove b %s" % (na ,nb)
        # print "ba1 len: %s" % (len(ba1))
        # print "---"

        largests_b = sorted(nx.connected_components(G2), key=len, reverse=True)
        if len(largests_b) == 0:
            break
        largest_b = largests_b[0]

        for g2node in G2.nodes_iter():
            if g2node not in largest_b:
                remove_nodes_b.add(g2node)

        G2.remove_nodes_from(remove_nodes_b)

        for g1node in G1.nodes_iter():
            if g1node not in largest_b:
                remove_nodes_a.add(g1node)

        G1.remove_nodes_from(remove_nodes_a)
        na = len(remove_nodes_a)
        remove_nodes_a.clear()
        remove_nodes_b.clear()
        if na == 0:
            break
        noi += 1
    return noi


def add_more_edges_random(G, num_edge, size):
    k = 0
    while k < num_edge:
        a, b = random.randint(0, size), random.randint(0, size)
        if not G.has_edge(a, b):
            G.add_edge(a, b)
            k += 1

def cascading_failures(G1, G2, init_nodes, G1_inter, G2_inter):
    G1.remove_nodes_from(init_nodes)
    na = len(init_nodes)

    for node in init_nodes:
        if G1_inter.has_key(node):
            couple_nodes = G1_inter.get(node)
            for couple in couple_nodes:
                if G2.has_node(couple):
                    G2.remove_node(couple)

    remove_nodes_a = set([])
    remove_nodes_b = set([])

    noi = 0
    while na > 0:

        largests_a = sorted(nx.connected_components(G1), key=len, reverse=True)
        if len(largests_a) == 0:
            break
        largest_a = largests_a[0]

        for g1node in G1.nodes_iter():
            if g1node not in largest_a:
                remove_nodes_a.add(g1node)
                if G1_inter.has_key(g1node):
                    couple_nodes = G1_inter.get(g1node)
                    for couple in couple_nodes:
                        remove_nodes_b.add(couple)

        G1.remove_nodes_from(remove_nodes_a)
        G2.remove_nodes_from(remove_nodes_b)

        # print "remove a %s----remove b %s" % (len(remove_nodes_a) ,len(remove_nodes_b))
        # print "G1 len: %s" % (len(G1))
        # print "G2 len: %s" % (len(G2))
        # print "---"

        remove_nodes_a.clear()
        remove_nodes_b.clear()

        largests_b = sorted(nx.connected_components(G2), key=len, reverse=True)
        if len(largests_b) == 0:
            break
        largest_b = largests_b[0]

        for g2node in G2.nodes_iter():
            if g2node not in largest_b:
                remove_nodes_b.add(g2node)
                if G2_inter.has_key(g2node):
                    couple_nodes = G2_inter.get(g2node)
                    for couple in couple_nodes:
                        remove_nodes_a.add(couple)

        # for node in remove_nodes_a:
        #     if G1_inter.has_key(node):
        #         couple_nodes = G1_inter.get(node)
        #         for couple in couple_nodes:
        #             remove_nodes_b.add(couple)

        G1.remove_nodes_from(remove_nodes_a)
        G2.remove_nodes_from(remove_nodes_b)

        na = len(remove_nodes_a)
        remove_nodes_a.clear()
        remove_nodes_b.clear()
        if na == 0:
            break
        noi += 1
    return noi


def cascading_failures2(G1, G2, init_nodes, G1_inter, G2_inter):

    na = len(init_nodes)
    remove_nodes_a = init_nodes
    remove_nodes_b = set([])

    noi = 0
    while na > 0:

        G1.remove_nodes_from(remove_nodes_a)

        for node in remove_nodes_a:
            if G1_inter.has_key(node):
                couple_nodes = G1_inter.get(node)
                for couple in couple_nodes:
                    if G2.has_node(couple):
                        remove_nodes_b.add(couple)

        remove_nodes_a.clear()

        #############################################################################
        largests_a = sorted(nx.connected_components(G1), key=len, reverse=True)
        if len(largests_a) == 0:
            break
        largest_a = largests_a[0]

        for g1node in G1.nodes_iter():
            if g1node not in largest_a:
                remove_nodes_a.add(g1node)
                if G1_inter.has_key(g1node):
                    couple_nodes = G1_inter.get(g1node)
                    for couple in couple_nodes:
                        remove_nodes_b.add(couple)

        G1.remove_nodes_from(remove_nodes_a)
        G2.remove_nodes_from(remove_nodes_b)

        remove_nodes_a.clear()
        for node in remove_nodes_b:
            if G2_inter.has_key(node):
                couple_nodes = G2_inter.get(node)
                for couple in couple_nodes:
                    remove_nodes_a.add(couple)

        remove_nodes_b.clear()

        #############################################################################
        largests_b = sorted(nx.connected_components(G2), key=len, reverse=True)
        if len(largests_b) == 0:
            break
        largest_b = largests_b[0]

        for g2node in G2.nodes_iter():
            if g2node not in largest_b:
                remove_nodes_b.add(g2node)
                if G2_inter.has_key(g2node):
                    couple_nodes = G2_inter.get(g2node)
                    for couple in couple_nodes:
                        remove_nodes_a.add(couple)

        G2.remove_nodes_from(remove_nodes_b)

        na = len(remove_nodes_a)
        remove_nodes_b.clear()
        if na == 0:
            break
        noi += 1
    return noi


if __name__ == '__main__':
    num_nodes = 5000
    p = 0.2
    color = ['ob', 'og', 'or', 'oc', 'ok', 'oy', 'om']
    # color = ['b', 'g', 'r', 'c', 'k', 'y', 'm', 'ob', 'og', 'or', 'oc', 'ok', 'oy', 'om']
    for lines in [0, 5, 10, 20]:

        x = []
        y = []
        for i in range(50):
            print i
            sum = 0
            it = 10
            for j in range(it):
                g1 = create_graph('ba', num_nodes, 4)
                g2 = create_graph('ba', num_nodes, 4)
                if lines != 0:
                    g1_inter = create_couplings(g1, g2, lines*5, p)
                else:
                    g1_inter = create_couplings_121(g1, g2)
                g2_inter = oppo_inter(g1_inter)
                # print g1_inter
                remove_nodes = set([])
                k = 0
                while len(remove_nodes) < num_nodes * i / 50.0:
                    r = random.randint(0, num_nodes)
                    remove_nodes.add(r)
                    k += 1
                cascading_failures2(g1, g2, remove_nodes, g1_inter, g2_inter)
                sum += len(g1)
            y.append(sum / float(num_nodes) / it)
            x.append(1 - i/50.0)
        plt.plot(x, y, color[lines % 7])
    plt.show()




    # g1_inter = {}
    # g2_inter = {}
    #
    # i = 0
    # for n in range(num_nodes):
    #
    #     ram = random.randint(0, 4*lines)
    #     link = []
    #     for m in range(ram):
    #
    #         r = random.randint(0, num_nodes)
    #         link.append(r)
    #         if not g2_inter.has_key(r):
    #             g2_inter.setdefault(r, [n])
    #         else:
    #             tmp = g2_inter.get(r)
    #             tmp.append(n)
    #             g2_inter.setdefault(r, tmp)
    #
    #     g1_inter.setdefault(n, link)
    #
    #     i += 1
    #     if i > num_nodes*p:
    #         break
    #
    # print er1_inter
    # print er2_inter



