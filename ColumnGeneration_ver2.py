from ImportData import *
import gurobipy as gb
import time

def SolveByCG(instance_index):
    [num_node, num_product, Q_product, num_vehicle, num_vehicle_product, Capacity, Size, cost, Demand] = GenerateInstanceFromFile(instance_index)
    U = 1000

    # generate initial solution
    y_pre = np.zeros(((num_node-1)*num_product, num_vehicle))
    cost_pre_comp = np.zeros((num_vehicle, num_product))
    cost_pre = np.zeros(num_vehicle)
    Demand_pre = Demand.copy()
    for l in range(num_product):
        i = 1
        pass_i = []
        v = 1
        cur_p = 0
        num_v = 1
        while (i < num_node):
            if cur_p + Demand_pre[l][i] <= Q_product[l]:
                if Demand_pre[l][i] != 0:
                    y_pre[(i-1)*num_product+l][v-1] = Demand_pre[l][i]
                    pass_i.append(i)
                """ if Demand_pre[l][i] == 0:
                    cost_pre[(i-1)*num_product+l] = cost[0,i]+cost[i,0] """
                    # start_i += 1
                    # v = v+1
                i = i+1
                cur_p = sum(y_pre[(j-1)*num_product+l][v-1] for j in pass_i)
            else:
                if cur_p == Q_product[l]:
                    # for k in range(start_i, i):
                    cost_pre_comp[v-1,l] = sum(cost[pass_i[j], pass_i[j+1]] for j in range(len(pass_i)-1)) + cost[0,pass_i[0]] + cost[pass_i[len(pass_i)-1],0]
                    cur_p = 0
                    # start_i = i
                    v = v+1
                    num_v += 1
                    pass_i = []
                else:
                    Demand_pre[l][i] = Demand_pre[l][i] - (Q_product[l]-cur_p)
                    y_pre[(i-1)*num_product+l][v-1] = Q_product[l] - cur_p
                    # for k in range(start_i, i+1):
                    # cost_pre[(v-1)*num_product+l] = sum(cost[start_i,j] for j in range(i+1)) + cost[0,start_i] + cost[i,0]
                    pass_i.append(i)
                    cost_pre_comp[v-1,l] = sum(cost[pass_i[j], pass_i[j+1]] for j in range(len(pass_i)-1)) + cost[0,pass_i[0]] + cost[pass_i[len(pass_i)-1],0]
                    cur_p = 0
                    # start_i = i
                    v = v+1
                    num_v += 1
                    pass_i = []
                
                """ while v < i:
                    v = v+1 """
                """ while v < i:
                    y_pre[(v-1)*num_product+l][(v-1)*num_product+l] = Demand[l][v]
                    cost_pre[(v-1)*num_product+l] = cost[0,v]+cost[v,0]
                    v = v+1 """
        """ while v < i-1:
            v = v+1
            y_pre[(v-1)*num_product+l][(v-1)*num_product+l] = Demand[l][v]
            cost_pre[(v-1)*num_product+l] = cost[0,v]+cost[v,0] """
        """ for i in range(num_node):
            if y_pre[(i-1)*num_product+l][(i-1)*num_product+l] == 0:
                y_pre[(i+num_vehicle-1)*num_product+l][(i+num_vehicle-1)*num_product+l] = Demand[l][i]
                cost_pre[(i-1)*num_product+l] = cost[0,i]+cost[i,0] """
    for v in range(num_vehicle):
        cost_pre[v] = max(cost_pre_comp[v,:])
    num_vehicle = 41
    # build master model
    master = gb.Model()
    f = {}
    demand_cons = {}
    vehicle_cons = None
    for i in range(num_vehicle):
        f[i] = master.addVar(obj = cost_pre[i], vtype = gb.GRB.CONTINUOUS, name="route[%d]"%(i))
    for i in range(1,num_node):
        for j in range(num_product):
            # f[(i-1)*num_product+j] = master.addVar(obj = sum(cost[ii,ii+1] for ii in range(i, num_node-1)) + cost[0,i] + cost[num_node-1,0], lb = 0, ub = 1, vtype = gb.GRB.CONTINUOUS,  name="route[%d]"%((i-1)*num_product+j))
            
            # f[(i-1)*num_product+j] = master.addVar(obj = cost_pre[(i-1)*num_product+j], lb = 0, ub = 1, vtype = gb.GRB.CONTINUOUS,  name="route[%d]"%((i-1)*num_product+j+num_vehicle))
            f[(i-1)*num_product+j+num_vehicle] = master.addVar(obj = cost[0,i]+cost[i,0], vtype = gb.GRB.CONTINUOUS,  name="route[%d]"%((i-1)*num_product+j+num_vehicle))
            # demand_cons[i*num_product+j] = master.addConstr(int(np.ceil(sum(Demand[j][i]for i in range(num_node))/num_vehicle_product[j]))*f[i*num_product+j] >= Demand[j][i], name="demand[%d]"%(i*num_product+j))
    for i in range(1,num_node):
        for j in range(num_product):
            # demand_cons[(i-1)*num_product+j] = master.addConstr(Demand[j][i]*f[(i-1)*num_product+j] >= Demand[j][i], name="demand[%d]"%((i-1)*num_product+j+num_vehicle))
            # demand_cons[(i-1)*num_product+j] = master.addConstr(gb.quicksum(y_pre[(i-1)*num_product+j][(k-1)*num_product+j]*f[(k-1)*num_product+j] for k in range(1,num_node)) >= Demand[j][i], name="demand[%d]"%((i-1)*num_product+j))
            # demand_cons[i*num_product+j] = master.addConstr(int(np.ceil(sum(Demand[j][ii]for ii in range(num_node))/num_vehicle_product[j]))*f[i*num_product+j] >= Demand[j][i], name="demand[%d]"%(i*num_product+j))
            # demand_cons[(i-1)*num_product+j] = master.addConstr(gb.quicksum(int(np.ceil(sum(Demand[j][k]for k in range(num_node))/num_vehicle_product[j]))*f[ii*num_product+j] for ii in range(i)) >= Demand[j][i], name="demand[%d]"%((i-1)*num_product+j))
            # demand_cons[(i-1)*num_product+j] = master.addConstr(gb.quicksum(int(np.ceil((Q_product[j] - Demand[j][ii+1])/(num_node-ii)))*f[ii*num_product+j] for ii in range(i-1)) + Demand[j][i]*f[(i-1)*num_product+j] >= Demand[j][i], name="demand[%d]"%((i-1)*num_product+j))
            # demand_cons[i*num_product+j] = master.addConstr(gb.quicksum(Q_product[j]*f[ii*num_product+j] for ii in range(num_node)) - Q_product[j]*f[i*num_product+j] 
                # + (sum(Demand[j][k]for k in range(num_node))-(num_vehicle_product[j]-1)*Q_product[j])*f[i*num_product+j] >= Demand[j][i], name="demand[%d]"%(i*num_product+j))
            demand_cons[(i-1)*num_product+j] = master.addConstr(gb.quicksum(y_pre[(i-1)*num_product+j][v]*f[v] for v in range(num_vehicle))+Demand[j][i]*f[(i-1)*num_product+j+num_vehicle] >= Demand[j][i], name="demand[%d]"%((i-1)*num_product+j))
    # f[(num_node-1)*num_product+num_vehicle] = master.addVar(obj = cost[0,1]+cost[1,2]+cost[2,0], lb = 0, ub = 1, vtype = gb.GRB.CONTINUOUS, name="route[%d]"%((num_node-1)*num_product))
    # prob = master.addVar(lb=0, ub=1)
    vehicle_cons = master.addConstr(gb.quicksum(f[i] for i in range((num_node-1)*num_product+num_vehicle)) == num_vehicle)
    master.update()

    num_var = (num_node-1)*num_product+num_vehicle
    route = {}
    cost_value = {}
    start = time.time()
    while 1:
        master.optimize()
        lambda_ = [demand_cons[i].Pi for i in range((num_node-1)*num_product)]
        pi_ = vehicle_cons.Pi

        sub = gb.Model()
        x = sub.addVars(num_node, num_node, vtype = gb.GRB.BINARY)
        y = sub.addVars(num_node, num_product, vtype = gb.GRB.INTEGER)
        mu = sub.addVars(num_node-1)
        sub.setObjective(gb.quicksum(gb.quicksum(x[i,j]*cost[i,j] for j in range(num_node)) for i in range(num_node)) - gb.quicksum(gb.quicksum(y[i,l]*lambda_[(i-1)*num_product+l] for l in range(num_product)) for i in range(1,num_node)) - pi_)
        sub.addConstrs(x[i,i] == 0 for i in range(num_node))
        sub.addConstrs(x.sum('*',i) == x.sum(i,'*') for i in range(num_node))
        sub.addConstr(x.sum('*',0) == 1)
        for i in range(1,num_node):
            for j in range(1,num_node):
                if j != i:
                    sub.addConstr(mu[i-1]-mu[j-1]+(num_node)*x[i,j] <= num_node-1)
        sub.addConstrs(y[i,l] <= Demand[l][i]*gb.quicksum(x[i,j] for j in range(num_node)) for i in range(1,num_node) for l in range(num_product))
        sub.addConstrs(gb.quicksum(y[i,l] for i in range(num_node)) >= sum(Demand[l][i] for i in range(num_node)) - (num_vehicle-1)*Q_product[l] for l in range(num_product))
        sub.addConstr(gb.quicksum(Size[l]*gb.quicksum(y[i,l] for i in range(num_node)) for l in range(num_product)) <= Capacity)
        sub.optimize()

        if sub.objval >= -0.001:
            break
        
        x_value = sub.getAttr('X', x)
        y_value = sub.getAttr('X', y)
        for ii in range(num_node):
            for jj in range(num_node):
                if x_value[ii,jj] != 0:
                    print((ii,jj))
        print(y_value[24,l] for l in range(num_product))
        route[num_var] = x_value
        cost_value[num_var] = sum(sum(x_value[i,j]*cost[i,j] for j in range(num_node)) for i in range(num_node))
        col = gb.Column()
        for i in range(1,num_node):
            for l in range(num_product):
                col.addTerms(y_value[i,l], demand_cons[(i-1)*num_product+l])
        col.addTerms(1, vehicle_cons)
        f[num_var] = master.addVar(obj=sum(sum(x_value[i,j]*cost[i,j] for j in range(num_node)) for i in range(num_node)), lb = 0, ub = 1, vtype = gb.GRB.CONTINUOUS, name="route[%d]"%num_var, column=col)
        master.update()
        num_var += 1

    lb = master.objval
    for i in range(num_var):
        f[i].vtype = gb.GRB.INTEGER
    master.optimize()
    for i in range(num_var):
        print(f[i].x,end=',')
    print("\n")
    for i in range(num_var):
        if f[i].x == 1:
            print(i, end=',')
            """ for ii in range(num_node):
                for jj in range(num_node):
                    if route[i][ii,jj] != 0:
                        print((ii,jj))
            print(cost_value[i]) """
            
    ub = master.objval
    end = time.time()

    print("lower bound is ", lb)
    print("upper bound is ", ub)
    print("number of iterations is ", num_var-(num_node*num_product+1))
    print("total time is ", end - start)

if __name__ == "__main__":
    SolveByCG(0)
