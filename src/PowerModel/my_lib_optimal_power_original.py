__author__ = 'Diman'

from gurobipy import *

# Model data
def optimal_ILP_power(nodes, power, link1, link2, linkNum):
    flows = []
    cost = []
    ILP_gen_power = []
    ILP_load_power = []
    #########################GREEEDY BASED APPROACH###############################
    flows, ILP_gen_power, ILP_load_power, cost = ILP_solution_best(nodes, power, link1, link2, linkNum)

    return flows, ILP_gen_power, ILP_load_power, cost
###
# Solve ILP of max flow problem where the Sets are given and each set can identify a set of links,

def ILP_solution_best(nodes, power, link1, link2, linkNum):
    #Power_gen_t = []
    #Power_load_t = []
    my_flows = []
    ILP_gen = []
    ILP_load = []
    cost = []
    w_g = 1
    w_l = 200
    Max_Thr = 1#1.5
    Min_Thr = -1#1.5
    P_g_max = 1
    P_g_min = -1
    P_l_max = -1
    P_l_min = 1
    #########################GREEEDY BASED APPROACH###############################
    #Best_greedy=0
    #Best_greedy_monitors=[]
    #Identified_links=[]
    #Edges=[]
    class Node():#(s,d,m):
        def __init__(self, s, d, m, number, node_number):
            edge=(s, d)
            self.e = edge # .append(edge)
            self.m = m
            self.n = number
            self.node_num = node_number
        def AddComb(self, edge):
            edges = []
            for e in self.e:
                if (e != ([], [])):
                    if (e != []):
                        edges.append(e)
            #if edges[0] ==([],[]):
            #    edges.remove(edges[0])
            edges.append(edge)
            self.e = edges
        def RemComb(self, edge):
            edges = []
            for e in self.e:
                edges.append(e)
            if (self.e != ([], [])):
                edges.remove(([], []))
            self.e = edges
    ########################################    
    class Monitors_Perm():
        def __init__(self,edges,m,number):
            self.ident= edges
            self.num=number
            self.monitors= m


    my_objects = []
    Edge_index=0
    Node_index = 0
    for i in range(0, 310):
    #for i in range(0,3):
        my_objects.append(Node([], [],Node_index, Node_index, Node_index ))
        Node_index = Node_index + 1


    for m in range(0, len(link1)):
        for k in range(0, 310):
        #for k in range(0, 3):
            #print 'KKKKKKKKKKKKKK'
            #print k
            if ((k+1)== link1[m]):# or (k == link2[m])):
                edge = (k+1, link2[m])
                my_objects[k].AddComb(edge)
                #Diman Commented:
                ###print 'my_objects[k].e'
                ###print my_objects[k].e
                ###print 'K:'
                ###print k
                #my_objects[k].AddComb(edge)
                ##my_objects[k].e.append(edge)
            if ((k+1)== link2[m]):
                edge = (link1[m], k+1)
                my_objects[k].AddComb(edge)
                #Diman Commented:
                ###print 'my_objects[k].e'
                ###print my_objects[k].e
                ###print 'K 2:'
                ###print k
                #my_objects[k].AddComb(edge)
    """    
    for obj in my_objects:
        print obj.e
        #print obj.m
        #print obj.n
        #if obj.n not in Edges:
        #    Edges.append(obj.n)
    """
    my_Model = Model('DCPowerflow')
    P_g_t = {}
    P_l_t = {}
    flows = {}
    P_j_t = {}
    ILP_gen_power = []
    ILP_load_power = []
    #for p in range(0,2):
    for p in range(0, 113):
        P_g_t[p] = my_Model.addVar(ub=2, lb=0, vtype=GRB.CONTINUOUS, name='GeneratorPower%s'% (p)) 
    #for e in range(2, 3):
    for e in range(113, 210):
        P_l_t[e] = my_Model.addVar(ub=0, lb=-2, vtype=GRB.CONTINUOUS, name='LoadPower%s'% (e))
    for k in range(210, 310):
    #for k in range(0,0):
        P_j_t[k] = my_Model.addVar(ub=2, lb=-2, vtype=GRB.CONTINUOUS, name='JunctionPower%s'% (k))
    theEdges= []
    for m in range(0, len(link1)):
        i = link1[m]
        j = link2[m]
        edge= (i,j)
        if edge not in theEdges:
            theEdges.append(edge)
            #print 'i,j:'
            #print i,j
            flows[i,j,1] = my_Model.addVar(ub=Max_Thr, lb=Min_Thr, vtype=GRB.CONTINUOUS, name='Flow_%s_%s_%s'% (i,j,1))
            flows[j,i,1] = my_Model.addVar(ub=Max_Thr, lb=Min_Thr, vtype=GRB.CONTINUOUS, name='Flow_%s_%s_%s'% (j,i,1)) 
        if edge in theEdges:
            flows[i,j,2] = my_Model.addVar(ub=Max_Thr, lb=Min_Thr, vtype=GRB.CONTINUOUS, name='Flow_%s_%s_%s'% (i,j,2))
            flows[j,i,2] = my_Model.addVar(ub=Max_Thr, lb=Min_Thr, vtype=GRB.CONTINUOUS, name='Flow_%s_%s_%s'% (j,i,2))
        #print 'theEdges'
        #print theEdges
    """
    for h in demand_flows:
        for i,j in arcs:
            #CREO LE VARIABILI CHE MI DICONO QUANTO FLUSSO H PASSA TRA I E J
            flow[h,i,j] = m.addVar(ub=capacity[i,j], obj=0.0, vtype=GRB.CONTINUOUS,
                                   name='flow_%s_%s_%s' % (h, i, j))
            flow[h,j,i] = m.addVar(ub=capacity[i,j], obj=0.0, vtype=GRB.CONTINUOUS,
                                   name='flow_%s_%s_%s' % (h, j, i))
    """
    my_Model.update()
    for i in range(0, 113):
    #for i in range(0,2):
        my_Model.addConstr(0 <= P_g_t[i], 'Non_Negative_Power_%s'% (i) ) #power[i] - 0.0001
        #my_Model.update()
    for j in range(0, 113):
    #for j in range(0,2):
        my_Model.addConstr(P_g_t[j] <= P_g_max, 'Max_Gen_Power_%s'% (j))
        #my_Model.update()
    #Load constraints
    for i in range(113, 210):
    #for i in range(2, 3):
        my_Model.addConstr(power[i] <= P_l_t[i] , 'Non_Negative_Power_%s'% (i))
        #my_Model.update()
    for j in range(113, 210):
    #for j in range(2, 3):
        my_Model.addConstr(P_l_t[j] <=0 , 'Max_Load_Power_%s'% (j))
    #Diman commented two lines
    for k in range(210, 310):
        my_Model.addConstr(P_j_t[k] == power[k], 'Junction_Power_%s'% (k))
        #my_Model.update()
    #Load line capacities:
    theEdges= []
    for m in range(0, len(link1)):
        #for j in range(0, 210):
        i= link1[m]
        j = link2[m]
        edge = (i,j)
        if edge not in theEdges:
            theEdges.append(edge)
            my_Model.addConstr(Min_Thr <= flows[i,j,1], 'Min_Flow_Thr1_%s'% (m))
            #my_Model.update()
            my_Model.addConstr(flows[i,j,1] <= Max_Thr, 'Max_Flow_Thr1_%s'% (m))
            #my_Model.update()
            my_Model.addConstr(flows[j,i,1] <= Max_Thr, 'Max_Flow_Thr2_%s'% (m))
            #my_Model.update()
            my_Model.addConstr(Min_Thr <= flows[j,i,1], 'Min_Flow_Thr2_%s'% (m))
            #my_Model.update()
            my_Model.addConstr(flows[i,j,1] + flows[j,i,1] == 0, 'Flows_dir_%s'% (m))
            #my_Model.update()
        if edge in theEdges:
            #my_Model.rem
            my_Model.addConstr(Min_Thr <= flows[i,j,2], 'Min_Flow_Thr1_%s'% (m))
            #my_Model.update()
            my_Model.addConstr(flows[i,j,2] <= Max_Thr, 'Max_Flow_Thr1_%s'% (m))
            #my_Model.update()
            my_Model.addConstr(flows[j,i,2] <= Max_Thr, 'Max_Flow_Thr2_%s'% (m))
            #my_Model.update()
            my_Model.addConstr(Min_Thr <= flows[j,i,2], 'Min_Flow_Thr2_%s'% (m))
            #my_Model.update()
            my_Model.addConstr(flows[i,j,2] + flows[j,i,2] == 0, 'Flows_dir_%s'% (m))
            #my_Model.update()
            
    ###Flow Conservation:
    my_Model.addConstr((quicksum(P_g_t[l] for l in range(0,113)) + quicksum(P_l_t[j] for j in range(113, 210))) == 0, 'ConsumedGeneratedPower')
    #my_Model.addConstr((quicksum(P_g_t[l] for l in range(0,2)) + quicksum(P_l_t[j] for j in range(2, 3))) == 0, 'ConsumedGeneratedPower')

    my_Model.update()
    #Flow Conservation constraint:
    #theEdges = []
    for k in range(0, 113):
    #for k in range(0,2):
        edges =[]
        theEdges =[]
        if (my_objects[k].e != ([], [])):
            #Diman Commented:
            ###print 'my_objects[k].e'
            ###print my_objects[k].e
            for (i,j) in my_objects[k].e:
                if (i == k+1):
                    e = (i,j)
                    if e not in edges:
                        theEdges.append((i,j,1))
                        edges.append(e)
                    else: #if e in edges:
                        edges.append(e)
                        theEdges.append((i,j,2))
                if (j == k+1):
                    e = (j,i)
                    if e not in edges:
                      edges.append(e)
                      theEdges.append((j,i,1))
                    else: #if e in edges:
                      edges.append(e)
                      theEdges.append((j,i,2))
            #Diman Commented:
            ###print 'INJAAAAAAAAAAA:'
            ###print theEdges
            #for (e,f,g) in theEdges:
            #    print e,f,g
            #my_Model.addConstr(sum(flows[k,f,g] for (k,f,g) in theEdges) == P_g_t[k], 'Gen_FlowConservation_%s'% (k))
            if (theEdges !=[]):
                my_Model.addConstr(sum(flows[k,f,g] for (k,f,g) in theEdges) == P_g_t[k], 'Gen_FlowConservation_%s'% (k))
                my_Model.update()
            else:
                my_Model.addConstr(P_g_t[k] == power[k], 'Gen_FlowConservation_%s'% (k))
                my_Model.update()
    #Load flow conservation:
    for k in range(113, 210):
    #for k in range(2,3):
        edges =[]
        theEdges =[]
        if (my_objects[k].e != ([], [])):
            #Diman Commented:
            ###print 'my_objects[k].e'
            ###print my_objects[k].e
            for (i,j) in my_objects[k].e:
                if (i == k+1):
                    e = (i,j)
                    if e not in edges:
                        theEdges.append((i,j,1))
                        edges.append(e)
                    else: #if e in edges:
                        edges.append(e)
                        theEdges.append((i,j,2))
                if (j == k+1):
                    e = (j,i)
                    if e not in edges:
                      edges.append(e)
                      theEdges.append((j,i,1))
                    else: # e in edges:
                      edges.append(e)
                      theEdges.append((j,i,2))
            #Diman Commented:
            ###print 'Power INJAAAAAAAAAAAA:'
            ###print theEdges
            #my_Model.addConstr(quicksum(flows[e,f,g] for (e,f,g) in theEdges) == power[k] , 'Load_FlowConservation_%s'% (k) )
            if (theEdges !=[]):
                my_Model.addConstr(sum(flows[k,f,g] for (k,f,g) in theEdges) == P_l_t[k] , 'Load_FlowConservation_%s'% (k))
                #my_Model.addConstrs((flows.sum(e,f,g)  == P_l_t[k] for (e,f,g) in theEdges for k in range(113,210)), "node")
                my_Model.update()
            else:
                my_Model.addConstr( P_l_t[k] == 0 , 'Load_FlowConservation_%s'% (k))
                my_Model.update()
    #m.addConstr( (quicksum(flow[h,k,i] for k,i in to_i) + inflow[h,i]) == (quicksum(flow[h,i,j] for i,j in from_i)),'node_%s_%s' % (h, i))
    #Junction flow conservation:
    #Diman commented
    """ 
    for k in range(210, 310):
        edges =[]
        theEdges =[]
        if (my_objects[k].e != ([], [])):
            print 'my_objects[k].e'
            print my_objects[k].e
            for (i,j) in my_objects[k].e:
                if (i == k+1):
                    e = (i,j)
                    if e not in edges:
                        theEdges.append((i,j,1))
                        edges.append(e)
                    else: #if e in edges:
                        edges.append(e)
                        theEdges.append((i,j,2))
                if (j == k+1):
                    e = (j,i)
                    if e not in edges:
                      edges.append(e)
                      theEdges.append((j,i,1))
                    else: #if e in edges:
                      edges.append(e)
                      theEdges.append((j,i,2))
            #if power[k] >0:
            print 'Junction INJAAAAAAAAAAAAAA:'
            print theEdges
            my_Model.addConstr(quicksum(flows[e,f,g] for (e,f,g) in theEdges ) == P_j_t[k], 'Jun_FlowConservation_%s'% (k))
            #if power[k] <=0:
            #    my_Model.addConstr(quicksum(flows[i,j,k] for (i,j,k) in theEdges ) + power[k] == 0, 'Gen_FlowConservation')
    """
    #my_M del.update()
    #    for j in range(0, 210):
    #        for k in range(0, len(link1)):
    #            if (i == link1[k]) and (j == link2[k]):

    ##for obj in my_objects:
    ##    my_Model.addConstr(quicksum(flows[obj.e,j] for j in obj. )== power[m])
    

    my_Model.update()
    #my_Model.optimize()

    my_Model.setObjective(w_g*(sum((P_g_t[l] - power[l] ) for l in range(0,113)))+w_l*(sum((P_l_t[l] - power[l]) for l in range(113,210))), GRB.MINIMIZE)
    #my_Model.setObjective(w_g*(quicksum((P_g_t[l]-power[l] ) for l in range(0,2)))+w_l*(quicksum((P_l_t[l] - power[l]) for l in range(2,3))), GRB.MINIMIZE)

    my_Model.update()
    my_Model.optimize()
    ###################################################################
    if my_Model.status == GRB.status.OPTIMAL:
        ILP_flows=[]
        ILP_gen_power=[]
        for p in range(0, 113):
        #for p in range(0,2):
            var_reference = my_Model.getVarByName('GeneratorPower%s'% (p)) # ('GeneratorPower%s'%(i)) #Generator's power
            #Diman Commented
            ###print 'var_reference'
            ###print var_reference.x
            ILP_gen_power.append(var_reference.x)
            #if var_reference.x>0:
                #Diman Commented:
                ###print 'Generator Power:'
                ###print var_reference.x
                #ILP_gen_power.append(p)
                #print 'Generator Power:'
                #print ILP_gen_power
        ILP_load_power=[]
        for e in range(113, 210):
        #for e in range(2,3):
            var_reference = my_Model.getVarByName('LoadPower%s'% (e)) #('LoadPower%s'% (e)) #Load's Power
            #Diman Commented:
            ###print 'var_reference_power:'
            ###print var_reference.x
            ILP_load_power.append(var_reference.x)
            if var_reference.x>0:
                #Diman Commented:
                ###print var_reference.x
                ILP_load_power.append(e)
                #Diman Commented:
                ###print 'Load Power:'
                ###print ILP_load_power

    #Find the flows:
        theEdges =[]
        """
        for m in range(0, len(link1)):
            i = link1[m]
            j = link2[m]
            e = (i,j)
            if e not in theEdges:
                theEdges.append(e)
                #print 'i,j'
                #print i,j
                my_flow = my_Model.getVarByName('Flow_%s_%s_%s'%(i,j,1))
                my_flow_reverse = my_Model.getVarByName('Flow_%s_%s_%s'%(j,i,1))
            if e in theEdges:
                my_flow = my_Model.getVarByName('Flow_%s_%s_%s'%(i,j,2))
                my_flow_reverse = my_Model.getVarByName('Flow_%s_%s_%s'%(j,i,2))
            print 'my_flow.x:'
            print my_flow.x
            #print 'my_flow_reverse.x:'
            #print my_flow_reverse.x
            print 'i,j:'
            print i,j
            if my_flow.x>0 or my_flow_reverse.x>0:
                #print 'MY_FLOW.X:'
                #print my_flow.x
                edge = (i,j)
                #print 'i,j:'
                #print edge
                ILP_flows.append(edge)
        """
        #Add the generator's power to the results:
        ILP_gen = []
        gen_sol = my_Model.getAttr('x', P_g_t)
        for h in range(0, 113):
            ILP_gen.append(gen_sol[h])
        #Add the load's power to the results:
        ILP_load = []
        load_sol = my_Model.getAttr('x', P_l_t)
        for h in range(113, 210):
            ILP_load.append(load_sol[h])
        #Add the flows of the lines to the results:
        solution = my_Model.getAttr('x', flows)
        theEdges = []
        for h in range(0, len(link1)):
            i = link1[h]
            j = link2[h]
            e = (i,j)
            if e not in theEdges:
                theEdges.append(e)
                f = 1
            else:
                f =2
            #Diman Commented:
            ###print('\nOptimal flows for %s_%s:' % (i,j))
            #for i,j in arcs:
            #    if solution[h,i,j] > 0:
            #Diman Commented:
            ###print('%s -> %s, %s: %g' % (i, j, f, solution[i,j,f]))
            my_flows.append(solution[i,j,f])
        cost =[]
        cost = my_Model.objVal
        print 'Solution:'
        print('The optimal objective is %g' % my_Model.objVal)
    #Find the flows:

    return my_flows, ILP_gen, ILP_load, cost #ILP_gen_power, ILP_load_power, cost #ILP_flows#flows

