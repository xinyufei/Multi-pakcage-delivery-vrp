from ImportData import *
import gurobipy as gb

def SolveByGurobi(instance_index):
    # [num_node, num_product, num_vehicle, Capacity, Size, cost, Edge, Demand] = GenerateInstance(instance_index)
    [num_node, num_product, Q_product, num_vehicle, num_vehicle_product, Capacity, Size, cost, Demand] = GenerateInstanceFromFile(instance_index)
    U = 5
    # num_vehicle = 45
    m = gb.Model()
    x = m.addVars(num_node, num_node, num_vehicle, vtype = gb.GRB.BINARY)
    # x = m.addVars(num_node, num_node, num_vehicle, vtype = gb.GRB.CONTINUOUS)
    u = m.addVars(num_vehicle, vtype = gb.GRB.BINARY)
    # u = m.addVars(num_vehicle, vtype = gb.GRB.CONTINUOUS)
    mu = m.addVars(num_node-1)
    y = m.addVars(num_node, num_product, num_vehicle, vtype = gb.GRB.INTEGER)
    # y = m.addVars(num_node, num_product, num_vehicle, vtype = gb.GRB.CONTINUOUS)
    m.setObjective(gb.quicksum(gb.quicksum(gb.quicksum(x[i,j,k] for k in range(num_vehicle))*cost[i,j] for j in range(num_node)) for i in range(num_node)))
    m.addConstrs(x[i,j,k] <= u[k] for i in range(num_node) for j in range(num_node) for k in range(num_vehicle))
    m.addConstrs(x[i,i,k] == 0 for i in range(num_node) for k in range(num_vehicle))
    m.addConstrs(x.sum('*',i,k) == x.sum(i,'*',k) for i in range(num_node) for k in range(num_vehicle))
    m.addConstrs(x.sum('*',0,k) <= u[k]*U for k in range(num_vehicle))
    for i in range(1,num_node):
        for j in range(1,num_node):
            if j != i:
                m.addConstrs(mu[i-1]-mu[j-1]+(num_node)*x[i,j,k] <= num_node-1 for k in range(num_vehicle))
    m.addConstrs(y[i,l,k] <= Demand[l][i]*gb.quicksum(x[i,j,k] for j in range(num_node)) for i in range(1,num_node) for l in range(num_product) for k in range(num_vehicle))
    m.addConstrs(gb.quicksum(Size[l]*gb.quicksum(y[i,l,k] for i in range(num_node)) for l in range(num_product)) <= Capacity*u[k] for k in range(num_vehicle))
    m.addConstrs(gb.quicksum(y[i,l,k] for k in range(num_vehicle)) >= Demand[l][i] for i in range(1,num_node) for l in range(num_product))
    # m.addConstrs(u[k] ==1 for k in range(num_vehicle))
    m.Params.LogFile = 'log/S' + str(num_node) + 'D' + str(num_product) + '.log'
    # m.Params.LogFile = 'log/S' + str(num_node) + 'D' + str(num_product) + '_lb.log'
    m.Params.TimeLimit = 720
    m.optimize()

if __name__ == "__main__":
    SolveByGurobi(3)
    SolveByGurobi(0)
    SolveByGurobi(1)