#!/usr/bin/env python
# coding: utf-8
# created by hevlhayt@foxmail.com 
# Date: 2016/1/16 
# Time: 15:14
#
#from src.cascade.findpc import findpc
from findpc import findpc
from graph import create_graph
#from src.cascade.graph import create_graph
import networkx as nx

import networkx as nx
#from src.cascade.graph import create_graph
#from src.couple.inter_couple import create_couplings_121
from graph import create_graph
from inter_couple import create_couplings_121

num_nodes = 1000
degree = 4

g1 = create_graph('er', num_nodes, degree)
g2 = create_graph('er', num_nodes, degree)

print findpc(g1, g2)
