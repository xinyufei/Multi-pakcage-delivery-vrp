from ImportData import * 
import gurobipy as gb

def H2(instance_index):
    [num_node, num_product, Q_product, num_vehicle, num_vehicle_product, Capacity, Size, cost, Demand] = GenerateInstanceFromFile(instance_index)
    num_vehicle_ub = num_product*num_node
    Q_product = [int(Capacity/Size[l]) for l in range(num_product)]
    num_vehicle_product = [int(np.ceil(sum(Demand[l][i] for i in range(num_node))/Q_product[l])) for l in range(num_product)]
    num_vehicle = sum(num_vehicle_product)
    
    # knapsack
    kn = gb.Model()
    Q = kn.addVars(num_vehicle_ub, num_product, vtype=gb.GRB.INTEGER)
    v = kn.addVars(num_vehicle_ub, vtype = gb.GRB.BINARY)
    kn.setObjective(gb.quicksum((k+1)*v[k] for k in range(num_vehicle_ub)))
    kn.addConstrs(gb.quicksum(Q[k,l]*Size[l] for l in range(num_product)) <= Capacity*v[k] for k in range(num_vehicle_ub))
    kn.addConstrs(gb.quicksum(Q[k,l] for k in range(num_vehicle_ub)) >= sum(Demand[l][i] for i in range(num_node)) for l in range(num_product))
    kn.optimize()
    Q_value = kn.getAttr('X', Q)
    v_value = kn.getAttr('X', v)

    num_vehicle = int(sum(v_value[k] for k in range(num_vehicle_ub)))

    cost_re = np.zeros(num_product)
    #  for l in range(num_product):
    # num_vehicle = int(sum(v_value[k] for k in range(num_vehicle_ub)))
    # num_vehicle = num_vehicle_product[l]
    U = 5
    m = gb.Model()
    x = m.addVars(num_node, num_node, num_vehicle, vtype = gb.GRB.BINARY)
    # x = m.addVars(num_node, num_node, num_vehicle, vtype = gb.GRB.CONTINUOUS)
    # u = m.addVars(num_vehicle, vtype = gb.GRB.BINARY)
    # u = m.addVars(num_vehicle, vtype = gb.GRB.CONTINUOUS)
    mu = m.addVars(num_node-1)
    # y = m.addVars(num_node, num_product, num_vehicle, vtype = gb.GRB.INTEGER)
    m.setObjective(gb.quicksum(gb.quicksum(gb.quicksum(x[i,j,k] for k in range(num_vehicle))*cost[i,j] for j in range(num_node)) for i in range(num_node)))
    m.addConstrs(gb.quicksum(gb.quicksum(x[i,j,k] for j in range(num_node)) for k in range(num_vehicle)) >= 1 for i in range(1,num_node))
    m.addConstrs(x[i,j,k] <= 1 for i in range(num_node) for j in range(num_node) for k in range(num_vehicle))
    m.addConstrs(x[i,i,k] == 0 for i in range(num_node) for k in range(num_vehicle))
    m.addConstrs(gb.quicksum(x[j,i,k] for j in range(num_node)) == gb.quicksum(x[i,j,k] for j in range(num_node)) for i in range(num_node) for k in range(num_vehicle))
    m.addConstrs(gb.quicksum(x[0,j,k] for j in range(num_node)) <= U for k in range(num_vehicle))
    for i in range(1,num_node):
        for j in range(1,num_node):
            if j != i:
                m.addConstrs(mu[i-1]-mu[j-1]+(num_node)*x[i,j,k] <= num_node-1 for k in range(num_vehicle))
    """ for l in range(num_product):
        for k in range(num_vehicle):
            m.addConstr(gb.quicksum(np.ceil(Demand[l][i]/num_vehicle)*gb.quicksum(x[i,j,k] for j in range(num_node)) for i in range(1,num_node)) <= Q_value[k,l]) """
    m.addConstrs(gb.quicksum(gb.quicksum(np.ceil(Demand[l][i]/num_vehicle)*Size[l] for l in range(num_product))*gb.quicksum(x[i,j,k] for j in range(num_node)) for i in range(1,num_node)) <= Capacity for k in range(num_vehicle))
    # m.addConstrs(gb.quicksum(y[i,l,k] for i in range(num_node)) <= Q_value[k,l] for k in range(num_vehicle) for l in range(num_product))
    # m.addConstrs(gb.quicksum(Size[l]*gb.quicksum(y[i,l,k] for i in range(num_node)) for l in range(num_product)) <= Capacity for k in range(num_vehicle))
    # m.addConstrs(gb.quicksum(y[i,l,k] for k in range(num_vehicle)) >= Demand[l][i] for i in range(1,num_node) for l in range(num_product))
    # m.addConstrs(x[i,i+1,k] == 1 for i in range(num_node-1) for k in range(num_vehicle))
    # m.addConstrs(x[num_node-1,0,k] == 1 for k in range(num_vehicle))
    # m.addConstr(gb.quicksum(gb.quicksum(gb.quicksum(x[i,j,k] for k in range(num_vehicle))*cost[i,j] for j in range(num_node)) for i in range(num_node)) >= 1901.0181404341342)
    m.Params.TimeLimit=1800
    # m.Params.TimeLimit=50
    m.Params.LogFile = 'log/S' + str(num_node) + 'D' + str(num_product) + '_heu_global.log'
    m.optimize()
    # cost_re[l] = m.objval
    
    print(sum(cost_re))

if __name__ == "__main__":
    H2(1)