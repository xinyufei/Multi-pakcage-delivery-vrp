import numpy as np
""" def ReadData(file_name, demand_prob, demand_index):
    dataset = []
    file = open("data/"+file_name, mode='r')
    for line in file:
        line = line.strip('\n')
        line = line.split(' ')
        if line[0] != '':
            dataset.append(line) 
        dataset.append(line)
    # print(dataset)
    file.close()
    Edge = []
    start_graph = False
    start_demand = False
    for data in dataset:
        if data[0] == 'DIMENSION':
            n = int(data[2])
            demand = np.zeros(n)
            np.random.seed(demand_index+1)
            randomnumber = np.random.rand(n)
            coord = np.zeros((n,2))
            # print(randomnumber[1])
        if data[0] == 'COMMENT':
            data[7] = data[7].split(',')
            min_num_vehicle = int(data[7][0])
        if data[0] == 'NODE_COORD_SECTION':
            start_graph = True
            continue
        if data[0] == 'DEMAND_SECTION':
            start_graph = False
            start_demand = True
            continue
        if data[0] == 'DEPOT_SECTION':
            start_demand = False
            break
        if start_graph == True:
            # Edge.append((int(data[0])-1, int(data[1])-1))
            coord[int(data[0])-1, 0] = data[1]
            coord[int(data[0])-1, 1] = data[2]
            # cost[(int(data[0])-1, int(data[1])-1)] = data[2]
        if start_demand == True:
            # randomnumber = np.random.rand()
            if randomnumber[int(data[0])-1] < demand_prob:
                demand[int(data[0])-1] = data[1]
            else:
                demand[int(data[0])-1] = 0
    cost = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            cost[i][j] = np.sqrt(np.power(coord[i,0]-coord[j,0],2) + np.power(coord[i,1]-coord[j,1],2))
    return n, min_num_vehicle, cost, Edge, demand """

def ReadGraph(file_name):
    dataset = []
    file = open("data/"+file_name, mode='r')
    for line in file:
        line = line.strip('\n')
        line = line.split(' ')
        if line[0] != '':
            dataset.append(line) 
        # dataset.append(line)
    file.close()
    start_graph = False
    for data in dataset:
        if data[0] == 'DIMENSION':
            n = int(data[2])
            coord = np.zeros((n,2))
            # print(randomnumber[1])
        # if data[0] == 'COMMENT':
            # data[7] = data[7].split(',')
            # min_num_vehicle = int(data[7][0])
        if data[0] == 'NODE_COORD_SECTION':
            start_graph = True
            continue
        if data[0] == 'DEMAND_SECTION':
            start_graph = False
            break
        if start_graph == True:
            coord[int(data[0])-1, 0] = data[1]
            coord[int(data[0])-1, 1] = data[2]
    cost = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            cost[i][j] = np.sqrt(np.power(coord[i,0]-coord[j,0],2) + np.power(coord[i,1]-coord[j,1],2))
    return n, cost

def ReadDemand(file_name):
    dataset = []
    file = open("data/"+file_name, mode='r')
    for line in file:
        line = line.strip('\n')
        line = line.split(' ')
        if line[0] != '':
            dataset.append(line) 
        # dataset.append(line)
    file.close()
    start_size = False
    start_demand = False
    for data in dataset:
        if data[0] == "NUM_NODE":
            n = int(data[1])
        if data[0] == "NUM_PRODUCT":
            num_product = int(data[1])
            Size = np.zeros(num_product)
            demand = np.zeros((num_product, n))
        if data[0] == "SIZE":
            start_size = True
            continue
        if data[0] == "DEMAND":
            start_demand = True
            start_size = False
            continue
        if start_size == True:
            Size[int(data[0])] = int(data[1])
        if start_demand == True:
            for l in range(num_product):
                demand[l][int(data[0])-1] = int(data[l+1])
    return num_product, Size, demand

def GenerateInstanceFromFile(index_instance):
    if index_instance == 0:
        file_name = "S51D1.sd"
        num_node, cost = ReadGraph(file_name)
        file_name = "DemandS51P4.sd"
        num_product, Size, Demand = ReadDemand(file_name)
        Capacity = 1000  
        num_vehicle = int(np.ceil(sum(sum(Demand[l][i] for i in range(num_node))*Size[l] for l in range(num_product))/Capacity))
        c_n = sum(np.ceil(sum(Demand[l][i] for i in range(num_node))/num_vehicle)*Size[l] for l in range(num_product))
        while c_n > Capacity:
            num_vehicle += 1
            c_n = sum(np.ceil(sum(Demand[l][i] for i in range(num_node))/num_vehicle)*Size[l] for l in range(num_product))
        """ Q_product = [int(Capacity/Size[l]) for l in range(num_product)]
        num_vehicle_product = [int(np.ceil(sum(Demand[l][i] for i in range(num_node))/Q_product[l])) for l in range(num_product)]
        num_vehicle = sum(num_vehicle_product) """
        """ print([(np.ceil(sum(Demand[l][i]for i in range(num_node))/num_vehicle_product[l]))*Size[l] for l in range(num_product)])
        for l in range(num_product):
            print((np.ceil(sum(Demand[l][i]for i in range(num_node))/num_vehicle_product[l]))*num_vehicle_product[l] - sum(Demand[l][i] for i in range(num_node))) """
        Q_product = [int(np.ceil(sum(Demand[l][i] for i in range(num_node))/num_vehicle)) for l in range(num_product)]
        print([Q_product[l]*num_vehicle - sum(Demand[l][i] for i in range(num_node)) for l in range(num_product)])
        print([sum(Demand[l][i] for i in range(num_node)) - (num_vehicle-1)*Q_product[l] for l in range(num_product)])
        num_vehicle_product = []
        # num_vehicle = (num_node-1)*num_product
    if index_instance == 1:
        file_name = "S76D1.sd"
        num_node, cost = ReadGraph(file_name)
        file_name = "DemandS76P4.sd"
        num_product, Size, Demand = ReadDemand(file_name)
        Capacity = 1200  
        Q_product = [int(Capacity/Size[l]) for l in range(num_product)]
        num_vehicle_product = [int(np.ceil(sum(Demand[l][i] for i in range(num_node))/Q_product[l])) for l in range(num_product)]
        num_vehicle = sum(num_vehicle_product)
    if index_instance == 2:
        file_name = "S101D1.sd"
        num_node, cost = ReadGraph(file_name)
        file_name = "DemandS101P10.sd"
        num_product, Size, Demand = ReadDemand(file_name)
        Capacity = 1200  
        num_vehicle_product = [int(np.ceil(sum(Demand[l][i] for i in range(num_node))*Size[l]/Capacity)) for l in range(num_product)]
        num_vehicle = sum(num_vehicle_product)
    if index_instance == 3:
        file_name = "eil22.sd"
        num_node, cost = ReadGraph(file_name)
        file_name = "DemandS22P4.sd"
        num_product, Size, Demand = ReadDemand(file_name)
        Capacity = 1200 
        Q_product = [int(Capacity/Size[l]) for l in range(num_product)]
        num_vehicle_product = [int(np.ceil(sum(Demand[l][i] for i in range(num_node))/Q_product[l])) for l in range(num_product)]
        num_vehicle = sum(num_vehicle_product)
    return [num_node, num_product, Q_product, num_vehicle, num_vehicle_product, Capacity, Size, cost, Demand]

def GenerateInstance(index_instance = 0):
    if index_instance == 0:
        num_product = 6
        demand_prob = 0.6
        Demand = [None]*num_product
        min_num_vehicle = [None]*num_product
        np.random.seed(1)
        Size = np.random.randint(1,6,num_product)
        Capacity = 160*5
        for l in range(num_product):
            file_name = "S51D" + str(l+1) + ".sd"
            num_node, min_num_vehicle[l], cost, Edge, Demand[l] = ReadData(file_name, demand_prob, l)
        num_vehicle = int(sum(min_num_vehicle)*demand_prob/2)
    if index_instance == 1:
        # num_product = 4
        num_product = 6
        demand_prob = 0.6
        Demand = [None]*num_product
        min_num_vehicle = [None]*num_product
        np.random.seed(2)
        Size = np.random.randint(1,6,num_product)
        Capacity = 160*5
        for l in range(num_product):
            file_name = "S76D" + str(l+1) + ".sd"
            num_node, min_num_vehicle[l], cost, Edge, Demand[l] = ReadData(file_name, demand_prob, l)
        num_vehicle = int(sum(min_num_vehicle))
    if index_instance == 2:
        num_product = 4
        demand_prob = 0.6
        Demand = [None]*num_product
        min_num_vehicle = [None]*num_product
        np.random.seed(3)
        Size = np.random.randint(1,6,num_product)
        Capacity = 160*5
        for l in range(num_product):
            file_name = "S101D" + str(l+1) + ".sd"
            num_node, min_num_vehicle[l], cost, Edge, Demand[l] = ReadData(file_name, demand_prob, l)
        num_vehicle = int(sum(min_num_vehicle))
    return [num_node, num_product, num_vehicle, Capacity, Size, cost, Edge, Demand]


""" if __name__ == '__main__':
    [num_node, num_product, num_vehicle, Capacity, Size, cost, Edge, Demand] = GenerateInstance(2)
    # print(cost)
    print(num_product)
    print(num_vehicle)
    print(Capacity)
    print(Size)
    print(cost)
    print(Edge)
    print(Demand)
    for i in range(num_node):
        if sum(Demand[j][i] for j in range(num_product)) == 0:
            print(i) """