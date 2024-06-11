import numpy as np
import csv
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

def get_P_matrix(K : int):
    cpu_index = 0
    system_disk_indexes = [1,2,3]

    user_disk_probability = .4
    user_disk_indexes = [4 + i for i in range(K)]

    P = [[.15, .2, .15, .1],
        [.35, .25, .0, .0],
        [.35, .0, .25, .0],
        [.35, .0, .0, .25], 
        ]


    for i in range(4):
        for kk in range(K):
            P[i].append(user_disk_probability/K)

    for i in range(K):
        P.append([0. for j in range(4 + K)])

    P = np.array(P)

    # print all
    #print('P:')
    #for arr in P:
    #    print(arr)

    return P

def get_Lambda_array_alpha_dependant(K : int):
    P_transposed = get_P_matrix(K).transpose()
    I_minus_P_transposed =  np.identity(P_transposed.shape[0]) - P_transposed
    inverted  = np.linalg.inv(I_minus_P_transposed)

    A = np.zeros(inverted.shape[0])
    A[0] = 1
    
    lambda_matrix = np.dot(inverted, A)

    return lambda_matrix

def get_resource_name_from_index(index : int):
    if index == 0:
        return 'CPU'
    if index in [1,2,3]:
        return 'SDisk' + str(index)
    if index in [4,5,6,7,8]:
        return 'UDisk' + str(index - 3)


#analytical 1
csv_file = 'protoci_analiticki.csv'
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['K', 'Lambda_CPU(Alpha)', 'Lambda_SDisk1(Alpha)', 'Lambda_SDisk2(Alpha)', 'Lambda_SDisk3(Alpha)', 'Lambda_UDisk1(Alpha)', 'Lambda_UDisk2(Alpha)', 'Lambda_UDisk3(Alpha)', 'Lambda_UDisk4(Alpha)', 'Lambda_UDisk5(Alpha)'])
    for k in range(2,6):
        
        lambda_matrix = get_Lambda_array_alpha_dependant(k)

        writer.writerow([k] + list(lambda_matrix))


#analytical 2
print('Analytical 2')
k_list = []
alpha_list = []
for k in range(2,6):
    lambda_matrix = get_Lambda_array_alpha_dependant(k)
    mi_array = [1/4, 1/10, 1/15, 1/15]
    for i in range(len(lambda_matrix) - len(mi_array)):
        mi_array.append(1/25)
    mi_array = np.array(mi_array)

    max_alpha_array = np.divide(mi_array, lambda_matrix)
    max_alpha = min(max_alpha_array)
    max_alpha_indicies = [index for index, value in enumerate(max_alpha_array) if value == max_alpha]
    critical_resource_names = [get_resource_name_from_index(index) for index in max_alpha_indicies]

    print('K:', k)
    print("Critical resource(s):", critical_resource_names)
    print('Alpha max:', max_alpha*1000)

    k_list.append(k)
    alpha_list.append(max_alpha*1000)

#plot alpha(K) with dots and k must be integer
plt.scatter(k_list, alpha_list)
plt.plot(k_list, alpha_list)
plt.xlabel('K')
plt.ylabel('Alpha (s^-1)')
plt.title('Alpha(K)')
plt.xscale('linear')
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
plt.show()