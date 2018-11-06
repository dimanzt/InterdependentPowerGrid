__author__ = 'Diman'

from gurobipy import *
import numpy as np
from my_lib_DC_Flow_delta import *

# Model data
#[precision, recall, detcted_edges] = Detect_gray(nodes, power, link1, link2, reactances, linkNum, Thr, remoced_edges, gray)
def Detect_gray(nodes, power, link1, link2, reactances, linkNum, Thr, removed_edges, gray, Original_link1, Original_link2, Original_reactances, RemovedEdges):
#def optimal_DC_Flow_delta(nodes, power, link1, link2, reactances, linkNum, Thr):
    precision = []
    recall = []
    detected_edges = []
    #########################GREEEDY BASED APPROACH###############################
    [precision, recall, detcted_edges] = Detect_gray(nodes, power, link1, link2, reactances, linkNum, Thr, removed_edges, gray, Original_link1, Original_link2, Original_reactances, RemovedEdges)

    return precision, recall, detected_edges
# Solve ILP of max flow problem where the Sets are given and each set can identify a set of links,

def Detect_gray(nodes, power, link1, link2, reactances, linkNum, Thr, removed_edges, gray, Original_link1, Original_link2, Original_reactances, RemovedEdges):
#def DC_Flow_solution(nodes, power, link1, link2, reactances, linkNum, Thr):
    precision = []
    recall = []
    detected_edges = []
    #############################################################################
    #Print the Detection rate before the detection algorithm:
    #for m in range(0, len(flows)):
    #    if
    NotDetected = 0
    loop =1
    while(loop == 1):
        for m in range(0, len(gray)):
            if(gray[m] ==1):
                NotDetected = NotDetected + 1
        print 'LENGTH GRAY:'
        print len(gray)
        print 'NOT DETECTED:'
        print NotDetected
        print 'Detection Rate:'
        print float(float(len(gray) - NotDetected) / float(len(gray)))
        recall = float(float(len(gray) - NotDetected) / float(len(gray))) #float(float((len(gray) - NotDetected))/float(len(gray)))
        if (recall <= 1.0):
            loop = 0
    print 'DETECTION RATE Before the Detection:'
    print recall
    NotDetected = 0
    #############################################################################
    flows = []
    ILP_gen_power = []
    ILP_load_power = []
    cost = []
    TotalPower = []
    #############################################################################
    [flows, ILP_gen_power, ILP_load_power, cost, TotalPower] = optimal_DC_Flow_delta(nodes, power, link1, link2,reactances, linkNum, Thr)
    GrayEdges = []
    SingleEdgeIndex = []
    for m in range(0, len(power)):
        GrayEdges.append(0)
        for k in range(0, len(RemovedEdges)):
            #print 'KKKKKKKKKKKKKKKKKKK:'
            #print k
            #print len(gray)
            #print len(RemovedEdges)
            e1 = RemovedEdges[k][0]
            e2 = RemovedEdges[k][1]
            if (e1 == m) or (e2 == m):
                GrayEdges[m] = GrayEdges[m] +1 
                SingleEdgeIndex = k
        if (GrayEdges[m] ==1):
            gray[SingleEdgeIndex] = 0
        if (m < len(ILP_gen_power)):
            total_power = 0
            for h in range(0, len(link1)):
                if (link1[h] == m):
                    total_power = flows[h] + total_power
                if (link2[h] == m):
                    total_power = total_power - flows[h]
            if (ILP_gen_power[m] == total_power):
                for j in range(0, len(RemovedEdges)):
                    e1 = RemovedEdges[j][0]
                    e2 = RemovedEdges[j][1]
                    if (e1 == m) or (e2 == m):
                        gray[j] = 0
        if ((m- len(ILP_gen_power)) < len(ILP_load_power)) and (m >= len(ILP_gen_power)):
            total_power = 0
            for h in range(0, len(link1)):
                if (link1[h] == m):
                    total_power = flows[h] + total_power
                if (link2[h] == m):
                    total_power = total_power - flows[h]
            if (ILP_load_power[m - len(ILP_gen_power)] == total_power):
                for j in range(0, len(RemovedEdges)):
                    e1 = RemovedEdges[j][0]
                    e2 = RemovedEdges[j][1]
                    if (e1 == m) or (e2 == m):
                        gray[j] = 0
        ################################################################
        if ((m- len(ILP_gen_power)- len(ILP_load_power) < (361- len(ILP_gen_power)- len(ILP_load_power))) and (m >= len(ILP_gen_power)+ len(ILP_load_power))):
            total_power = 0
            for h in range(0, len(link1)):
                if (link1[h] == m):
                    total_power = flows[h] + total_power
                if (link2[h] == m):
                    total_power = total_power - flows[h]
            if (power[m] == total_power):# - len(ILP_gen_power)- len(ILP_gen_power)] == total_power):
                for j in range(0, len(RemovedEdges)):
                    e1 = RemovedEdges[j][0]
                    e2 = RemovedEdges[j][1]
                    if (e1 == m) or (e2 == m):
                        gray[j] = 0


    #for m in range(0, len(flows)):
    #    if 
    NotDetected = 0
    loop =1 
    while(loop == 1):
        for m in range(0, len(gray)):
            if(gray[m] ==1):
                NotDetected = NotDetected + 1
        print 'LENGTH GRAY:'
        print len(gray)
        print 'NOT DETECTED:'
        print NotDetected
        print 'Detection Rate:'
        print float(float(len(gray) - NotDetected) / float(len(gray)))
        recall = float(float(len(gray) - NotDetected) / float(len(gray))) #float(float((len(gray) - NotDetected))/float(len(gray)))
        if (recall <= 1.0):
            loop = 0
    print 'DETECTION RATEEEEEEEEEEEEEEEEEEEEEEEEEEEE:'
    print recall
    return precision, recall, detected_edges

