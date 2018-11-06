#!/usr/bin/env python
# coding: utf-8
# created by hevlhayt@foxmail.com 
# Date: 2016/4/12 
# Time: 10:42
#
#answer
#R R D L L U R R R D L L U R D D L D R U R D L U L L D R U U L U

# when we reach the target of the plan, we use trace function to iterate in the movement trace
def trace(node):

    if node['prev'] != None:
        trace(node['prev'])
    else:
        return
    r1, c1 = node['prev']['row'], node['prev']['col']
    r2, c2 = node['row'], node['col']
    if r2 == r1 - 1:
        print 'U',
    elif r2 == r1 + 1:
        print 'D',
    elif c2 == c1 - 1:
        print 'L',
    else:
        print 'R',

#swap node(r1, c1) and node(r2, c2), return new state string
def swap(state, r1, c1, r2, c2):
    m, n = list(sorted([r1 * 4 + c1, r2 * 4 + c2]))
    return state[:m] + state[n] + state[m+1:n] + state[m] + state[n+1:]


def move(row, col):
    if row >= 0 and row < 4 and col >= 0 and col < 4:
        state = swap(s, r, c, row, col)
        #if current state not in visited, we add it to visited, and we add it to dfs queue
        if state not in visited:
            visited.add(state)
            q.append(dict(state=state, row=row, col=col, prev=cur))

#4*4 plan are represented by a string, 2-white, 0-red, 1-blue
start = dict(state='2011001100110011', row=0, col=0, prev=None)
target = '2101101001011010'

#dfs queue
q = [start]

#visited states
visited = set(start['state'])

i = 0
while i < len(q):
    cur = q[i]
    i += 1
    s, r, c = cur['state'], cur['row'], cur['col']
    # print s,r,c
    #if we find the target state, we use the trace function to print the movement trace
    if s == target:
        trace(cur)
        break

    #dfs move to search the target state
    move(r - 1, c)
    move(r + 1, c)
    move(r, c - 1)
    move(r, c + 1)


