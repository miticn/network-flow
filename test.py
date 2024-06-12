import numpy as np
import csv
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import copy
from util import *


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

    max_alpha = max_alpha*0.99
    print('K:', k)
    print("Critical resource(s):", critical_resource_names)
    print('Alpha max:', max_alpha*1000)

    k_list.append(k)
    alpha_list.append(max_alpha)

#plot alpha(K) with dots and k must be integer
alpha_in_s_1 = [alpha*1000 for alpha in alpha_list]
plt.scatter(k_list, alpha_in_s_1)
plt.plot(k_list, alpha_in_s_1)
plt.xlabel('K')
plt.ylabel('Alpha (s^-1)')
plt.title('Alpha(K)')
plt.xscale('linear')
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
plt.show()

#analytical 3
#potrebno je odrediti iskorišćenja resursa, protoke kroz resurse, 
#prosečan broj poslova u svakom od resursa ovog sistema i vreme odziva
#ovog sistema sa centralnim serverom za K od 2 do 5.
print('Analytical 3')
with open('rezultati_analiticki.csv', 'w', newline='') as csvfile:
    header = ['K', 'r', 'T', 'Ucpu', 'Uds1', 'Uds2', 'Uds3', 'Udu1', 'Udu2', 'Udu3', 'Udu4', 'Udu5',
                  'Xcpu', 'Xds1', 'Xds2', 'Xds3', 'Xdu1', 'Xdu2', 'Xdu3', 'Xdu4', 'Xdu5',
                  'Jcpu', 'Jds1', 'Jds2', 'Jds3', 'Jdu1', 'Jdu2', 'Jdu3', 'Jdu4', 'Jdu5']
    writer = csv.writer(csvfile)
    writer.writerow(header)

    r_list = [0.30, 0.55, 0.80, 1.00]
    for k in k_list:
        for r in r_list:
            print('K:', k)
            print('R:', r)
            lambda_matrix = get_Lambda_array_alpha_dependant(k)
            mi_array = [1/4, 1/10, 1/15, 1/15]
            for i in range(len(lambda_matrix) - len(mi_array)):
                mi_array.append(1/25)
            mi_array = np.array(mi_array)

            alpha_max = alpha_list[k-2]
            alpha = r*alpha_max

            lambda_matrix = lambda_matrix*alpha

            #iskoriscenja resursa
            U = []
            for i in range(len(lambda_matrix)):
                U.append(lambda_matrix[i]/mi_array[i])
            print('Utilization:', U)

            #protoke kroz resurse
            X = []
            for i in range(len(lambda_matrix)):
                X.append(lambda_matrix[i])
            print('Throughput:', X)

            #prosečan broj poslova u svakom od resursa ovog sistema
            J = []
            for i in range(len(lambda_matrix)):
                J.append(lambda_matrix[i]/(mi_array[i] - lambda_matrix[i]))
            print('Average number of jobs:', J)

            #vreme odziva ovog sistema sa centralnim serverom
            R_total = 0
            lambda_matrix_dependant_on_alpha = get_Lambda_array_alpha_dependant(k)
            for i in range(len(lambda_matrix_dependant_on_alpha)):
                T_curr = J[i]/X[i]
                R_total += T_curr * lambda_matrix_dependant_on_alpha[i]
            
            print('Response time:', R_total/1000)

            print('\n')

            #pad U, X, J to 9 elements
            while len(U) < 9:
                U.append(0)
            while len(X) < 9:  
                X.append(0)
            while len(J) < 9:
                J.append(0)
            

            X_in_s_1 = [x*1000 for x in X]
            R_total = R_total/1000
            row = [k, r, R_total] + U + X_in_s_1 + J
            

            writer.writerow(row)
