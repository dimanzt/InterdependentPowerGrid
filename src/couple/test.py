#!/usr/bin/env python
# coding: utf-8
# created by hevlhayt@foxmail.com 
# Date: 2016/1/16 
# Time: 20:03
#
import os
import random
import networkx as nx
from networkx.algorithms.operators.binary import disjoint_union
from networkx.algorithms.shortest_paths.generic import average_shortest_path_length
import sys

# a = [random.random() for i in range(20)]
# b = [random.random() for i in range(20)]
#
# title = "remove_degree_sum_ba_410"
# print title
#
# path = os.path.abspath('..\\..')+'\\exp2\\'
# f = open(path+title+'.txt', 'a+')
# f.write('hello')
# f.write('hello')
# f.write('hello')

# a = [i for i in range(1000000)]
# a.remove(random.randint(1000000))
# len(a)

print 37.5/100*37.5+(1-37.5/100)*25+(1-37.5/100)*50

# for t in a:

# path = os.path.abspath('..\\..')+'\\data\\garr_coordinates.txt'
# f = open(path, 'r')
# i = 0
# for l in f:
#     i+=1
#     l = l.lstrip('   ').rstrip('\n')
#     tmp = l.split('   ')
#
#     if tmp[1].endswith('0'):
#         tmp[1] = float(tmp[1][0:5])
#     else:
#         tmp[1] = float(tmp[1][0:5])*10
#     if tmp[2].endswith('0'):
#         tmp[2] = float(tmp[2][0:5])
#     else:
#         tmp[2] = float(tmp[2][0:5])*10
#     print str(i)+','+str(tmp[1])+','+str(tmp[2])

# path = os.path.abspath('..\\..')+'\\data\\garr_net.txt'
# f = open(path, 'r')
# for l in f:
#
#     l = l.lstrip('   ').rstrip('\n')
#     tmp = l.split('   ')
#     if tmp[0].endswith('0'):
#         tmp[0] = tmp[0][0:1]
#     else:
#         tmp[0] = tmp[0][0:1]+tmp[0][2:3]
#     if tmp[1].endswith('0'):
#         tmp[1] = tmp[1][0:1]
#     else:
#         tmp[1] = tmp[1][0:1]+tmp[1][2:3]
#     print tmp[0]+','+tmp[1]

# path = os.path.abspath('..\\..')+'\\data\\hvietloc'
# f = open(path, 'r')
#
# s = {}
# loc = ''
# node = ''
# news = ''
# for l in f:
#     l.rstrip('\n')
#     info = l.split('\t')
#     # print info
#
#     if info[3]+info[4] != loc:
#         node = info[0]
#         loc = info[3]+info[4]
#         lat = info[3][0:len(info[3])-1].split('\xa1\xe3')
#         lon = info[4][0:len(info[4])-2].split('\xa1\xe3')
#         news += info[0]+','+str(float(lat[0])+float(lat[1])/100.0)+','+str(float(lon[0])+float(lon[1])/100.0)+'\n'
#         s.setdefault(info[0], [info[0], [float(lat[0])+float(lat[1])/100.0, float(lon[0])+float(lon[1])/100.0]])
#     else:
#         lat = info[3][0:len(info[3])-1].split('\xa1\xe3')
#         lon = info[4][0:len(info[4])-2].split('\xa1\xe3')
#         s.setdefault(info[0], [node, [float(lat[0])+float(lat[1])/100.0, float(lon[0])+float(lon[1])/100.0]])
#         news += info[0]+','+str(float(lat[0])+float(lat[1])/100.0)+','+str(float(lon[0])+float(lon[1])/100.0)+'\n'
#
# # print s
# # print len(s)
# print news
# f.close()
#
# G = nx.Graph()
# path = os.path.abspath('..\\..')+'\\data\\hviet'
# f = open(path, 'r')
# for l in f:
#     nodes = l.rstrip('\n').split(',')
#
#     G.add_edge(s.get(nodes[0])[0], s.get(nodes[1])[0])

# print G.size()
# print len(G.nodes())




# G1 = nx.barabasi_albert_graph(1000, 2)
# sg1 = average_shortest_path_length(G1)
# print sg1
# G2 = nx.barabasi_albert_graph(1000, 2)
# sg2 = average_shortest_path_length(G2)
# print sg2
# sg = sg1 + sg2
# G3 = disjoint_union(G1, G2)
# G4 = disjoint_union(G1, G2)
# size = len(G1)
# interlayer = [i for i in range(size)]
# random.shuffle(interlayer)
# for node in G1.nodes():
#
#     if G1.degree(node)+G2.degree(interlayer[node]) > 1:
#         G3.add_edge(node, interlayer[node]+size)
#
# for node in G1.nodes():
#
#     if G1.degree(node)+G2.degree(interlayer[node]) <= 4:
#         G4.add_edge(node, interlayer[node]+size)
#         break
#
# print average_shortest_path_length(G3)
# print average_shortest_path_length(G4)

# """
# This program is supposed to prompt for the dimension of a square bin and a data
# file containing numbers of squared blocks to be placed into the bin. It is
# supposed to be placed using the First Fit descending algorithm. It is currently
# only looping through and placing the first squared block but not continuing to go
# through and placing others
# """
#
# def isoneSpaceFree(_bin,row,col):
#     if col > len(_bin) or row > len(_bin):
#         return False
#     if _bin[row][col] == 0:
#         return True
#     else:
#         return False
# def isSpaceFree(_bin,row,col,value):
#     for r in range(value):
#         for c in range(value):
#             if not isoneSpaceFree(_bin,r,c):
#                 return False
#     return True
# def grid(i):
#     _bin = [[0 for col in range(i)] for row in range(i)]
#
#     return _bin
# def blockList():
#     L = []
#     for data in open('blockList.txt'):
#         L = (data.strip().split())
#     L = [int(i) for i in L]
#     L.sort(reverse = True)
#     return L
#
# def pack(blockList, _bin):
#     contained = []
#     notcontained =[]
#     for i in range(len(blockList)):
#         placements=placement(_bin,blockList[i])
#         _bin=placements[0]
#         if placements[1]==True:
#             contained.append(blockList[i])
#         else:
#             notcontained.append(blockList[i])
#     result = [_bin, contained, notcontained]
#     return result
# def placement(_bin, value):
#     for r in range(len(_bin)):
#         for c in range(len(_bin)):
#             if isSpaceFree(_bin,r,c,value):
#                 for height in range(value):
#                     for width in range(value):
#                         _bin[height][width] = value
#                 return [_bin,True]
#             else:
#                 continue
#     return [_bin,False]
#
# """
# square in contained subtract from grid in a for loop to calculate number of
# missing spaces.
# """
# def printgrid(_bin):
#     for j in range(len(_bin)):
#         for k in range(len(_bin)):
#             print(_bin[j][k])
#             print()
#
# def main():
#     i = int(input('Enter Square Bin Dimension: '))
#     filename = input('Block file: ')
#     L = []
#     for data in open(filename):
#         L = (data.strip().split())
#     L = [int(i) for i in L]
#     L.sort(reverse = True)
#     _bin = grid(i)
#     results = pack(L, _bin)
#     printgrid(results[0])
#
#
# if __name__ == '__main__':
#     main()
# def transfer(nums):
#     bit1 = int(nums[0]) << 24
#     bit2 = int(nums[1]) << 16
#     bit3 = int(nums[2]) << 8
#     bit4 = int(nums[3])
#     bit = bin(bit1 + bit2 + bit3 + bit4)[2:]
#     return bit
#
# i = 0
# a = 0
# b = 0
#
# rules = []
# ips = []
# Stop = 1
# while 1:
#     # if i > a+b:
#     #     break
#     line = sys.stdin.readline()
#     # if i == 0:
#     #    a = int(line.split()[0])
#     #    b = int(line.split()[1])
#     print 'hi', line
    # elif 0 < i <= a:
    #     rules.append(line.strip())
    # elif a < i <= a+b:
    #     ips.append(line.strip())
    # i += 1
#
#
# print rules
# print ips
#
# policy = {}
# deny = {}
#
#
# for rule in rules:
#     p = rule.split(' ')[0]
#     tmp = rule.split(' ')[1].split('/')
#     nums = tmp[0].split('.')
#
#     bit = transfer(nums)
#     if len(tmp) != 1:
#         mask = int(tmp[1])
#     else:
#         mask = 0
#     print nums, mask
#     if p == 'allow':
#
#         policy.setdefault(bit, (mask, 1))
#
#     else:
#         policy.setdefault(bit, (mask, 0))
#
# print policy
# for ip in ips:
#     bit = transfer(ip.split('.'))
#     print bit
#     if bit in policy:
#         if policy.get(bit)[1]:
#             print 'YES'
#         else:
#             print 'NO'
#
#     else:
#         find = 0
#         for k, v in policy.items():
#             mask = v[0]
#             if k[0:mask] == bit[0:mask]:
#                 if v[1] == 1:
#                     print 'YES'
#                 else:
#                     print 'NO'
#                 break
#
#         print 'NO'





