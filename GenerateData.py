import numpy as np
def GenerateData(num_node, num_product):
    # num_product = 10
    demand_prob = 0.6
    Q = 30
    Size = np.random.randint(1,20,num_product)
    f = open("data/DemandS"+str(num_node)+"P"+str(num_product)+".sd", "w+")
    print("NUM_NODE", num_node, file = f)
    print("NUM_PRODUCT", num_product, file = f)
    print("SIZE", file = f)
    for l in range(num_product):
        print(l, Size[l], file = f)
    Demand = [None]*num_product
    print("DEMAND", file = f)
    for l in range(num_product):
        Demand[l] = np.random.rand(num_node-1)*10
    for i in range(num_node):
        if i == 0:
            print(i+1, end=' ', file = f)
            for l in range(num_product):
                print(0, end=' ', file = f)
        else:
            print(i+1, end=' ', file = f)
            for l in range(num_product):
                print(int(Demand[l][i-1]), end=' ', file = f)
        print("\n", file = f)

if __name__ == "__main__":
    GenerateData(51,4)
    GenerateData(76,4)
    # GenerateData(101,6)
    GenerateData(22,4)
    GenerateData(51,6)
    GenerateData(76,6)
    # GenerateData(101,6)
    GenerateData(22,6)
    GenerateData(51,10)
    GenerateData(76,10)
    # GenerateData(101,6)
    GenerateData(22,10)
