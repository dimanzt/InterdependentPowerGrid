#!/usr/bin/env python
# coding: utf-8
# created by hevlhayt@foxmail.com 
# Date: 2016/1/15 
# Time: 16:10
#
import os
from multiprocessing import Process
from src.cascade.findpc import findpc
from src.cascade.graph import create_graph


def run_cascade_single(Ga, Gb, size=10000):

    title = Ga+' '+Gb+' random attack pc s'
    print title

    degree = 4
    ga = create_graph(Ga, size, degree)
    pcl = []

    for l in range(2, 21):
        gb = create_graph(Gb, size, l*2)
        pc = findpc(ga, gb)
        pcl.append(pc)
        print Ga+' '+Gb+'--s--'+str(l)+'  '+str(pc)

    path = os.path.abspath('..\\..')+'\\exp\\'
    f = open(path+title+'.txt', 'wb')
    f.write(str(pcl))
    f.close()


def run_cascade_double(Ga, Gb, size=10000):

    title = Ga+' '+Gb+' random attack pc d'
    print title

    pcl = []

    for l in range(2, 21):
        ga = create_graph(Ga, size, l*2)
        gb = create_graph(Gb, size, l*2)
        pc = findpc(ga, gb)
        pcl.append(pc)
        print Ga+' '+Gb+'--d--'+str(l)+'  '+str(pc)

    path = os.path.abspath('..\\..')+'\\exp\\'
    f = open(path+title+'.txt', 'wb')
    f.write(str(pcl))
    f.close()

if __name__ == "__main__":
    # target1 = [('ba', 'er'), ('ba', 'ws'),
    #                    ('ws', 'er'), ('ws', 'ba'),
    #                    ('er', 'ba'), ('er', 'ws')]
    # target2 = [('ba', 'er'), ('ba', 'ws'), ('ws', 'er')]
    # for arg in target1:
    #     proc1 = Process(target=run_cascade_single, args=arg)
    #     proc1.start()
    # for arg in target2:
    #     proc2 = Process(target=run_cascade_double, args=arg)
    #     proc2.start()

    target3 = [('power', 'ws', 4941), ('er', 'power', 4941), ('ws', 'power', 4941), ('ba', 'power', 4941),
               ('air', 'er', 1226), ('air', 'ws', 1226), ('air', 'ba', 1226),
               ('er', 'air', 1226), ('ws', 'air', 1226), ('ba', 'air', 1226)]
    for arg in target3:
        proc2 = Process(target=run_cascade_single, args=arg)
        proc2.start()
