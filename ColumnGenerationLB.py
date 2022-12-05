from ImportData import *
import gurobipy as gb
import time

def SolveByCG(instance_index):
    [num_node, num_product, Q_product, num_vehicle, num_vehicle_product, Capacity, Size, cost, Demand] = GenerateInstanceFromFile(instance_index)
    U = 5
    # num_vehicle = 45
    # build master model
    master = gb.Model()
    f = {}
    demand_cons = {}
    vehicle_cons = None
    for i in range(num_node):
        for j in range(num_product):
            f[i*num_product+j] = master.addVar(obj = cost[0,i]+cost[i,0], vtype = gb.GRB.CONTINUOUS,  name="route[%d]"%(i*num_product+j))
            # demand_cons[i*num_product+j] = master.addConstr(int(np.ceil(sum(Demand[j][i]for i in range(num_node))/num_vehicle_product[j]))*f[i*num_product+j] >= Demand[j][i], name="demand[%d]"%(i*num_product+j))
    for i in range(num_node):
        for j in range(num_product):
            demand_cons[i*num_product+j] = master.addConstr(np.ceil(sum(sum(Demand[j][i] for i in range(num_node)) for j in range(num_product))/num_vehicle)*f[i*num_product+j] >= Demand[j][i], name="demand[%d]"%(i*num_product+j))
    f[num_node*num_product] = master.addVar(obj = cost[0,1]+cost[1,2]+cost[2,0], lb = 0, ub = 1, vtype = gb.GRB.CONTINUOUS, name="route[%d]"%((num_node-1)*num_product))
    vehicle_cons = master.addConstr(gb.quicksum(f[i] for i in range(num_node*num_product+1)) == num_vehicle)
    master.update()

    num_var = num_node*num_product+1
    route = {}
    cost_value = {}
    start = time.time()
    while 1:
        master.optimize()
        lambda_ = [demand_cons[i].Pi for i in range(num_node*num_product)]
        pi_ = vehicle_cons.Pi
        lb = master.objval

        sub = gb.Model()
        x = sub.addVars(num_node, num_node, vtype = gb.GRB.BINARY)
        # x = sub.addVars(num_node, num_node, vtype = gb.GRB.CONTINUOUS)
        y = sub.addVars(num_node, num_product, vtype = gb.GRB.INTEGER)
        y = sub.addVars(num_node, num_product, vtype = gb.GRB.CONTINUOUS)
        mu = sub.addVars(num_node-1)
        sub.setObjective(gb.quicksum(gb.quicksum(x[i,j]*cost[i,j] for j in range(num_node)) for i in range(num_node)) - gb.quicksum(gb.quicksum(y[i,l]*lambda_[i*num_product+l] for l in range(num_product)) for i in range(num_node)) - pi_)
        sub.addConstrs(x[i,i] == 0 for i in range(num_node))
        sub.addConstrs(x.sum('*',i) == x.sum(i,'*') for i in range(num_node))
        sub.addConstr(x.sum('*',0) >= 1)
        for i in range(1,num_node):
            for j in range(1,num_node):
                if j != i:
                    sub.addConstr(mu[i-1]-mu[j-1]+(num_node)*x[i,j] <= num_node-1)
        sub.addConstrs(y[i,l] <= Demand[l][i]*gb.quicksum(x[i,j] for j in range(num_node)) for i in range(1,num_node) for l in range(num_product))
        # sub.addConstr(gb.quicksum(y[i,l] for i in range(num_node)) >= sum(Demand[l][i] for i in range(num_node)) - (num_vehicle-1)*Q_product[l] for l in range(num_product))
        sub.addConstr(gb.quicksum(Size[l]*gb.quicksum(y[i,l] for i in range(num_node)) for l in range(num_product)) <= Capacity)
        sub.Params.Timelimit = 10
        sub.optimize()

        if sub.objval >= -0.001:
            break
        
        x_value = sub.getAttr('X', x)
        y_value = sub.getAttr('X', y)
        """ for ii in range(num_node):
            for jj in range(num_node):
                if x_value[ii,jj] != 0:
                    print((ii,jj))
        print(y_value[42,0]) """
        route[num_var] = x_value
        cost_value[num_var] = sum(sum(x_value[i,j]*cost[i,j] for j in range(num_node)) for i in range(num_node))
        col = gb.Column()
        for i in range(num_node):
            for l in range(num_product):
                col.addTerms(y_value[i,l], demand_cons[i*num_product+l])
        col.addTerms(1, vehicle_cons)
        f[num_var] = master.addVar(obj=sum(sum(x_value[i,j]*cost[i,j] for j in range(num_node)) for i in range(num_node)), lb = 0, ub = 1, vtype = gb.GRB.CONTINUOUS, name="route[%d]"%num_var, column=col)
        master.update()
        num_var += 1

        end = time.time()
        if (end-start >= 720):
            break
    
    """ for i in range(num_var):
        f[i].vtype = gb.GRB.INTEGER
    master.optimize()
    for i in range(num_var):
        print(f[i].x,end=',') """
    """ print("\n")
    for i in range(num_var):
        if f[i].x == 1:
            print(i, end=',')
            for ii in range(num_node):
                for jj in range(num_node):
                    if route[i][ii,jj] != 0:
                        print((ii,jj))
            print(cost_value[i]) """
            
    # ub = master.objval
    end = time.time()

    f = open('log/S' + str(num_node) + 'D' + str(num_product) + '_CG.log', 'a+')
    print("lower bound is ", lb, file = f)
    # print("upper bound is ", ub)
    print("number of iterations is ", num_var-(num_node*num_product+1), file = f)
    print("total time is ", end - start, file = f)
    f.close()

if __name__ == "__main__":
    SolveByCG(3)
    SolveByCG(0)
    SolveByCG(1)
